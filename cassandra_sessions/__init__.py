from cassandra import ConsistencyLevel, InvalidRequest
from cassandra.cluster import Cluster

from django.conf import settings
from django.contrib.sessions.backends.base import SessionBase, CreateError


host = getattr(settings, 'CASSANDRA_HOSTS', ('127.0.0.1',))
port = getattr(settings, 'CASSANDRA_PORT', 9042)
keyspace = getattr(settings, 'CASSANDRA_SESSION_KEYSPACE', 'django_cassandra')
table = getattr(settings, 'CASSANDRA_SESSIONS_TABLE', 'sessions')

cluster = Cluster(host, port=port)
cassandra_session = cluster.connect()

try:
    load = cassandra_session.prepare('''
        SELECT * FROM %s.%s
        WHERE session_key = ?
    ''' % (keyspace, table))
    load.consistency_level = ConsistencyLevel.QUORUM

    delete = cassandra_session.prepare('''
        DELETE FROM %s.%s
        WHERE session_key = ?
    ''' % (keyspace, table))
    delete.consistency_level = ConsistencyLevel.QUORUM
except InvalidRequest:
    import os

    ddl = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            'ddl.cql')).read()
    raise InvalidRequest(
        "Column families not properly configured. "
        "Please use a schema similar to:\n\n%s" % ddl)


class SessionStore(SessionBase):
    """
    A Cassandra-based session store.
    """

    def __init__(self, session_key=None):
        self._last_insert = None
        self._last_insert_ttl = None

        super(SessionStore, self).__init__(session_key)

    def _execute_query(self, prepared_statement, bind_tuple, ttl=None):
        """
        A helper method to execute prepared statements
        """
        if not prepared_statement:
            if self._last_insert_ttl == ttl:
                prepared_statement = self._last_insert
            else:
                prepared_statement = cassandra_session.prepare('''
                    INSERT INTO %s.%s
                        (session_key, session_data)
                    VALUES
                        (?, ?)
                    USING TTL %s
                ''' % (keyspace, table, ttl))
                prepared_statement.consistency_level = ConsistencyLevel.QUORUM

                self._last_insert = prepared_statement
                self._last_insert_ttl = ttl

        return cassandra_session.execute(prepared_statement.bind(bind_tuple))

    @property
    def cache_key(self):
        return self._get_or_create_session_key()

    def load(self):
        """
        Loads the session data and returns a dictionary.
        """
        try:
            results = self._execute_query(load, (self.cache_key,))
            if results[0].session_data:
                return results[0].session_data
            return {}
        except IndexError:
            self.create()
            return {}

    def create(self):
        """
        Creates a new session instance. Guaranteed to create a new object with
        a unique key and will have saved the result once (with empty data)
        before the method returns.
        """
        for i in xrange(100):
            self._session_key = self._get_new_session_key()
            try:
                self.save(must_create=True)
            except CreateError:
                continue
            self.modified = True
            return
        raise RuntimeError(
            "Unable to create a new session key. "
            "It is likely that Cassandra is unavailable.")

    def save(self, must_create=False):
        """
        Saves the session data. If 'must_create' is True, a new session object
        is created (otherwise a CreateError exception is raised). Otherwise,
        save() can update an existing object with the same key.
        """
        cache_key = self.cache_key
        if must_create and self.exists(cache_key):
            raise CreateError
        self._execute_query(None,
                            (cache_key, self._get_session(no_load=must_create)),
                            self.get_expiry_age())

    def exists(self, session_key):
        """
        Returns True if the given session_key already exists.
        """
        results = self._execute_query(load, (session_key,))
        if results:
            return True
        else:
            return False

    def delete(self, session_key=None):
        """
        Deletes the session data under this key. If the key is None, the
        current session key value is used.
        """
        if session_key is None:
            if self.session_key is None:
                return
            session_key = self.session_key
        self._execute_query(delete, (session_key,))

    @classmethod
    def clear_expired(cls):
        """
        Remove expired sessions from the session store.

        If this operation isn't possible on a given backend, it should raise
        NotImplementedError. If it isn't necessary, because the backend has
        a built-in expiration mechanism, it should be a no-op.
        """
        pass

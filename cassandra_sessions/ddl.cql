CREATE KEYSPACE django_cassandra
WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1 };

CREATE TABLE django_cassandra.sessions (
    session_key text,
    session_data map<blob, blob>,
    PRIMARY KEY (session_key)
);

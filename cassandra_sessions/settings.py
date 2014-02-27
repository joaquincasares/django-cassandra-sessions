SECRET_KEY = 'hash-needed-for-django'

# Ability to test both backends, currently testing cassandra_sessions
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_ENGINE = 'cassandra_sessions'

CASSANDRA_HOSTS = ('127.0.0.1',)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3'
    }
}

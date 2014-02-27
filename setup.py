from setuptools import setup, find_packages
 
version = '0.2.0'
 
LONG_DESCRIPTION = """
django-cassandra-sessions
=========================

This is a session backend for Django that stores sessions in Cassandra,
using the DataStax Driver for Apache Cassandra.

Installing django-cassandra-sessions
------------------------------------

1. Either download the tarball and run ``python setup.py install``, or simply
   use easy install or pip like so ``easy_install django-cassandra-sessions``.


2. Set ``cassandra_sessions`` as your session engine, like so::

       SESSION_ENGINE = 'cassandra_sessions'


3. Setup the proper schema. For example:

       CREATE KEYSPACE django_cassandra
       WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1 };

       CREATE TABLE django_cassandra.sessions (
           session_key text,
           session_data map<blob, blob>,
           PRIMARY KEY (session_key)
       );


4. (optional) Add settings describing where to connect to Cassandra::

       CASSANDRA_HOSTS = ('127.0.0.1',)
       CASSANDRA_PORT = 9042
       CASSANDRA_SESSIONS_KEYSPACE = 'django_cassandra'
       CASSANDRA_SESSIONS_TABLE = 'sessions'
"""
 
setup(
    name='django-cassandra-sessions',
    version=version,
    description="This is a session backend for Django that stores sessions in Cassandra, using the DataStax Driver for Apache Cassandra.",
    long_description=LONG_DESCRIPTION,
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Framework :: Django",
        "Environment :: Web Environment",
    ],
    keywords='cassandra,session,django',
    author='Mat Clayton',
    author_email='mat@wakari.co.uk',
    url='http://github.com/matclayton/django-cassandra-sessions/tree/master',
    license='MIT',
    packages=find_packages(),
    zip_safe=False,
    install_requires=['setuptools', 'cassandra-driver',],
    include_package_data=True,
    setup_requires=['setuptools_git'],
)

r"""
>>> from importlib import import_module
>>> from django.conf import settings
>>> SessionStore = import_module(settings.SESSION_ENGINE).SessionStore

# >>> settings.configure()
>>> session_store = SessionStore()
>>> session_store.modified
False
>>> session_store.get('cat')
>>> session_store['cat'] = "dog"
>>> session_store.modified
True
>>> session_store.pop('cat')
'dog'
>>> session_store.pop('some key', 'does not exist')
'does not exist'
>>> session_store.save()
>>> session_store.exists(session_store.session_key)
True
>>> session_store.delete(session_store.session_key)
>>> session_store.exists(session_store.session_key)
False

>>> session_store['foo'] = 'bar'
>>> session_store.save()
>>> session_store.exists(session_store.session_key)
True
>>> prev_key = session_store.session_key
>>> session_store.flush()
>>> session_store.exists(prev_key)
False
>>> session_store.session_key == prev_key
False
>>> session_store.modified, session_store.accessed
(True, True)
>>> session_store['a'], session_store['b'] = 'c', 'd'
>>> session_store.save()
>>> prev_key = session_store.session_key
>>> prev_data = session_store.items()
>>> session_store.cycle_key()
>>> session_store.session_key == prev_key
False
>>> session_store.items() == prev_data
True
>>> session_store['a']
'c'
>>> session_store['b']
'd'
"""

if __name__ == '__main__':
    import os
    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
    import doctest
    doctest.testmod()

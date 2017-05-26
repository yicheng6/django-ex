import os

def config():
    return {
    	'DB': os.getenv('DATABASE_DB'),
        'USER': os.getenv('DATABASE_USER'),
        'PASSWD': os.getenv('DATABASE_PASSWD'),
        'HOST': os.getenv('DATABASE_HOST'),
        'PORT': os.getenv('DATABASE_PORT'),
    }
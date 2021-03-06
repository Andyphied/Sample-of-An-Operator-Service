import os
from pathlib import Path
from flask_sqlalchemy import SQLAlchemy
from flask_mongoengine import MongoEngine

DATABASE_ENGINE = os.environ.get('DATABASE_ENGINE', 'LOCAL')

if DATABASE_ENGINE == 'LOCAL':
    dir_path = Path(os.path.dirname(os.path.realpath(__file__)))
    path = dir_path / '..'

    # Sqlite Database initialisation
    FILE_PATH = f'{path}/db.sqlite3'
    DB_URI = 'sqlite+pysqlite:///{file_path}'

    db_config = {
        'SQLALCHEMY_DATABASE_URI': DB_URI.format(file_path=FILE_PATH),
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    }

    mongo_config = {
        'db': 'test',
        'host': 'mongodb://localhost:27017/test'
        }

elif DATABASE_ENGINE == 'TEST_ENGINE':
    dir_path = Path(os.path.dirname(os.path.realpath(__file__)))
    path = dir_path / '..'

    # Sqlite Database initialisation
    FILE_PATH = f'{path}/db.sqlite3'
    DB_URI = 'sqlite+pysqlite:///{file_path}'

    mongo_params = {
        'host': os.environ['MONGODB_HOST'],
        'database': os.environ['MONGODB_DB'],
        'user': os.environ['MONGODB_USER'],
        'pwd': os.environ['MONGODB_PASSWORD'],
        'port': int(os.environ['MONGODB_PORT']),
    }

    MONGO_URI = ('mongodb://{user}:{pwd}@{host}:{port}/{database}'
                 '?authSource=admin')

    mongo_config = {
        'host': MONGO_URI.format(**mongo_params)
    }

    db_config = {
        'SQLALCHEMY_DATABASE_URI': DB_URI.format(file_path=FILE_PATH),
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    }


elif DATABASE_ENGINE == 'POSTGRESQL':
    db_params = {
        'host': os.environ['POSTGRES_HOST'],
        'database': os.environ['POSTGRES_DB'],
        'user': os.environ['POSTGRES_USER'],
        'pwd': os.environ['POSTGRES_PASSWORD'],
        'port': os.environ['POSTGRES_PORT'],
    }

    mongo_config = {
        'db': 'test',
        'host': 'mongodb://localhost:27017/test'
        }

    DB_URI = 'postgresql://{user}:{pwd}@{host}:{port}/{database}'

    db_config = {
        'SQLALCHEMY_DATABASE_URI': DB_URI.format(**db_params),
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    }

elif DATABASE_ENGINE == 'DEV_ENGINE':
    db_params = {
        'host': os.environ['POSTGRES_HOST'],
        'database': os.environ['POSTGRES_DB'],
        'user': os.environ['POSTGRES_USER'],
        'pwd': os.environ['POSTGRES_PASSWORD'],
        'port': os.environ['POSTGRES_PORT'],
    }
    mongo_params = {
        'host': os.environ['MONGODB_HOST'],
        'database': os.environ['MONGODB_DB'],
        'user': os.environ['MONGODB_USER'],
        'pwd': os.environ['MONGODB_PASSWORD'],
        'port': int(os.environ['MONGODB_PORT']),
    }

    MONGO_URI = ('mongodb://{user}:{pwd}@{host}:{port}/{database}'
                 '?authSource=admin')

    mongo_config = {
        'host': MONGO_URI.format(**mongo_params)
    }
    DB_URI = 'postgresql://{user}:{pwd}@{host}:{port}/{database}'

    db_config = {
        'SQLALCHEMY_DATABASE_URI': DB_URI.format(**db_params),
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    }

else:
    raise Exception('Incorrect DATABASE_ENGINE')


db = SQLAlchemy()
mongo = MongoEngine()

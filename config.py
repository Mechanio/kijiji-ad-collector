import os
from dotenv import load_dotenv

# project_root = os.getcwd()
# load_dotenv(os.path.join(project_root, '.env'))
load_dotenv()


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')

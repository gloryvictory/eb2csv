import os
from time import strftime  # Load just the strftime Module from Time

# from dotenv import load_dotenv
# load_dotenv() # читаем из .env и устанавливаем переменные окружения

API_VERSION = "/api/v1"

DATETIME_CURRENT = str(strftime("%Y-%m-%d-%H-%M-%S"))

FILE_LOG_NAME = 'eb2csv'
FILE_LOG = DATETIME_CURRENT + '_' + FILE_LOG_NAME + '.log'
FILE_LOG_FORMAT = '%(asctime)s %(levelname)s %(message)s'


# FOLDER_BASE = os.getenv("FOLDER_BASE", "C:\\Glory\\Projects\\Python\\")
FOLDER_OUT = 'log'
FOLDER_GEOJSON_OUT = 'geojson'
FOLDER_DATA = 'data'

# DB_SQLITE = "sqlite:///test.db"
# DB_SCHEMA = 'test'
# DB_HOST = os.getenv("DB_HOST", 'localhost')
# DB_PORT = os.getenv("DB_PORT", '5432')
# DB_USER = os.getenv("DB_USER", 'test')
# DB_PASS = os.getenv("DB_PASS", 'testpwd')
# DB_NAME = os.getenv("DB_NAME", 'test')
# DB_SCHEMA = os.getenv("DB_SCHEMA", 'geodex2')
# DB_DSN = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

CRS_OUT = 4326  # 4326 - WGS 84

# FIELDS_FILE_GEOJSON_IN = 'FIELDS.geojson' # 'mest.geojson'
# FIELDS_FILE_GEOJSON_OUT = 'FIELDS.geojson'
# FIELDS_NAME_FIELD = 'name_ru'
# FIELDS_FILE_LOG = FIELDS_FILE_GEOJSON_IN + '.log'


class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE_URI = "mysql+pymysql://root:password@localhost/svvaul"


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    MAX_CONTENT_LENGTH = 16 * 1000 * 1000

    # UPLOAD_PHOTOS_RELATIVE = '/uploads'
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}


class TestingConfig(Config):
    TESTING = True


DB_PASSWORD = "2364855112"
DB_NAME = "evm_lab"

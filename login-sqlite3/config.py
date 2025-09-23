class Config:
    SECRET_KEY = "clave123"

class DevelopmentConfig(Config):
    DEBUG = True

config = {
    'development': DevelopmentConfig
}
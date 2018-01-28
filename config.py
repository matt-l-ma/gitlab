# -*- coding:utf-8 -*-

import sys
default_encodeing = "utf-8"

if sys.getdefaultencoding() != default_encodeing:
    reload(sys)
    sys.setdefaultencoding(default_encodeing)

import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Internationalization 
    SUPPORTED_LANGUAGES = { 'en': 'English', 'zh_CN': 'Chinese' }
    BABEL_DEFAULT_LOCALE = 'zh_CN'
    BABEL_DEFAULT_TIMEZONE = 'UTC'

    @staticmethod
    def init_app(app):
        pass

class DevConfig(Config):
    DEBUG =True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'mysql://root:0210@localhost:3306/scm_admin'
    # Internationalization 
    SUPPORTED_LANGUAGES = { 'en': 'English', 'zh_CN': 'Chinese' }
    BABEL_DEFAULT_LOCALE = 'zh_CN'
    BABEL_DEFAULT_TIMEZONE = 'UTC'

config = {
    'development' : DevConfig,
    'default' : DevConfig
}
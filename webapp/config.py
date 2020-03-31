import os

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir,
                                                      '..', 'webapp.db'
                                                      )

SECRET_KEY = 'i43bT4i3fN43nG34bndu3ndieF3'

SQLALCHEMY_TRACK_MODIFICATIONS = False
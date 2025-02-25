import os

class Config:
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://redis:6379/0')
    CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://redis:6379/0')
    MATRIX_HOMESERVER_URL = os.getenv('MATRIX_HOMESERVER_URL', 'https://matrix.halleysud.it')
    MATRIX_USER = os.getenv('MATRIX_USER', '@giordana:matrix.halleysud.it')
    MATRIX_PASSWORD = os.getenv('MATRIX_PASSWORD', 'Giord@n@')
    MATRIX_ROOM_ID = os.getenv('MATRIX_ROOM_ID', '!NZjipmSSzPqrGSIpEo:matrix.halleysud.it')
  


#@giordanap:matrix.org
#@giordanap
#!BrxNdJPMMXCXLjPJru:matrix.halleysud.it
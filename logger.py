import boto3
from datetime import datetime
import logging


region_name = "us-east-2"

# Create a Secrets Manager client
session = boto3.session.Session()
client = session.client(
    service_name='secretsmanager',
    region_name=region_name
)

def create_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    fh = logging.FileHandler('{}_{}.log'.format(logger_name, datetime.now().isoformat().split('.')[0]))
    fh.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    return logger

def upload_log(logger):
    file_name = logger.handlers[0].baseFilename
    directory = datetime.now().date().isoformat()
    key = "{}/{}".format(directory, file_name.split('/')[-1])
    bucket_name = "coinbase_bot_logs"

    client.upload_file(Filename = file_name, Bucket = bucket_name, Key = key)

def logger(func):
    def function_wrapper(*args, **kwargs):
        function_name = func.__name__
        logger = create_logger(function_name)
        logger.infor("Now running - {}".format(function_name))

        resp = func(logger = logger, *args, **kwargs)
        upload_log(logger)

        return resp
    return function_wrapper
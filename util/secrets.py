import boto3
import os
import yaml

from botocore.exceptions import ClientError
from pathlib import Path


BASE_DIR = str(Path(__file__).resolve(strict=True).parent.parent)


def get_secret(secret_name):
    secret_path = f'/zid/{os.getenv("ENVIRONMENT")}/{secret_name}'
    try:
        return get_local_secret(secret_path)
    except (FileNotFoundError, FileExistsError, KeyError):
        return get_remote_secret(secret_path)


def get_remote_secret(secret_path: str):
    try:
        client = boto3.client('ssm', region_name='us-east-1')
        response = client.get_parameter(
            Name=secret_path,
            WithDecryption=True
        )
        return response['Parameter']['Value']
    except ClientError:
        return None


def get_local_secret(secret_path: str):
    with open(BASE_DIR + f'/{os.getenv("ENVIRONMENT")}-properties.yml') as secrets_file:
        secrets = yaml.safe_load(secrets_file)
    return find_in_dict(secrets, secret_path.split('/')[1:])


def find_in_dict(secrets: dict, secret_path: list):
    # KeyError possibly thrown; handled in get_secret method
    result = secrets[secret_path.pop(0)]

    if len(secret_path) > 0:
        return find_in_dict(result, secret_path)
    else:
        return result

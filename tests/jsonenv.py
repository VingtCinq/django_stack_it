import json
import os


def get_credentials():
    conf = os.environ.get('CONF', '')
    file_ = ".env.json"
    if conf:
        file_ = f".env.{conf}.json"
    print(f'LOADING CREDS FROM FILE {file_}')
    env_file_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(os.path.join(env_file_dir, file_), 'r') as f:
        creds = json.loads(f.read())
    return creds


env = get_credentials()

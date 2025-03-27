import json
import os
import pathlib
import pytest

@pytest.fixture(scope="session")
def config():
    ENV=os.getenv('ENV') or 'dev'
    current_dir=str(pathlib.Path(__file__).resolve().parent)
    config_path =os.getenv('CONFIG_PATH') or f"{current_dir}/configs/{ENV}/config.json"
    with open(config_path) as fp:
        return json.load(fp)

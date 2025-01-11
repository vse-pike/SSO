import os

import pytest
import pytest_asyncio
from dotenv import load_dotenv

from main import HttpClient, PublicApi, InternalApi, DbClient, DbActions

def pytest_addoption(parser):
    parser.addini("env_file", help="Path to the .env file", default="./.env")

@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    env_file = config.getini("env_file")
    if env_file and os.path.exists(env_file):
        load_dotenv(env_file)

@pytest.fixture(scope="function")
def public_api():
    url = os.getenv("PUBLIC_API_URL")
    if url is None:
        raise Exception("PUBLIC_API_URL is not set")
    client = HttpClient(base_url=url)
    return PublicApi(client)


@pytest.fixture(scope="function")
def internal_api():
    url = os.getenv("INTERNAL_API_URL")
    if url is None:
        raise Exception("INTERNAL_API_URL is not set")
    client = HttpClient(base_url=url)
    return InternalApi(client)


@pytest_asyncio.fixture(scope="function")
async def db_actions():
    dsn = os.getenv("CONNECTION_STRING")
    if dsn is None:
        raise Exception("CONNECTION_STRING is not set")
    async with DbClient(dsn) as client:
        db_actions = DbActions(client)
        yield db_actions


@pytest.fixture(scope="session")
def is_local_run():
    ci = os.getenv("CI")
    if ci is not None and ci.lower() == "true":
        print("\nRunning on CI\n")
        return False
    else:
        print("\nRunning on local\n")
        return True


@pytest_asyncio.fixture(autouse=True)
async def truncate_db(is_local_run, db_actions: DbActions):
    if not is_local_run:
        return

    await db_actions.truncate()


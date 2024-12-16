import os
import json
import secrets
import tarfile
import asyncio
import traceback
import functools
from beanie import BulkWriter
from beanie import init_beanie
from tri_api.core.logger import logger
from tri_api.models.trove.cve import CVE
from tri_api.support.enums import AWSOption
from tri_api.support.config import CONFIGURATION
from motor.motor_asyncio import AsyncIOMotorClient
from tri_api.models.tenant.tenant import InviteToken
from tri_api.models.trove.taxonomy import CWE, CAPEC
from tri_api.aws.utils import scrape, create_presigned_link
from tri_api.celery.app import async_to_sync, tri_api_celery_app


async def init_database():
    client = AsyncIOMotorClient(CONFIGURATION.mongo_uri)
    db = client.account

    await init_beanie(
        database=db,
        document_models=[
            CVE,
            CWE,
            CAPEC,
        ],
    )
    return client


async def populate_database():
    logger.info("Downloading data file from s3")
    file_name = AWSOption.file.value
    await init_database()
    file_name += ".tar.gz"
    link = create_presigned_link(file_name)

    try:

        response = scrape(link)
        file_name = AWSOption.download_dir.value + file_name

        with open(file_name, "wb") as handle:
            handle.write(response.content)

        if not os.path.isfile(file_name):
            raise Exception("Downloaded file not found")

        with tarfile.open(file_name, "r:gz") as tar:
            tar.extractall(path=AWSOption.download_dir.value)

        cwe_file = os.path.join(AWSOption.download_dir.value, "cwe.jsonl")
        cve_file = os.path.join(AWSOption.download_dir.value, "cve.jsonl")
        capec_file = os.path.join(AWSOption.download_dir.value, "capec.jsonl")

        # Updating CWE database
        logger.info("Updating CVE database in mongo")
        with open(cve_file, "r") as fp:
            cve_chunk = []
            line = next(fp, None)
            while line:
                line = line.strip()
                obj = json.loads(line)

                cve_chunk.append(CVE(**obj))

                if len(cve_chunk) == 100:
                    async with BulkWriter() as bulk_writer:
                        for doc in cve_chunk:
                            await doc.save()
                        await bulk_writer.commit()
                    cve_chunk = []

                line = next(fp, None)

            if cve_chunk:
                async with BulkWriter() as bulk_writer:
                    for doc in cve_chunk:
                        await doc.save()
                    await bulk_writer.commit()

        logger.info("CVE database updated")

        # Updating CWE database
        logger.info("Updating CWE database in mongo")
        with open(cwe_file, "r") as fp:
            cwe_chunk = []
            line = next(fp, None)
            while line:
                line = line.strip()
                obj = json.loads(line)

                cwe_chunk.append(CWE(**obj))

                if len(cwe_chunk) == 100:
                    async with BulkWriter() as bulk_writer:
                        for doc in cwe_chunk:
                            await doc.save()
                        await bulk_writer.commit()
                    cwe_chunk = []

                line = next(fp, None)

            if cwe_chunk:
                async with BulkWriter() as bulk_writer:
                    for doc in cwe_chunk:
                        await doc.save()
                    await bulk_writer.commit()

        logger.info("CWE database updated")

        # Updating CAPEC database
        logger.info("Updating CAPEC database in mongo")
        with open(capec_file, "r") as fp:
            capec_chunk = []
            line = next(fp, None)
            while line:
                line = line.strip()
                obj = json.loads(line)

                capec_chunk.append(CAPEC(**obj))

                if len(capec_chunk) == 100:
                    async with BulkWriter() as bulk_writer:
                        for doc in capec_chunk:
                            await doc.save()
                        await bulk_writer.commit()
                    capec_chunk = []

                line = next(fp, None)

            if capec_chunk:
                async with BulkWriter() as bulk_writer:
                    for doc in capec_chunk:
                        await doc.save()
                    await bulk_writer.commit()

        logger.info("CAPEC database updated")

    except Exception as err:
        logger.error(err)
        logger.debug(traceback.format_exc())


@async_to_sync
async def sample_func():
    pass


@tri_api_celery_app.task()
def sample_task():
    sample_func()


@tri_api_celery_app.task(
    name="test_task",
    queue="tri",
    exchange="tri",
    routing_key="tri",
    max_retries=3,
)
def test_task():
    for i in range(10):
        logger.info(f"Running test task {i}")


@tri_api_celery_app.task(
    name="populate_trove_intel_database",
    queue="tri",
    exchange="tri",
    routing_key="tri",
    max_retries=3,
)
def populate_trove_intel_database():
    """Celery task to populate CVE, CWE and CAPEC databases"""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    try:
        loop.run_until_complete(populate_database())
    except Exception as e:
        logger.error(f"Task execution failed: {str(e)}")
        logger.debug(traceback.format_exc())

from fipy.ngsi.entity import EntityUpdateNotification
from fipy.ngsi.headers import FiwareContext
from fastapi import FastAPI, Header
from typing import Optional

from loguru import logger

from cncsmart import __version__
from cncsmart.enteater import process_update
from cncsmart.ngsy import PartProgramEntity


app = FastAPI()


@app.get('/')
def read_root():
    return {'cncsmart': __version__}


@app.get("/version")
def read_version():
    return read_root()


@app.post("/updates")
def post_updates(notification: EntityUpdateNotification,
                 fiware_service: Optional[str] = Header(None),
                 fiware_servicepath: Optional[str] = Header(None),
                 fiware_correlator: Optional[str] = Header(None)):
    ctx = FiwareContext(
        service=str(fiware_service), service_path=str(fiware_servicepath),
        correlator=str(fiware_correlator)
    )

    header = f"got entity updates for {ctx}:"
    logger.info(header + ''.join([f"{line}\n" for line in notification]))

    updated_machines = notification.filter_entities(PartProgramEntity)
    if updated_machines:
        process_update(ctx, updated_machines)

"""
Eats NGSI entities for breakfast.

Endpoint to process machine entity updates from Orion.

"""

from fipy.ngsi.headers import FiwareContext
from fipy.ngsi.orion import OrionClient
from fipy.ngsi.entity import FloatAttr
from typing import List

from loguru import logger

import cncsmart.config as config
from cncsmart.ngsy import PartProgramEntity, DurationEstimateEntity


def estimate(machine: PartProgramEntity) -> DurationEstimateEntity:
    xin = [len(machine.file_name.value),
           len(machine.json_data.value)]
    c_prediction = sum(xin)
    d_prediction = xin[0]

    # TODO what should the ID be? ideally there should be a bijection b/w
    #   machine IDs and estimate IDs...
    return DurationEstimateEntity(id=machine.id,
                                  cutting_duration=FloatAttr.new(c_prediction),
                                  duration=FloatAttr.new(d_prediction))


def process_update(ctx: FiwareContext, ms: List[PartProgramEntity]):
    header = f"going to process updates for {ctx}:\n"
    logger.info(header + ''.join([f"{line}\n" for line in ms]))

    estimates = [estimate(m) for m in ms]

    header = f"going to update context ({ctx}) with estimates:"
    logger.info(header + ''.join([f"{line}\n" for line in estimates]))

    orion = OrionClient(config.orion_base_url(), ctx)
    orion.upsert_entities(estimates)

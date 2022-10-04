"""
Roughnator NGSI v2 data types.

Examples
--------

>>> from fipy.ngsi.entity import *
>>> from cncsmart.ngsy import *

Filter machine entities out of an NGSI update notification.

>>> notification = EntityUpdateNotification(
...    data=[
...        {"id": "1", "type": "PartProgram", "file_name": {"value": "sample_1.json"}},
...        {"id": "2", "type": "NotMe", "file_name": {"value": "not_sample.json"}},
...        {"id": "3", "type": "PartProgram", "file_name": {"value": "sample_2.json"}}
...    ]
... )
>>> notification.filter_entities(PartProgramEntity)

"""

from fipy.ngsi.entity import BaseEntity, TextAttr, FloatAttr
from pydantic import BaseModel
from typing import Optional


class PartProgramEntity(BaseEntity):
    type = 'PartProgram'
    file_name: Optional[TextAttr]
    json_data: Optional[TextAttr]


class DurationEstimateEntity(BaseEntity):
    type = 'DurationEstimate'
    cutting_duration: FloatAttr
    duration: FloatAttr


class RawReading(BaseModel):
    file_name: Optional[str]
    json_data: Optional[str]

    def to_partprogram_entity(self, entity_id) -> PartProgramEntity:
        e = PartProgramEntity(id=entity_id)

        e.file_name = TextAttr.new(self.file_name)
        e.json_data = TextAttr.new(self.json_data)

        return e

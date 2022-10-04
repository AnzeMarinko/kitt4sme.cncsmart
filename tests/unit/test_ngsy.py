from cncsmart.ngsy import *


def test_float_attr_serialisation():
    want = '{"type": "Number", "value": 2.3}'
    got = FloatAttr.new(2.3).json()
    assert want == got


def test_readings_to_machine_entity_json():
    sensors_data = {"file_name": "sample.json", "json_data": "[]"}
    rr = RawReading(**sensors_data)

    machine1 = PartProgramEntity(id='').set_id_with_type_prefix('1')
    got = rr.to_partprogram_entity(entity_id=machine1.id).to_json()

    want = '{"id": "urn:ngsi-ld:PartProgram:1", "type": "PartProgram", ' \
           '"file_name": {"type": "Text", "value": "sample.json"}, ' \
           '"json_data": {"type": "Text", "value": "[]"}}'
    assert want == got

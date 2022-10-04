from tests.sim.runner import run


"""
Run this file and send new entities using command:

curl -v localhost:1026/orion/v2/entities?options=upsert -H 'Content-Type: application/json' -H 'fiware-service: csic' -d '
{
  "id": "urn:ngsi-ld:PartProgram:1",
  "type": "PartProgram",
  "file_name": {
    "type": "Text",
    "value": "sample.json"
  },
  "json_data": {
    "type": "Text",
    "value": "[{\"sample\": 1}]"
  }
}
'

"""


if __name__ == '__main__':
    run()

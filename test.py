from api_plugin.sams_science import SamsApi
import requests

payload = [{
    "sourceId": "dht22-humidity-DE-37139-[97834523476534654]",
    "values": [{
        "ts": '2018-10-10T10:16:00Z',
        "value": 75.5
    }]
}]

api = SamsApi()
api.api_call(payload)


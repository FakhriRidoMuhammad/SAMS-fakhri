from api_plugin.sams_science import SamsApi

api = SamsApi()

payload = [{
    "sourceId": "dht22-humidity-DE-37139-[97834523476534654]",
    "values": [{
        "ts": "2019-01-30T09:15:00Z",
        "value": 75.5
    }]
}]
test = [
    {
        'sourceId': 'dht22-temperature-Zy9Jtu1uXEIw94OP3cLMeDhSK5OAYXWT',
        'values': [{'value': 21.3, 'ts': '2019-01-30T09:15:00Z'}]
    },
    {
        'sourceId': 'dht22-humidity-Zy9Jtu1uXEIw94OP3cLMeDhSK5OAYXWT',
        'values': [{'value': 52.1, 'ts': '2019-01-30T09:15:00Z'}]
    },
    {
        'sourceId': 'Zy9Jtu1uXEIw94OP3cLMeDhSK5OAYXWT',
        'value': [{'value': 0.02, 'ts': '2019-01-30T09:15:00Z'}],
    },
    {
        'sourceId': 'dsb18b20-0-Zy9Jtu1uXEIw94OP3cLMeDhSK5OAYXWT',
        'value': [{'value': 20.937, 'ts': '2019-01-30T09:15:00Z'}]
    },
    {
        'sourceId': 'dsb18b20-1-Zy9Jtu1uXEIw94OP3cLMeDhSK5OAYXWT',
        'value': [{'value': 21.0, 'ts': '2019-01-30T09:15:00Z'}]
    }
]


test2 = [
    {
        'sourceId': 'dht22-temperature-Zy9Jtu1uXEIw94OP3cLMeDhSK5OAYXWT',
        'values': [{'ts': '2019-01-30T09:15:00Z', 'value': 21.3}]
    },
    {'sourceId': 'dht22-humidity-Zy9Jtu1uXEIw94OP3cLMeDhSK5OAYXWT',
     'values': [{'ts': '2019-01-30T09:15:00Z', 'value': 52.2}]
     },
    {'sourceId': 'Zy9Jtu1uXEIw94OP3cLMeDhSK5OAYXWT',
     'value': [{'ts': '2019-01-30T09:15:00Z', 'value': 0.02}]
     },
    {'sourceId': 'dsb18b20-0-Zy9Jtu1uXEIw94OP3cLMeDhSK5OAYXWT',
     'value': [{'ts': '2019-01-30T09:15:00Z', 'value': 20.937}]
     },
    {'sourceId': 'dsb18b20-1-Zy9Jtu1uXEIw94OP3cLMeDhSK5OAYXWT',
     'value': [{'ts': '2019-01-30T09:15:00Z', 'value': 20.937}]
     }
]


api.call(test2)

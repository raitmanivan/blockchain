transaction_schema = {
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "http://example.com/example.json",
    "type": "object",
    "title": "The root schema",
    "description": "The root schema comprises the entire JSON document.",
    "default": {},
    "examples": [
        {
            "sender": "Ivano",
            "recipient": "Vos",
            "amount": "1 BTC"
        }
    ],
    "required": [
        "sender",
        "recipient",
        "amount"
    ],
    "properties": {
        "sender": {
            "$id": "#/properties/sender",
            "type": "string",
            "title": "The sender schema",
            "description": "An explanation about the purpose of this instance.",
            "default": "",
            "examples": [
                "Ivano"
            ]
        },
        "recipient": {
            "$id": "#/properties/recipient",
            "type": "string",
            "title": "The recipient schema",
            "description": "An explanation about the purpose of this instance.",
            "default": "",
            "examples": [
                "Vos"
            ]
        },
        "amount": {
            "$id": "#/properties/amount",
            "type": "string",
            "title": "The amount schema",
            "description": "An explanation about the purpose of this instance.",
            "default": "",
            "examples": [
                "1 BTC"
            ]
        }
    },
    "additionalProperties": False
}

nodes_schema = {
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "http://example.com/example.json",
    "type": "object",
    "title": "The root schema",
    "description": "The root schema comprises the entire JSON document.",
    "default": {},
    "examples": [
        {
            "nodes": [
                "http://127.0.0.1:8001",
                "http://127.0.0.1:8002"
            ]
        }
    ],
    "required": [
        "nodes"
    ],
    "properties": {
        "nodes": {
            "$id": "#/properties/nodes",
            "type": "array",
            "title": "The nodes schema",
            "description": "An explanation about the purpose of this instance.",
            "default": [],
            "examples": [
                [
                    "http://127.0.0.1:8001",
                    "http://127.0.0.1:8002"
                ]
            ],
            "additionalItems": False,
            "items": {
                "$id": "#/properties/nodes/items",
                "anyOf": [
                    {
                        "$id": "#/properties/nodes/items/anyOf/0",
                        "type": "string",
                        "title": "The first anyOf schema",
                        "description": "An explanation about the purpose of this instance.",
                        "default": "",
                        "examples": [
                            "http://127.0.0.1:8001",
                            "http://127.0.0.1:8002"
                        ]
                    }
                ]
            }
        }
    },
    "additionalProperties": False
}
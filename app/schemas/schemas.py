transaction_schema = {
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "http://example.com/example.json",
    "type": "object",
    "title": "The root schema",
    "description": "The root schema comprises the entire JSON document.",
    "default": {},
    "examples": [
        {
            "author": "Ivan Raitman",
            "content": "test"
        }
    ],
    "required": [
        "author",
        "content"
    ],
    "properties": {
        "author": {
            "$id": "#/properties/author",
            "type": "string",
            "title": "The author schema",
            "description": "An explanation about the purpose of this instance.",
            "default": "",
            "examples": [
                "Ivan Raitman"
            ]
        },
        "content": {
            "$id": "#/properties/content",
            "type": "string",
            "title": "The content schema",
            "description": "An explanation about the purpose of this instance.",
            "default": "",
            "examples": [
                "test"
            ]
        }
    },
    "additionalProperties": False
}
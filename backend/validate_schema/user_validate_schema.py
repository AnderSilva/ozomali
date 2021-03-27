user_create_schema = {
    'type': 'object',
    'properties': {
        'nome': {'type': 'string',  "minLength": 4, "maxLength": 200},
        'login': {'type': 'string', "pattern": "[^@]+@[^@]+\.[^@]"},
        'senha': {'type': 'string', "minLength": 8, "maxLength": 20} # , "pattern": "^.*(?=.{8,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&+=*]).*$"}
    },
    'required': ['nome', 'login', 'senha']
}

user_auth_schema = {
    'type': 'object',
    'properties': {
        'login': {'type': 'string', "pattern": "[^@]+@[^@]+\.[^@]"},
        'senha': {'type': 'string',  "minLength": 1, "maxLength": 200}
    },
    'required': ['login', 'senha']
}

user_update_schema = {
    'type': 'object',
    'properties': {
        'id': {'type': 'number', "minimum": 1},
        'nome': {'type': 'string',  "minLength": 4, "maxLength": 200},
        'login': {'type': 'string', "pattern": "[^@]+@[^@]+\.[^@]"},
        'senha': {'type': 'string', "minLength": 8, "maxLength": 20} #, "pattern": "^.*(?=.{8,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&+=*]).*$"}
    },
    'required': ['id', 'nome', 'login', 'senha']
}
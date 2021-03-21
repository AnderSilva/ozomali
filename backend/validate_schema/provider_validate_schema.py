provider_create_schema = {
    'type': 'object',
    'properties': {
        'nome': {'type': 'string',  "minLength": 4, "maxLength": 200},
        'cnpj': {'type': 'string',  "minLength": 14, "maxLength": 14 },
        'cep': {'type': 'string', "minLength": 8, "maxLength": 8},
        'endereco': {'type': 'string',  "minLength": 4, "maxLength": 200},
        'numero': {'type': 'string',  "minLength": 1, "maxLength": 10},
        'complemento': {'type': 'string',  "maxLength": 10},
        'cidade': {'type': 'string',  "minLength": 1, "maxLength": 60},
        'estado': {'type': 'string',  "minLength": 2, "maxLength": 2}
    },
    'required': ['nome', 'cnpj', 'cep', 'endereco', 'numero', 'cidade', 'estado']
}

provider_update_schema = {
    'type': 'object',
    'properties': {
        'id': {'type': 'number', "minimum": 1},
        'nome': {'type': 'string',  "minLength": 4, "maxLength": 200},
        'cnpj': {'type': 'string',  "minLength": 14, "maxLength": 14},
        'cep': {'type': 'string', "minLength": 8, "maxLength": 8},
        'endereco': {'type': 'string',  "minLength": 4, "maxLength": 200},
        'numero': {'type': 'string',  "minLength": 1, "maxLength": 10},
        'complemento': {'type': 'string',  "maxLength": 10},
        'cidade': {'type': 'string',  "minLength": 1, "maxLength": 60},
        'estado': {'type': 'string',  "minLength": 2, "maxLength": 2}
    },
    'required': ['id', 'nome', 'cnpj', 'cep', 'endereco', 'numero', 'cidade', 'estado']
}
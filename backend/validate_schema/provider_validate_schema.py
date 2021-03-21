provider_create_schema = {
    'type': 'object',
    'properties': {
        'nome': {'type': 'string',  "minLength": 4, "maxLength": 200},
        'cnpj': {'type': 'string',  "minLength": 18, "maxLength": 18, "pattern": "^\d{2}\.\d{3}\.\d{3}\/\d{4}\-\d{2}$"},
        'cep': {'type': 'number', "minimum": 1000, "maximum": 99999999},
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
        'cnpj': {'type': 'string',  "minLength": 18, "maxLength": 18, "pattern": "^\d{2}\.\d{3}\.\d{3}\/\d{4}\-\d{2}$"},
        'cep': {'type': 'number', "minimum": 1000, "maximum": 99999999},
        'endereco': {'type': 'string',  "minLength": 4, "maxLength": 200},
        'numero': {'type': 'string',  "minLength": 1, "maxLength": 10},
        'complemento': {'type': 'string',  "maxLength": 10},
        'cidade': {'type': 'string',  "minLength": 1, "maxLength": 60},
        'estado': {'type': 'string',  "minLength": 2, "maxLength": 2}
    },
    'required': ['id', 'nome', 'cnpj', 'cep', 'endereco', 'numero', 'cidade', 'estado']
}
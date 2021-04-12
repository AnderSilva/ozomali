product_create_schema = {
    'type': 'object',
    'properties': {
        'nome': {'type': 'string',  "minLength": 2, "maxLength": 200},
        'preco_custo': {'type': 'number', "minimum": 0.01, "maximum": 9999999.99},
        'preco_venda': {'type': 'number', "minimum": 0.01, "maximum": 9999999.99},
        'quantidade': {'type': 'number', "minimum": 0, "maximum": 999999999999999}
    },
    'required': ['nome', 'preco_custo', 'preco_venda', 'quantidade']
}

product_update_schema = {
    'type': 'object',
    'properties': {
        'id': {'type': 'number', "minimum": 1},
        'nome': {'type': 'string',  "minLength": 2, "maxLength": 200},
        'preco_custo': {'type': 'number', "minimum": 0.01, "maximum": 9999999.99},
        'preco_venda': {'type': 'number', "minimum": 0.01, "maximum": 9999999.99},
        'quantidade': {'type': 'number', "minimum": 0, "maximum": 999999999999999}
    },
    'required': ['id', 'nome', 'preco_custo', 'preco_venda', 'quantidade']
}
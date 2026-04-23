def validate_product_payload(payload, partial=False):
    if not isinstance(payload, dict):
        return 'JSON body must be an object'
        
    required_fields = ['name', 'price']
    if not partial:
        for field in required_fields:
            if field not in payload:
                return f'Missing required field: {field}'
                
    if 'name' in payload and (not isinstance(payload['name'], str) or not payload['name'].strip()):
        return 'name must be a non-empty string'
        
    if 'price' in payload and not isinstance(payload['price'], (int, float)):
        return 'price must be a number'
        
    if 'in_stock' in payload and not isinstance(payload['in_stock'], bool):
        return 'in_stock must be a boolean'
        
    if 'description' in payload and not isinstance(payload['description'], str):
        return 'description must be a string'
        
    return None
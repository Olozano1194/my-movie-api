#Este es el archivo para generar tokens en python
#instalamos jwt en la terminal, pip install pyjwt


from jwt import encode, decode

#creamos un diccionario con los datos que queremos guardar en el token

def create_token(data: dict) -> str:
    token: str =encode(payload=data, key='my_secrete_key', algorithm='HS256')
    return token

def validate_token(token: str) -> dict:
    data:dict = decode(token, key='my_secrete_key', algorithms=['HS256'])
    return data
    
    
    
    
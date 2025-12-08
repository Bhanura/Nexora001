"""Remove BOM from .env file"""
with open('.env', 'r', encoding='utf-8-sig') as f:
    content = f.read()
    
with open('.env', 'w', encoding='utf-8') as f:
    f.write(content)
    
print('BOM removed from .env file successfully!')

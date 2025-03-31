import requests

response = requests.get('https://swapi.dev/api/people/17/')
print(response.status_code)
print(response.json())
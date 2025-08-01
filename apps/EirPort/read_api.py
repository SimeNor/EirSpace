import requests

url = "http://localhost:8080/"

payload = {}
headers = {"accept": "application/json"}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)

import requests

identifier = "food_bowl"

# Read scale
response = requests.get(
    f"http://localhost:8001/read/{identifier}?unit=kg",
    headers={"accept": "application/json"},
)

print(response.json())

import requests


def read_scale(identifier: str) -> None:
    response = requests.get(
        f"http://localhost:8001/read/{identifier}?unit=kg",
        headers={"accept": "application/json"},
    )
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to read scale: {response.status_code}")

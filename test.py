import requests

url = "https://payload.vextapp.com/hook/PYAYLLWJ82/catch/anhtt9x"

payload = { "payload": "what is machine learning" }
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "Apikey": "Api-Key "
}

response = requests.post(url, json=payload, headers=headers)

print(response.text)

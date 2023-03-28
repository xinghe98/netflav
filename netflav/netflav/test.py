import requests

url = "https://streamtape.to/e/vWayQgQqQyI4vDZ"

response = requests.request("GET", url)

print(response.text)

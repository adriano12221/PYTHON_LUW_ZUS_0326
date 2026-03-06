import requests

url = "https://jsonplaceholder.typicode.com/posts"

response = requests.get(url)
print(f"status code: {response.status_code}")

data = response.json()

for post in data[:5]:
    print(post["title"])

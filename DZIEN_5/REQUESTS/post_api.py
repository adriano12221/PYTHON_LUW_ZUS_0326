import requests

url = "https://jsonplaceholder.typicode.com/posts"
data = {"title": "Python AI", "body": "przykładowy post", "userId": 1}

response = requests.post(url, json=data)
print(f"status code: {response.status_code}")
print(response.json())

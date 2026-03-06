import requests

users_url = "https://jsonplaceholder.typicode.com/users"
posts_url = "https://jsonplaceholder.typicode.com/posts"

users = requests.get(users_url).json()
posts = requests.get(posts_url).json()

for user in users:
    user_post = [p for p in posts if p["userId"] == user["id"]]
    print(user["name"],"->" ,len(user_post),"posts")

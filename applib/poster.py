import requests

WP_URL = "https://allfootballnews.com.ng/wp-json/wp/v2/posts"
username = "peter"
password = "9F2h xuFH JQDc ujyd YsuS jQDh"

data = {
    "title": "My test post",
    "content": "Post body",
    "status": "draft"
}

rsp = requests.post(WP_URL, json=data, auth=(username, password))

if rsp.status_code == "201":
    print("Post made successfully")
    print(rsp.json()["link"])
else:
    print("Failed to create the post")
    print(rsp.json())


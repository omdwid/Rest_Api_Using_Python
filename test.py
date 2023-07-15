import requests
import json

BASE = "http://127.0.0.1:5000/"

headers = {'Content-Type': 'application/json'}
data = [ 
            json.dumps({'likes':2000, 'name':'My First Video', 'views':100000}),
            json.dumps({'likes':3000, 'name':'My Second Video', 'views':126000}),
            json.dumps({'likes':4000, 'name':'My Third Video', 'views':138000}),
            json.dumps({'likes':5000, 'name':'My Fourth Video', 'views':149000}),
            json.dumps({'likes':6000, 'name':'My Fifth Video', 'views':156000})
        ]

for i, d in enumerate(data):
    print(requests.put(BASE + f"video/{10+i}", d, headers=headers).json())

input()
data = json.dumps(
    {
        'views': 3434,
        'likes': 2222,
        'name': "Hey! this is the video after the updation"
    }
)
response = requests.patch(BASE+'video/10', data, headers=headers)
print(response.json())

input()
response = requests.get(BASE + 'video/10')
print(response.json())

# print(requests.post(BASE + "helloworld").json())
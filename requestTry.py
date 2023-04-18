import requests

BASE = "http://192.168.1.221:8000"
response=requests.post(BASE+"/api/login" ,json=
                              {"username":"rashid01",
                               "password":"123"
                        })
print(response.json())
import requests
from flask_login import current_user

s = requests.Session()
BASE = "http://192.168.1.6:8000"
response=s.post(BASE+"/api/login" ,json=
                              {"username":"rashid01",
                               "password":"123"
                        })
print(response.json())
#print(f"current_user_id:{current_user.id}")

response=s.get(BASE+"/api/Course" ,json=
                              {"course_names":["MA 123"],
                               "semesters":["Fall 2023"],
                                "status": [1]
                                })


print(response.json())
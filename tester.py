import json
import requests

# url = "http://localhost:5000"  # if you want to test local
url = "http://diabetes-manager-app.herokuapp.com"  # if you want to test deployed

val = [{"id": 1,
        "timestamp": "2000-10-10 7:10",
        "code": 33,
        "value": 10.0,
        "user_id": 1},
       {"id": 2,
        "timestamp": "2000-10-10 9:10",
        "code": 59,
        "value": 100.0,
        "user_id": 1},
       {"id": 3,
        "timestamp": "2000-10-10 11:10",
        "code": 60,
        "value": 180.0,
        "user_id": 1},
       {"id": 4,
        "timestamp": "2000-10-10 19:10",
        "code": 63,
        "value": 250.0,
        "user_id": 1},
       {"id": 5,
        "timestamp": "2000-10-10 22:10",
        "code": 57,
        "value": 300.0,
        "user_id": 1},
       {"id": 6,
        "timestamp": "2000-10-11 9:10",
        "code": 33,
        "value": 5.0,
        "user_id": 1},
       {"id": 7,
        "timestamp": "2000-10-11 10:10",
        "code": 59,
        "value": 150.0,
        "user_id": 1},
       {"id": 8,
        "timestamp": "2000-10-11 13:10",
        "code": 60,
        "value": 200.0,
        "user_id": 1},
       {"id": 9,
        "timestamp": "2000-10-11 18:10",
        "code": 63,
        "value": 100.0,
        "user_id": 1},
       {"id": 10,
        "timestamp": "2000-10-11 00:10",
        "code": 57,
        "value": 180.0,
        "user_id": 1},
       {"id": 11,
        "timestamp": "2000-10-12 8:10",
        "code": 33,
        "value": 7.0,
        "user_id": 1},
       {"id": 12,
        "timestamp": "2000-10-12 8:10",
        "code": 59,
        "value": 90.0,
        "user_id": 1},
       {"id": 13,
        "timestamp": "2000-10-12 12:10",
        "code": 60,
        "value": 130.0,
        "user_id": 1},
       {"id": 14,
        "timestamp": "2000-10-12 20:10",
        "code": 63,
        "value": 150.0,
        "user_id": 1},
       {"id": 15,
        "timestamp": "2000-10-12 23:10",
        "code": 57,
        "value": 200.0,
        "user_id": 1}]


# you'll get a 200 response if the keys align, and something bad if the keys don't align.

if __name__ == '__main__':
    r_success = requests.post(url, data=json.dumps(val))
    print(
        f"Request responded: {r_success}.\nResponse was\n{r_success.json()}")
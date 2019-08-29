import json
import pickle
import numpy as np
from datetime import *
from flask import Flask, request, jsonify

# def ValuePredictor(to_predict_list):
#     """Predict function"""
#     to_predict = np.array(to_predict_list).reshape(1, -1)
#     loaded_model = pickle.load(open("diabetes_model.pkl", 'rb'))
#     result = loaded_model.predict(to_predict)
#     return result[0]


app = Flask(__name__)
@app.route("/", methods=['POST'])
def address():
    '''Takes a list of json dictionaries and return average value within
    each time frame'''

    # receive input
    inputs = request.get_json(force=True)

    morning_val = 0
    lunch_val = 0
    dinner_val = 0
    bed_val = 0
    morning_num = 0
    lunch_num = 0
    dinner_num = 0
    bed_num = 0

    # get data from json
    for x in inputs:
        timestamp = x['timestamp']
        code = x['code']
        value = x['value']

        # validate input
        assert isinstance(timestamp, str)
        assert isinstance(code, int)
        assert isinstance(value, float)

        time = datetime.strptime(timestamp, '%Y-%m-%d %H:%M')
        hour = time.hour
        if 4 <= hour <= 10:
            morning_val += value
            morning_num += 1
        elif 11 <= hour <= 15:
            lunch_val += value
            lunch_num += 1
        elif 16 <= hour <= 21:
            dinner_val += value
            dinner_num += 1
        else:
            bed_val += value
            bed_num += 1

    # unpickle
    # with open('model.pickle', 'rb') as mod:
    #     model = pickle.load(mod)

    # predict
    # output = model.predict(timestamp, code, value)

    # use a dictionary to format output for json
    out = {'Morning blood glucose level': int(morning_val//morning_num),
           'Noon blood glucose level': int(lunch_val//lunch_num),
           'Evening blood glucose level': int(dinner_val//dinner_num),
           'Night blood glucose level': int(bed_val//bed_num)}

    # give output to sender.
    return app.response_class(
        response=json.dumps(out),
        status=200,
        mimetype='application/json'
    )


if __name__ == '__main__':
    app.run(port=5000, debug=True)

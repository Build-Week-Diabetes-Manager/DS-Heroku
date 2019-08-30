import json
import pickle
import numpy as np
from datetime import *
from flask import Flask, request, jsonify


# def ValuePredictor(to_predict_list):
#     """Predict function"""
#     to_predict = np.array(to_predict_list).reshape(1, -1)
#     loaded_model = pickle.load(open("model.pkl", 'rb'))
#     result = loaded_model.predict(to_predict)
#     return result


app = Flask(__name__)
@app.route("/", methods=['POST'])
def address():
    '''Takes a list of json dictionaries and return prediction values within
    each time frame'''

    # receive input
    inputs = request.get_json(force=True)

    total_value = 0
    len_glucose = 0
    # get data from json
    for x in inputs:
        timestamp = x['timestamp']
        code = x['code']
        value = x['value']

        # validate input
        assert isinstance(timestamp, str)
        assert isinstance(code, int)

        time = datetime.strptime(timestamp, '%Y-%m-%d %H:%M')
        next_day = time + timedelta(days=1)

        if code in range(57, 64):
            total_value += value
            glucose_val = value
            len_glucose += 1

    date = next_day.year, next_day.month, next_day.day
    pre_breakfast_time = f'{date[0]}-{date[1]}-{date[2]} 07:23'
    pre_breakfast_time = datetime.strptime(
        pre_breakfast_time, '%Y-%m-%d %H:%M')
    pre_breakfast_min = (pre_breakfast_time - time).total_seconds()/60
    post_breakfast_time = f'{date[0]}-{date[1]}-{date[2]} 09:56'
    post_breakfast_time = datetime.strptime(
        post_breakfast_time, '%Y-%m-%d %H:%M')
    post_breakfast_min = (post_breakfast_time -
                          pre_breakfast_time).total_seconds()/60
    pre_lunch_time = f'{date[0]}-{date[1]}-{date[2]} 12:09'
    pre_lunch_time = datetime.strptime(pre_lunch_time, '%Y-%m-%d %H:%M')
    pre_lunch_min = (pre_lunch_time - post_breakfast_time).total_seconds()/60
    post_lunch_time = f'{date[0]}-{date[1]}-{date[2]} 14:20'
    post_lunch_time = datetime.strptime(post_lunch_time, '%Y-%m-%d %H:%M')
    post_lunch_min = (post_lunch_time - post_breakfast_time).total_seconds()/60
    pre_supper_time = f'{date[0]}-{date[1]}-{date[2]} 17:52'
    pre_supper_time = datetime.strptime(pre_supper_time, '%Y-%m-%d %H:%M')
    pre_supper_min = (pre_supper_time - post_lunch_time).total_seconds()/60
    post_supper_time = f'{date[0]}-{date[1]}-{date[2]} 19:11'
    post_supper_time = datetime.strptime(post_supper_time, '%Y-%m-%d %H:%M')
    post_supper_min = (post_supper_time - pre_supper_time).total_seconds()/60

    # unpickle
    with open('model.pkl', 'rb') as mod:
        # [predict code,
        # given last glucose measurement,
        # known avg measurement(all),
        # minutes since last measurement]
        model = pickle.load(mod)

    avg_values = total_value/len_glucose

    # predict
    pre_breakfast = model.predict(
        [[58, glucose_val, avg_values, pre_breakfast_min]])
    post_breakfast = model.predict(
        [[59, pre_breakfast[0], avg_values, post_breakfast_min]])
    pre_lunch = model.predict(
        [[60, post_breakfast[0], avg_values, pre_lunch_min]])
    post_lunch = model.predict(
        [[61, pre_lunch[0], avg_values, post_lunch_min]])
    pre_supper = model.predict(
        [[62, post_lunch[0], avg_values, pre_supper_min]])
    post_supper = model.predict(
        [[63, pre_supper[0], avg_values, post_supper_min]])

    # use a dictionary to format output for json
    out = {'Pre-breakfast 07:23AM measurement': pre_breakfast[0],
           'Post-breakfast 09:56AM measurement': post_breakfast[0],
           'Pre-lunch 12:09PM measurement': pre_lunch[0],
           'Post-lunch 14:20PM measurement': post_lunch[0],
           'Pre-supper 17:52PM measurement': pre_supper[0],
           'Post-supper 19:11PM measurement': post_supper[0]}

    # give output to sender.
    return app.response_class(
        response=json.dumps(out),
        status=200,
        mimetype='application/json'
    )


if __name__ == '__main__':
    app.run(port=5000, debug=True)

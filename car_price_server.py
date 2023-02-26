from flask import Flask,jsonify,request
import json
import pickle
import numpy as np

app = Flask(__name__)

__data_columns = None
__car_model = None
__type = None
__fuel = None
__city = None
__model = None


@app.route('/get_all_model_details')
def get_all_model_details():
    load_artifacts()
    response = jsonify({
        'car_model': __car_model,
        'city': __city,
        'fuel': __fuel,
        'type': __type,
    }
    )
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

def load_artifacts():
    global __data_columns
    global __city
    global __fuel
    global __type
    global __car_model
    global __model
    with open('./artifacts/columns.json', 'r') as f:
        __data_columns = json.load(f)['data_columns']
        __car_model = __data_columns[3:47]
        __city = __data_columns[47:58]
        __fuel = __data_columns[58:60]
        __type = __data_columns[60:62]
    with open('./artifacts/Used_car_price_prediction.pickle','rb') as f:
        __model = pickle.load(f)



@app.route('/car_price_prediction', methods=['POST'])
def car_price_prediction():
    kms = int(request.form['kms'])
    owners = int(request.form['owner'])
    car_life = int(request.form['car_life'])
    car_model = request.form['car_model']
    type = request.form['type']
    fuel = request.form['fuel']
    city = request.form['city']
    load_artifacts()



    try:
        car_model_index = __data_columns.index(car_model.lower())
    except:
        car_model_index = -1

    try:
        type_index = __data_columns.index(type.lower())
    except:
        type_index = -1

    try:
        fuel_index = __data_columns.index(fuel.lower())
    except:
        fuel_index = -1

    try:
        city_index = __data_columns.index(city.lower())
    except:
        city_index = -1

    x = np.zeros(len(__data_columns))
    x[0] = kms
    x[1] = owners
    x[2] = car_life

    if car_model_index >= 0:
        x[car_model_index] = 1
    if type_index >= 0:
        x[type_index] = 1
    if fuel_index >= 0:
        x[fuel_index] = 1
    if city_index >= 0:
        x[city_index] = 1

    response = jsonify({
        'estimated_car_price': round(__model.predict([x])[0],2)
    }
    )
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


if __name__ == '__main__':
    app.run()


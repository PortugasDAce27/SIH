import requests
from flask import *
import weatherkey
import pickle
import numpy as np

app = Flask(__name__)

model = 'RandomForest.pkl'
model = pickle.load(open(model,'rb'))


@app.route('/login', methods=['POST'])
def login():
    print(request.get_json())
    value = {
        "N" : request.get_json().get('n'),
        "P": request.get_json().get('p'),
        "K": request.get_json().get('k'),
        "Ph" : request.get_json().get('Ph'),
        "Rain" : request.get_json().get('Rain'),
        "State": request.get_json().get('State'),
        "City" : request.get_json().get('City')

    }
    N = request.get_json().get('n')
    P = request.get_json().get('p')
    K = request.get_json().get('k')
    Ph = request.get_json().get('Ph')
    Rain = request.get_json().get('Rain')
    State = request.get_json().get('State')
    City = request.get_json().get('City')
    print(fetch(City))
    if fetch(City) != None:
        temperature, humidity = fetch(City)
        data = np.array([[N, P, K, temperature, humidity, Ph, Rain]])
        my_prediction = model.predict(data)
        final_prediction = my_prediction[0]
        print(final_prediction)
        return jsonify({"result":final_prediction})

    # Dictionary to JSON Object using dumps() method
    # Return JSON Object
    return json.dumps(value)


#   return request["nm"];




def fetch(City):

    api_key  = weatherkey.weather_api_key
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + api_key + "&q=" + City

    response = requests.get(complete_url)
    a = response.json()

    if a["cod"] != "404":
        b = a["main"]

        temperature = round((b["temp"] - 273.15), 2)
        humidity = b["humidity"]

        return temperature, humidity
    else:
        return None


# @app.route("/pre" , methods = ['POST'])
# def prediction():
#     if request.method =='POST':
#         val = login.value
#         N = val["N"]
#         P =val["P"]
#         K = val["K"]
#         Ph = val["Ph"]
#         Rain = val["Rain"]
#         State = val["State"]
#         City = val["City"]
#
#         if fetch(City) != None:
#
#             temperature, humidity = fetch(City)
#             data = np.array([[N, P, K, temperature, humidity, Ph, Rain]])
#             my_prediction = model.predict(data)
#             final_prediction = my_prediction[0]
#             print(final_prediction)
#             return jsonify(final_prediction)
#






if __name__ == '__main__':
    app.run(debug=True)
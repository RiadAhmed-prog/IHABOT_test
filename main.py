
import requests
import cv2
import time
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import classification_report,f1_score,confusion_matrix
from sklearn.ensemble import RandomForestClassifier

import pickle
# api-endpoint
get_URL = "http://127.0.0.1:8000/api/get/"

put_URL = "http://127.0.0.1:8000/api/update/6/"


r = requests.get(url=get_URL)
data = r.json()

def take_temp():
    temp=0

    for i in range(10):
        temp=98
        time.sleep(1)
    return temp


def take_pressure():
    s_bp,d_bp,pul=0,0,0

    for i in range(5):
        s_bp,d_bp,pul=60,140,75
        time.sleep(1)
    return s_bp,d_bp,pul


def take_oxy():
    oxy= 0
    for i in range(5):
        oxy=96
        time.sleep(1)

    return oxy


def take_exercise():
    pred= 0

    for i in range(10):
        pred=i
        time.sleep(1)
    return pred

def health_check(temp, pulse, resp, ss_bp, d_bp, ox):
    pred= 0
    score_names = ["Normal", "Mild", "Severe", "Critical"]
    with open('scalar.pkl', 'rb') as f:
        scalar = pickle.load(f)
        f.close()

    with open('health_model.pkl', 'rb') as f:
        model = pickle.load(f)
        f.close()

    inp = np.array([[temp, pulse, resp, ss_bp, d_bp, ox]])
    inp = pd.DataFrame(inp)
    inp_x = scalar.transform(inp)

    pred = model.predict(inp_x)
    print(score_names[pred[0]])
    return score_names[pred[0]]


all_flags= [
    data['temperature_flag'],
    data['bp_flag'],
    data['oxygen_saturation_flag'],
    data['exercise_flag'],
    data['health_flag']
]

while True:


    if 0 in all_flags or 4 in all_flags:

        try:

            instrument_id= all_flags.index(0)
        except:
            instrument_id = all_flags.index(4)


        if instrument_id ==0:
            data["temperature_flag"]=1
            print("temperature is taking")
            r = requests.put(url=put_URL, data=data)
            temp= take_temp()

            while temp <1:
                data["temperature_flag"] = 4
                r = requests.put(url=put_URL, data=data)
                temp = take_temp()
            data["temperature_flag"] = 2
            data["temperature"] = temp
            r = requests.put(url=put_URL, data=data)
            print("temperature done")

        elif instrument_id == 1:
            data["bp_flag"] = 1
            r = requests.put(url=put_URL, data=data)
            print("BP is taking")
            s_bp,d_bp,pul = take_pressure()
            while 0 in [s_bp,d_bp,pul]:
                data["bp_flag"] = 4
                r = requests.put(url=put_URL, data=data)
                s_bp, d_bp, pul = take_pressure()
            data["bp_flag"] = 2

            data["systolic_bp"]=s_bp
            data["diastolic_bp"] = d_bp
            data["pulse_rate"] = pul

            r = requests.put(url=put_URL, data=data)
            print("BP Done")

        elif instrument_id == 2:
            data["oxygen_saturation_flag"] = 1
            r = requests.put(url=put_URL, data=data)
            print("OX is taking")
            oxy = take_oxy()

            while oxy <1:
                data["oxygen_saturation_flag"] = 4
                r = requests.put(url=put_URL, data=data)
                oxy = take_oxy()
            data["oxygen_saturation_flag"] = 2

            data["oxygen_saturation"]=oxy

            r = requests.put(url=put_URL, data=data)
            print("OX Done")

        elif instrument_id == 3:
            data["exercise_flag"] = 1
            r = requests.put(url=put_URL, data=data)
            print("pred is taking")
            pred = take_exercise()

            while pred ==0:
                data["exercise_flag"] = 4
                r = requests.put(url=put_URL, data=data)
                pred = take_exercise()

            data["exercise_flag"] = 2
            data["exercise_prediction"]=pred
            r = requests.put(url=put_URL, data=data)
            print("pred Done")

        elif instrument_id ==4:
            # input temp, pulse, resp, ss_bp, d_bp, ox
            data["health_flag"]=1
            print("Health checking")
            r = requests.put(url=put_URL, data=data)
            h_score= health_check(data["temperature"],data["pulse_rate"],80,data["systolic_bp"],data["diastolic_bp"],data["oxygen_saturation"])

            while h_score ==0:
                data["health_flag"] = 4
                r = requests.put(url=put_URL, data=data)
                h_score= health_check(data["temperature"],data["pulse_rate"],80,data["systolic_bp"],data["diastolic_bp"],data["oxygen_saturation"])
            data["health_flag"] = 2
            data["health_prediction"] = h_score
            r = requests.put(url=put_URL, data=data)
            print("health_prediction done")


    else:
        print("All data have taken..")
    r = requests.get(url=get_URL)
    data = r.json()
    all_flags = [
        data['temperature_flag'],
        data['bp_flag'],
        data['oxygen_saturation_flag'],
        data['exercise_flag'],
        data['health_flag']
    ]

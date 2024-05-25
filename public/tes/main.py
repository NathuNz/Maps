from flask import Flask, request, jsonify
import pickle
import psycopg2
from psycopg2.extras import RealDictCursor
import numpy as np
import pandas as pd
import datetime
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.model_selection import train_test_split
from fwi import FWICLASS
from elmz import elm

app = Flask(__name__)

def format_date(date):
        return date.strftime('%Y-%m-%d')

with open('modelsz.pkl', 'rb') as file:
    model = pickle.load(file)

connection = psycopg2.connect(user="ffp-indonesia",
                              password="forestfire123",
                              host="34.101.120.221",
                              port="5432",
                              database="ffp-indonesia",
                              cursor_factory=RealDictCursor)

@app.route('/forecast/temperature', methods=['GET'])
def forecast_temp():
    selected_provinsi = request.args.get('provinsi')
    selected_kabupaten = request.args.get('kabupaten')
    cursor = connection.cursor()
    cursor.execute("SELECT provinsi, date, windspeed, humidity, rainfall, temperature FROM posts WHERE kabupaten = %s AND provinsi = %s", (selected_kabupaten, selected_provinsi))
    data = cursor.fetchall()
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')

    # Features and target variable
    train_data = df[df['date'] <= '2020-12-31']
    test_data = df[df['date'] > '2020-12-31']

    X_train = train_data[['humidity', 'windspeed', 'rainfall']].values
    y_train = train_data[['temperature']].values
    X_test = test_data[['humidity', 'windspeed', 'rainfall']].values
    y_test = test_data[['temperature']].values

    dates = test_data['date'].tolist()

    scaler_X = StandardScaler()
    X_train_scaled = scaler_X.fit_transform(X_train)
    X_test_scaled = scaler_X.transform(X_test)

    scaler_y = StandardScaler()
    y_train_scaled = scaler_y.fit_transform(y_train)
    y_test_scaled = scaler_y.transform(y_test)

    elm(hidden_units=20, activation_function='sigmoid', x=X_train_scaled, y=y_train_scaled, random_type='normal')
    model.fit()

    y_pred_scaled = model.predict(X_test_scaled)
    y_pred = scaler_y.inverse_transform(y_pred_scaled)
    y_test = scaler_y.inverse_transform(y_test_scaled)

    # Mengasumsikan 'df' adalah DataFrame Anda dan 'Tanggal' adalah kolom tanggal
    last_date = df['date'].max()

    # Menghasilkan rangkaian tanggal untuk 90 hari ke depan
    future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=num_days)

    # Mengambil sampel acak dari fitur kelembapan, curah hujan, dan kecepatan angin 
    num_days = 20
    sampled_humidity = np.random.choice(df['Temperature'], num_days, replace=True)
    sampled_rainfall = np.random.choice(df['Windspeed'], num_days, replace=True)
    sampled_windspeed = np.random.choice(df['Rainfall'], num_days, replace=True)

    # Membuat DataFrame baru dari fitur yang disampling
    forecast_features = pd.DataFrame({
        'date': future_dates,  # Menambahkan kolom tanggal
        'Temperature': sampled_humidity,
        'Windspeed': sampled_rainfall,
        'Rainfall': sampled_windspeed
    })

    # Menormalisasi fitur menggunakan scaler yang sudah ada
    forecast_features_scaled = scaler.transform(forecast_features[['Temperature', 'Windspeed', 'Rainfall']])

    # Melakukan prediksi menggunakan model ELM
    predicted_forecast_temperatures = model.predict(forecast_features_scaled)

    # Mendenormalisasi prediksi suhu
    predicted_forecast_temperatures_denormalized = scaler_target.inverse_transform(predicted_forecast_temperatures)

    # Menambahkan prediksi suhu ke DataFrame
    forecast_features['Humidity'] = predicted_forecast_temperatures_denormalized

    # Menampilkan hasil dengan tanggal dan prediksi suhu
    forecast_features[['Tanggal', 'Humidity']].round(1)

@app.route('/train/temperature', methods=['GET'])
def train_temp():
    selected_provinsi = request.args.get('provinsi')
    selected_kabupaten = request.args.get('kabupaten')
    cursor = connection.cursor()
    cursor.execute("SELECT provinsi, date, windspeed, humidity, rainfall, temperature FROM posts WHERE kabupaten = %s AND provinsi = %s", (selected_kabupaten, selected_provinsi))
    data = cursor.fetchall()

    if not data:
        return jsonify({"error": "No data found"}), 404

    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')

    # Features and target variable
    train_data = df[df['date'] <= '2020-12-31']
    test_data = df[df['date'] > '2020-12-31']

    X_train = train_data[['humidity', 'windspeed', 'rainfall']].values
    y_train = train_data[['temperature']].values
    X_test = test_data[['humidity', 'windspeed', 'rainfall']].values
    y_test = test_data[['temperature']].values

    dates = test_data['date'].tolist()

    scaler_X = StandardScaler()
    X_train_scaled = scaler_X.fit_transform(X_train)
    X_test_scaled = scaler_X.transform(X_test)

    scaler_y = StandardScaler()
    y_train_scaled = scaler_y.fit_transform(y_train)
    y_test_scaled = scaler_y.transform(y_test)

    elm(hidden_units=20, activation_function='sigmoid', x=X_train_scaled, y=y_train_scaled, random_type='normal')
    model.fit()

    y_pred_scaled = model.predict(X_test_scaled)
    y_pred = scaler_y.inverse_transform(y_pred_scaled)
    y_test = scaler_y.inverse_transform(y_test_scaled)

    result_df = pd.DataFrame({
        'date': dates,
        'Actual Temperature': y_test.flatten(),
        'Predicted Temperature': y_pred.flatten()
    })

    response = {
        'result': result_df.to_dict(orient='records')
    }
    return jsonify(response)

@app.route('/train/humidity', methods=['GET'])
def train_humid():
    selected_provinsi = request.args.get('provinsi')
    selected_kabupaten = request.args.get('kabupaten')
    cursor = connection.cursor()
    cursor.execute("SELECT provinsi, date, windspeed, humidity, rainfall, temperature FROM posts WHERE kabupaten = %s AND provinsi = %s", (selected_kabupaten, selected_provinsi))
    data = cursor.fetchall()

    if not data:
        return jsonify({"error": "No data found"}), 404

    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')

    # Features and target variable
    train_data = df[df['date'] <= '2020-12-31']
    test_data = df[df['date'] > '2020-12-31']

    X_train = train_data[['temperature', 'windspeed', 'rainfall']].values
    y_train = train_data[['humidity']].values
    X_test = test_data[['temperature', 'windspeed', 'rainfall']].values
    y_test = test_data[['humidity']].values

    dates = test_data['date'].tolist()

    scaler_X = StandardScaler()
    X_train_scaled = scaler_X.fit_transform(X_train)
    X_test_scaled = scaler_X.transform(X_test)

    scaler_y = StandardScaler()
    y_train_scaled = scaler_y.fit_transform(y_train)
    y_test_scaled = scaler_y.transform(y_test)

    elm(hidden_units=20, activation_function='sigmoid', x=X_train_scaled, y=y_train_scaled, random_type='normal')
    model.fit()

    y_pred_scaled = model.predict(X_test_scaled)
    y_pred = scaler_y.inverse_transform(y_pred_scaled)
    y_test = scaler_y.inverse_transform(y_test_scaled)

    result_df = pd.DataFrame({
        'date': dates,
        'Actual Humidity': y_test.flatten(),
        'Predicted Humidity': y_pred.flatten()
    })

    response = {
        'result': result_df.to_dict(orient='records')
    }
    return jsonify(response)

@app.route('/train/rainfall', methods=['GET'])
def train_rain():
    selected_provinsi = request.args.get('provinsi')
    selected_kabupaten = request.args.get('kabupaten')
    cursor = connection.cursor()
    cursor.execute("SELECT provinsi, date, windspeed, humidity, rainfall, temperature FROM posts WHERE kabupaten = %s AND provinsi = %s", (selected_kabupaten, selected_provinsi))
    data = cursor.fetchall()

    if not data:
        return jsonify({"error": "No data found"}), 404

    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')

    # Features and target variable
    train_data = df[df['date'] <= '2020-12-31']
    test_data = df[df['date'] > '2020-12-31']

    X_train = train_data[['temperature', 'humidity', 'windspeed']].values
    y_train = train_data[['rainfall']].values
    X_test = test_data[['temperature', 'humidity', 'windspeed']].values
    y_test = test_data[['rainfall']].values

    dates = test_data['date'].tolist()

    scaler_X = StandardScaler()
    X_train_scaled = scaler_X.fit_transform(X_train)
    X_test_scaled = scaler_X.transform(X_test)

    scaler_y = StandardScaler()
    y_train_scaled = scaler_y.fit_transform(y_train)
    y_test_scaled = scaler_y.transform(y_test)

    elm(hidden_units=20, activation_function='sigmoid', x=X_train_scaled, y=y_train_scaled, random_type='normal')
    model.fit()

    y_pred_scaled = model.predict(X_test_scaled)
    y_pred = scaler_y.inverse_transform(y_pred_scaled)
    y_test = scaler_y.inverse_transform(y_test_scaled)

    result_df = pd.DataFrame({
        'date': dates,
        'Actual Rainfall': y_test.flatten(),
        'Predicted Rainfall': y_pred.flatten()
    })

    response = {
        'result': result_df.to_dict(orient='records')
    }
    return jsonify(response)

@app.route('/train/windspeed', methods=['GET'])
def train_wind():
    selected_provinsi = request.args.get('provinsi')
    selected_kabupaten = request.args.get('kabupaten')
    cursor = connection.cursor()
    cursor.execute("SELECT provinsi, date, windspeed, humidity, rainfall, temperature FROM posts WHERE kabupaten = %s AND provinsi = %s", (selected_kabupaten, selected_provinsi))
    data = cursor.fetchall()

    if not data:
        return jsonify({"error": "No data found"}), 404

    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')

    # Features and target variable
    train_data = df[df['date'] <= '2020-12-31']
    test_data = df[df['date'] > '2020-12-31']

    X_train = train_data[['temperature', 'humidity', 'rainfall']].values
    y_train = train_data[['windspeed']].values
    X_test = test_data[['temperature', 'humidity', 'rainfall']].values
    y_test = test_data[['windspeed']].values

    dates = test_data['date'].tolist()

    scaler_X = StandardScaler()
    X_train_scaled = scaler_X.fit_transform(X_train)
    X_test_scaled = scaler_X.transform(X_test)

    scaler_y = StandardScaler()
    y_train_scaled = scaler_y.fit_transform(y_train)
    y_test_scaled = scaler_y.transform(y_test)

    elm(hidden_units=20, activation_function='sigmoid', x=X_train_scaled, y=y_train_scaled, random_type='normal')
    model.fit()

    y_pred_scaled = model.predict(X_test_scaled)
    y_pred = scaler_y.inverse_transform(y_pred_scaled)
    y_test = scaler_y.inverse_transform(y_test_scaled)

    result_df = pd.DataFrame({
        'date': dates,
        'Actual Windspeed': y_test.flatten(),
        'Predicted Windspeed': y_pred.flatten()
    })

    response = {
        'result': result_df.to_dict(orient='records')
    }
    return jsonify(response)

@app.route('/train', methods=['GET'])
def final_data():

    cursor = connection.cursor()
    selected_provinsi = request.args.get('selectedProvinsi')
    selected_kabupaten = request.args.get('selectedKabupaten')

    response_temp = app.test_client().get('/train/temperature', query_string={'provinsi': selected_provinsi, 'kabupaten': selected_kabupaten})
    response_humid = app.test_client().get('/train/humidity', query_string={'provinsi': selected_provinsi, 'kabupaten': selected_kabupaten})
    response_rain = app.test_client().get('/train/rainfall', query_string={'provinsi': selected_provinsi, 'kabupaten': selected_kabupaten})
    response_wind = app.test_client().get('/train/windspeed', query_string={'provinsi': selected_provinsi, 'kabupaten': selected_kabupaten})
    
    result_temp = response_temp.get_json().get('result')
    result_humid = response_humid.get_json().get('result')
    result_rain = response_rain.get_json().get('result')
    result_wind = response_wind.get_json().get('result')

    predict_data = {}
    for temp, humid, rain, wind in zip(result_temp, result_humid, result_rain, result_wind):
        insert_query = "INSERT INTO post_predicts (provinsi, kabupaten, temperature_predict, rainfall_predict, humidity_predict, windspeed_predict, date) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        date_str = temp['date']  
        date = datetime.datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %Z')  
        formatted_date = format_date(date)  
        cursor.execute(insert_query, (selected_provinsi, selected_kabupaten, temp['Predicted Temperature'],rain['Predicted Rainfall'], humid['Predicted Humidity'], wind['Predicted Windspeed'], formatted_date))
        connection.commit()
        predict_data[formatted_date] = {
            'Date' : formatted_date,
            'Actual Temperature': temp['Actual Temperature'],
            'Predicted Temperature': temp['Predicted Temperature'],
            'Actual Humidity': humid['Actual Humidity'],
            'Predicted Humidity': humid['Predicted Humidity'],
            'Actual Rainfall': rain['Actual Rainfall'],
            'Predicted Rainfall': rain['Predicted Rainfall'],
            'Actual Windspeed': wind['Actual Windspeed'],
            'Predicted Windspeed': wind['Predicted Windspeed']
        }

    return jsonify(predict_data)

@app.route('/api/fwi-data-all', methods=['GET', 'POST'])
def fwi_data():
    data = request.json
    date = data['date']

    cursor = connection.cursor()
    q = ("""
            SELECT date, temperature, humidity, rainfall, windspeed, provinsi, kabupaten
            FROM posts
            WHERE date = %s
            """)
    cursor.execute(q, (date,))
    data = cursor.fetchall()
    
    if not data:
        return jsonify({"error": "No data found"}), 404
    
    results = []

    ffmc0 = 85.0  
    dmc0 = 6.0    
    dc0 = 15.0

    for entry in data:
        kabupaten = entry['kabupaten']
        provinsi = entry['provinsi']
        date = entry['date']
        date_out = format_date(date)
        windspeed = entry['windspeed']
        humidity = entry['humidity']
        rainfall = entry['rainfall']
        temperature = entry['temperature']
        
        q1 = ("SELECT name FROM regencies WHERE id = %s AND province_id = %s")
        cursor.execute(q1, (kabupaten, provinsi))
        name_data = cursor.fetchall()

        for entry_name in name_data:
            name = entry_name['name']
        
        month = date.month
        
        fwi_instance = FWICLASS(temp=temperature, rhum=humidity, wind=windspeed, prcp=rainfall)
        
        ffmc = fwi_instance.FFMCcalc(ffmc0)
        dmc = fwi_instance.DMCcalc(dmc0, month)
        dc = fwi_instance.DCcalc(dc0, month)
        isi = fwi_instance.ISIcalc(ffmc)
        bui = fwi_instance.BUIcalc(dmc, dc)
        fwi = fwi_instance.FWIcalc(isi, bui)
        
        # insert_query = "INSERT INTO fwis (provinsi, kabupaten, ffmc, dmc, dc, isi, bui, fwi, date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        # cursor.execute(insert_query, (provinsi, kabupaten, ffmc, dmc, dc, isi, bui, fwi, date))
        # connection.commit()
        results.append({
            "name": name,
            "date": date_out,
            "FFMC": ffmc,
            "DMC": dmc,
            "DC": dc,
            "ISI": isi,
            "BUI": bui,
            "FWI": fwi
        })

        ffmc0 = ffmc
        dmc0 = dmc
        dc0 = dc
    return jsonify(results)

@app.route('/api/fwi-data-0', methods=['GET'])
def fwi_data1():
    date = '2019-01-01'

    cursor = connection.cursor()
    q = ("""
            SELECT date, temperature, humidity, rainfall, windspeed, provinsi, kabupaten
            FROM posts
            WHERE date = %s
            """)
    cursor.execute(q, (date,))
    data = cursor.fetchall()

    if not data:
        return jsonify({"error": "No data found"}), 404

    results = []

    ffmc0 = 85.0  
    dmc0 = 6.0    
    dc0 = 15.0

    for entry in data:
        kabupaten = entry['kabupaten']
        provinsi = entry['provinsi']
        date = entry['date']
        date_out = format_date(date)
        windspeed = entry['windspeed']
        humidity = entry['humidity']
        rainfall = entry['rainfall']
        temperature = entry['temperature']

        q1 = ("SELECT name FROM regencies WHERE id = %s AND province_id = %s")
        cursor.execute(q1, (kabupaten, provinsi))
        name_data = cursor.fetchall()

        for entry_name in name_data:
            name = entry_name['name']

        month = date.month

        fwi_instance = FWICLASS(temp=temperature, rhum=humidity, wind=windspeed, prcp=rainfall)

        ffmc = fwi_instance.FFMCcalc(ffmc0)
        dmc = fwi_instance.DMCcalc(dmc0, month)
        dc = fwi_instance.DCcalc(dc0, month)
        isi = fwi_instance.ISIcalc(ffmc)
        bui = fwi_instance.BUIcalc(dmc, dc)
        fwi = fwi_instance.FWIcalc(isi, bui)

        results.append({
            "name": name,
            "date": date_out,
            "FFMC": ffmc,
            "DMC": dmc,
            "DC": dc,
            "ISI": isi,
            "BUI": bui,
            "FWI": fwi
        })

        ffmc0 = ffmc
        dmc0 = dmc
        dc0 = dc

    print("FWI Data:", results)  # Log FWI data to the console
    return jsonify(results)

@app.route('/fwi-upload_db', methods=['GET', 'POST'])
def fwi_data_db():

    cursor = connection.cursor()
    q = ("""
            SELECT date, temperature, humidity, rainfall, windspeed, provinsi, kabupaten
            FROM posts
            WHERE kabupaten = '3671' AND date BETWEEN '2019-01-01' AND '2024-01-29'
            """)
    cursor.execute(q)
    data = cursor.fetchall()
    
    if not data:
        return jsonify({"error": "No data found"}), 404
    
    results = []

    ffmc0 = 85.0  
    dmc0 = 6.0    
    dc0 = 15.0

    for entry in data:
        kabupaten = entry['kabupaten']
        provinsi = entry['provinsi']
        date = entry['date']
        date_out = format_date(date)
        windspeed = entry['windspeed']
        humidity = entry['humidity']
        rainfall = entry['rainfall']
        temperature = entry['temperature']
        
        month = date.month
        
        fwi_instance = FWICLASS(temp=temperature, rhum=humidity, wind=windspeed, prcp=rainfall)
        
        ffmc = fwi_instance.FFMCcalc(ffmc0)
        dmc = fwi_instance.DMCcalc(dmc0, month)
        dc = fwi_instance.DCcalc(dc0, month)
        isi = fwi_instance.ISIcalc(ffmc)
        bui = fwi_instance.BUIcalc(dmc, dc)
        fwi = fwi_instance.FWIcalc(isi, bui)
        
        insert_query = "INSERT INTO fwis (provinsi, kabupaten, ffmc, dmc, dc, isi, bui, fwi, date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(insert_query, (provinsi, kabupaten, ffmc, dmc, dc, isi, bui, fwi, date))
        connection.commit()
        results.append({
            "date": date_out,
            "FFMC": ffmc,
            "DMC": dmc,
            "DC": dc,
            "ISI": isi,
            "BUI": bui,
            "FWI": fwi
        })

        ffmc0 = ffmc
        dmc0 = dmc
        dc0 = dc
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, request, jsonify, render_template
import numpy as np
import joblib

app = Flask(__name__)
model = joblib.load('model.pkl')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    # Extraction des valeurs numériques
    cylinders = float(request.form['cylinders'])
    displacement = float(request.form['displacement'])
    horsepower = float(request.form['horsepower'])
    weight = float(request.form['weight'])
    acceleration = float(request.form['acceleration'])
    model_year = float(request.form['model year'])

    # Récupération des valeurs d'origine avec une valeur par défaut de 0
    origin_asia = int(request.form.get('origin_Asia', 0))
    origin_europe = int(request.form.get('origin_Europe', 0))
    origin_usa = int(request.form.get('origin_USA', 0))

    # Création de la liste finale des caractéristiques pour la prédiction
    final_features = np.array([cylinders, displacement, horsepower, weight, acceleration, model_year, origin_asia, origin_europe, origin_usa]).reshape(1, -1)

    prediction = model.predict(final_features)

    output = round(prediction[0], 2)

    return render_template('index.html', prediction_text='Prediction MPG : {}'.format(output))

@app.route('/predict_api', methods=['POST'])
def predict_api():
    '''
    For direct API calls through request
    '''
    data = request.get_json(force=True)
    prediction = model.predict([np.array(list(data.values()))])

    output = prediction[0]
    return jsonify(output)

if __name__ == "__main__":
    app.run(debug=True)

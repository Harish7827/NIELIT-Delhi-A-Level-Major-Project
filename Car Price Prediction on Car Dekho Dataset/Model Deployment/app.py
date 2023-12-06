from flask import Flask, render_template, request, jsonify
import pickle
import pandas as pd
import datetime
import numpy as np

app = Flask(__name__)

# Load the pre-trained model
model_file = 'rf_regression_model.pkl'
with open(model_file, 'rb') as file:
    model = pickle.load(file)

# Define a route for the home page
@app.route('/')
def home():
    return render_template('index.html')

# Define a route for prediction
@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        km_driven = float(request.form['km_driven'])
        mileage = float(request.form['mileage'])
        max_power = float(request.form['max_power'])
        engine = float(request.form['engine'])
        seats = float(request.form['seats'])
        year = int(request.form['year'])
        owner = request.form['owner']
        fuel = request.form['fuel']
        transmission = request.form['transmission']
        seller_type = request.form['seller_type']

        car_age  = (datetime.datetime.now().year) - (year)


        # Owner input
        if owner == "Fisrt Owner":
            First_Owner = 1.0
            Second_Owner = 0.0
            Third_Owner = 0.0
            Fourth_Above_Owner = 0.0
        elif owner == "Second Owner":
            First_Owner = 0.0
            Second_Owner = 1.0
            Third_Owner = 0.0
            Fourth_Above_Owner = 0.0
        elif owner == "Third Owner":
            First_Owner = 0.0
            Second_Owner = 0.0
            Third_Owner = 1.0
            Fourth_Above_Owner = 0.0
        else:
            First_Owner = 0.0
            Second_Owner = 0.0
            Third_Owner = 0.0
            Fourth_Above_Owner = 1.0

        # Fuel type input 
        if fuel == "CNG":
            CNG = 1.0
            Diesel = 0.0
            Petrol = 0.0
            LPG = 0.0
        elif fuel == "Diesel":
            CNG = 0.0
            Diesel = 1.0
            Petrol = 0.0
            LPG = 0.0
        elif fuel == "Petrol":
            CNG = 0.0
            Diesel = 0.0
            Petrol = 1.0
            LPG = 0.0
        else:
            CNG = 0.0
            Diesel = 0.0
            Petrol = 0.0
            LPG = 1.0

        # Seller type input
        if seller_type == "Dealer":
            Dealer = 1.0
            Individual = 0.0 
            Trustmark_Dealer = 0.0
        elif seller_type == "Individual":
            Dealer = 0.0
            Individual = 1.0 
            Trustmark_Dealer = 0.0
        else:
            Dealer = 0.0
            Individual = 0.0 
            Trustmark_Dealer = 1.0

        # Transmission input

        if transmission == "Automatic":
            transmission = 0.0
        else:
            transmission = 1.0

        # Create Dictionary on user input data
        data = {
            'km_driven' : [km_driven], 
            'transmission' : [transmission], 
            'mileage' : [mileage], 
            'engine' : [engine], 
            'max_power' : [max_power], 
            'seats' : [seats],
            'car_age' : [car_age],
            'First Owner' : [First_Owner], 
            'Fourth & Above Owner' : [Fourth_Above_Owner], 
            'Second Owner' : [Second_Owner], 
            'Third Owner': [Third_Owner],
            'CNG' : [CNG],
            'Diesel' : [Diesel], 
            'LPG' : [LPG], 
            'Petrol' : [Petrol],
            'Dealer' : [Dealer], 
            'Individual' : [Individual], 
            'Trustmark Dealer' : [Trustmark_Dealer]
        } 

        # Convert into Dataframe
        df = pd.DataFrame(data)
        
        # Predict the value using trained model 
        pred = model.predict(df)
    
    return render_template('index.html', Valuation = "You Can Sell The Car at {} INR".format(round(np.expm1(np.expm1(pred))[0],2)))
 
if __name__ == '__main__':
    app.run(debug=True)

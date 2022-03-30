from flask import Flask, url_for, render_template, request, Markup
import json

app = Flask(__name__)

def get_airport_options():
    with open('airlines.json') as airlines_data:
        data = json.load(airlines_data)
    airports=[]
    for c in data:
        if c["Airport"]["Code"] not in airports:
            airports.append(c["Airport"]["Code"])
    options=""
    for a in airports:
        options += Markup("<option value=\"" + a + "\">" + a + "</option>")
    return options

def get_airline_options():
    with open('airlines.json') as airlines_data:
        data = json.load(airlines_data)
    airlines=[]
    for c in data:
        for x in c["Statistics"]["Carriers"]["Names"].split(","):
            if x not in airlines:
                airlines.append(x)
    options=""
    for a in airlines:
        options += Markup("<option value=\"" + a + "\">" + a + "</option>")
    return options

def most_delayed_airport_year(code):
    with open('airlines.json') as airlines_data:
        data = json.load(airlines_data)
    busiestYear = 0
    biggest = 0
    for a in data:
        if a["Airport"]["Code"] == code:
            if a["Statistics"]["Flights"]["Total"] > biggest:
                busiestYear = a["Time"]["Year"]
                biggest = a["Statistics"]["Flights"]["Total"]
    return busiestYear

def get_airport_full_name(code):
    with open('airlines.json') as airlines_data:
        data = json.load(airlines_data)
    for a in data:
        if a["Airport"]["Code"] == code:
            return a["Airport"]["Name"].split(":")[0]

def most_delayed_airline_year(airline):
    with open('airlines.json') as airlines_data:
        data = json.load(airlines_data)
    return

@app.route("/")
def render_main():
    return render_template("home.html")

@app.route("/airport")
def render_airport():
    s = get_airport_options()
    return render_template("airport.html", airport_options = s)

@app.route("/airline")
def render_airline():
    a = get_airline_options()
    return render_template("airline.html", airline_options = a)

@app.route("/ShowAirportData")
def show_airport_data():
    s = get_airport_options()
    airport = request.args["airport"]
    delayYear = most_delayed_airport_year(airport)
    fullName = get_airport_full_name(airport)
    return render_template("airport.html", airport_options = s, airport_delay_year = delayYear, airport_name = fullName)

@app.route("/ShowAirlineData")
def show_airline_data():
    a = get_airline_options()
    airline = request.args["airline"]
    delayYear = most_delayed_airline_year()
    return render_template("airline.html", airline_options = a, airline_delay_year = delayYear, airline_name = airline)

if __name__=="__main__":
    app.run(debug=True)

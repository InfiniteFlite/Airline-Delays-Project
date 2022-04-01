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

def get_month_options():
    months = ["January", "Febuary", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December", "Whole Year"]
    options = ""
    for m in months:
        options += Markup("<option value\"" + m + "\>" + m + "</option>")
    return options

def most_delayed_airport(code, month):
    with open('airlines.json') as airlines_data:
        data = json.load(airlines_data)
    if month == "Whole Year":
        busiestYears = {}
        for a in data:
            if a["Airport"]["Code"] == code:
                        if a["Time"]["Year"] in busiestYears.keys():
                            busiestYears[a["Time"]["Year"]] += a["Statistics"]["Flights"]["Total"]
                        else:
                            busiestYears[a["Time"]["Year"]] = a["Statistics"]["Flights"]["Total"]
    biggestYear = 0
    for b in busiestYears:
        if b > biggestYear:
            biggestYear = b
            return "The year where " + get_airport_full_name(code) + " was the most delayed was " + str(busiestYear)
    else:
        currentBiggest = 0
        busiestYearForMonth = 0
        for a in data:
            if a["Airport"]["Code"] == code:
                if a["Time"]["Month Name"] == month and a["Statistics"]["Flights"]["Total"] > currentBiggest:
                    busiestYearForMonth = a["Time"]["Year"]
                    currentBiggest = a["Statistics"]["Flights"]["Total"]
        return "The year where " + month + " had the most delays at " + get_airport_full_name(code) + " was " + str(busiestYearForMonth)




def get_airport_full_name(code):
    with open('airlines.json') as airlines_data:
        data = json.load(airlines_data)
    for a in data:
        if a["Airport"]["Code"] == code:
            return a["Airport"]["Name"].split(":")[0]

def most_delayed_airline(airline, month):
    with open('airlines.json') as airlines_data:
        data = json.load(airlines_data)
    if month == "Whole Year":
        busiestYears = {}
        for a in data:
                for x in a["Statistics"]["Carriers"]["Names"].split(","):
                    if x == airline:
                        if a["Time"]["Year"] in busiestYears.keys():
                            busiestYears[a["Time"]["Year"]] += a["Statistics"]["Flights"]["Total"]/a["Statistics"]["Carriers"]["Total"]
                        else:
                            busiestYears[a["Time"]["Year"]] = a["Statistics"]["Flights"]["Total"]/a["Statistics"]["Carriers"]["Total"]
        biggestYear = 0
        currentBiggestYear = 0
        for b in busiestYears:
            if busiestYears[b] > currentBiggestYear:
                currentBiggestYear = busiestYears[b]
                biggestYear = b
        return "The year where " + airline + " was the most delayed was " + str(biggestYear)
    else:
        currentBiggest = 0
        busiestYearForMonth = 0
        for a in data:
            if a["Time"]["Month Name"] == month:
                for x in a["Statistics"]["Carriers"]["Names"].split(","):
                    if x == airline:
                        if a["Statistics"]["Flights"]["Total"]/a["Statistics"]["Carriers"]["Total"] > currentBiggest:
                            currentBiggest = a["Statistics"]["Flights"]["Total"]/a["Statistics"]["Carriers"]["Total"]
                            busiestYearForMonth = a["Time"]["Year"]
        return "The year where " + month + " had the most delays for " + airline + " was " + str(busiestYearForMonth)


@app.route("/")
def render_main():
    return render_template("home.html")

@app.route("/airport")
def render_airport():
    s = get_airport_options()
    m = get_month_options()
    return render_template("airport.html", airport_options = s, Month_Options = m)

@app.route("/airline")
def render_airline():
    a = get_airline_options()
    m = get_month_options()
    return render_template("airline.html", airline_options = a, Month_Options = m)

@app.route("/ShowAirportData")
def show_airport_data():
    s = get_airport_options()
    m = get_month_options()
    airport = request.args["airport"]
    month = request.args["month"]
    delayYear = most_delayed_airport(airport, month)
    return render_template("airport.html", airport_options = s, Month_Options = m, airport_delay_year = delayYear)

@app.route("/ShowAirlineData")
def show_airline_data():
    a = get_airline_options()
    m = get_month_options()
    airline = request.args["airline"]
    month = request.args["month"]
    delayYear = most_delayed_airline(airline, month)
    return render_template("airline.html", airline_options = a, Month_Options = m, airline_delay_year = delayYear)

if __name__=="__main__":
    app.run(debug=True)

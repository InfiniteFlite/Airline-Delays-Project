from flask import Flask, url_for, render_template, request, redirect

app = Flask(__name__)

@app.route("/")
def render_main():
    return render_template("home.html")

if __name__=="__main__":
    app.run(debug=True)

from flask import Flask, render_template
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/hello")
def hello():
    return render_template("hello.html")

@app.route("/config")
def config():
    secret_key = os.getenv("SECRET_KEY", "Not Found")
    return render_template("config.html", secret_key=secret_key)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)


#https://departure-handlebar-protegee.ngrok-free.dev
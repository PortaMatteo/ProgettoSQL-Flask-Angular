from flask import Flask, render_template, request,redirect,url_for,Response,url_for,redirect
app = Flask(__name__)

import io
import pandas as pd
import pymssql

@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)
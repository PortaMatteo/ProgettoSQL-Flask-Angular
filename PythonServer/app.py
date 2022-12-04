from flask import Flask, render_template, request,redirect,url_for,Response,url_for,redirect
app = Flask(__name__)

import io
import pandas as pd
import pymssql

from os import getenv
from dotenv import load_dotenv
load_dotenv()

conn = pymssql.connect(server='213.140.22.237\SQLEXPRESS', user='porta.matteo', password='xxx123##', database='porta.matteo')

@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")

@app.route("/home/search", methods=["GET"])
def search():
  data = request.args["Ricerca"]
  return jasonfy()


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)
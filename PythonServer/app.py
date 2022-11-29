from flask import Flask, render_template, request,redirect,url_for,Response,url_for,redirect
app = Flask(__name__)

import io
import pandas as pd
import pymssql

from os import getenv
from dotenv import load_dotenv
load_dotenv()

sql_server = getenv("SQL_SERVER")
sql_user = getenv("SQL_USER")
sql_password = getenv("SQL_PASSWORD")
sql_name = getenv("SQL_NAME")

conn = pymssql.connect(sql_server, sql_user, sql_password, sql_name)

@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")

@app.route("/home/search", methods=["GET"])
def search():
  data = request.args["Ricerca"]
  return jasonfy()


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)
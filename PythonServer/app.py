from flask import Flask, render_template, request,redirect,url_for,Response,url_for,redirect, jsonify
import io
import pandas as pd
import pymssql
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

conn = pymssql.connect(server='213.140.22.237\SQLEXPRESS', user='porta.matteo', password='xxx123##', database='porta.matteo')

@app.route("/home", methods=["GET"])
def canzoni():
  data = request.args.get("search")

  q = 'SELECT * FROM spotify.tracks WHERE name LIKE %(data)s' 
  cursor = conn.cursor(as_dict=True)
  p = {"data": f"%{data}%"}
  cursor.execute(q, p)
  data = cursor.fetchall()

  print(data)

  return jsonify(data)


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)
from flask import Flask, render_template, request,redirect,url_for,Response,url_for,redirect, jsonify
import io
import pandas as pd
import pymssql
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

conn = pymssql.connect(server='213.140.22.237\SQLEXPRESS', user='porta.matteo', password='xxx123##', database='porta.matteo')

@app.route("/search", methods=["GET"])
def search():
  res = []
  arg = request.args.get("search")
  print(arg)

  q = 'SELECT TOP 10 * FROM spotify.albums ' + ('WHERE name LIKE %(arg)s' if arg != None and arg != '' else "") 
  cursor = conn.cursor(as_dict=True)
  p = {"arg": f"{arg}%"}

  cursor.execute(q, p)
  data = cursor.fetchall()
  if len(data) < 10:
    p = {"arg": f"%{arg}%"}

    cursor.execute(q, p)
    if cursor.fetchall() not in data:
      data += cursor.fetchall()
    if len(data) > 10:
      data = data[:10]
  res.append(data)

  q = 'SELECT TOP 10 * FROM spotify.artists ' + ('WHERE name LIKE %(arg)s' if arg != None and arg != '' else "") 
  cursor = conn.cursor(as_dict=True)
  p = {"arg": f"{arg}%"}

  cursor.execute(q, p)
  data = cursor.fetchall()
  if len(data) < 10:
    p = {"arg": f"%{arg}%"}

    cursor.execute(q, p)
    if cursor.fetchall() not in data:
      data += cursor.fetchall()
    if len(data) > 10:
      data = data[:10]

  res.append(data)

  q = 'SELECT TOP 10 * FROM spotify.genres ' + ('WHERE id LIKE %(arg)s' if arg != None and arg != '' else "") 
  cursor = conn.cursor(as_dict=True)
  p = {"arg": f"{arg}%"}

  cursor.execute(q, p)
  data = cursor.fetchall()
  if len(data) < 10:
    p = {"arg": f"%{arg}%"}

    cursor.execute(q, p)
    if cursor.fetchall() not in data:
      data += cursor.fetchall()
    if len(data) > 10:
      data = data[:10]
  
  res.append(data)

  q = 'SELECT TOP 10 name FROM spotify.tracks ' + ('WHERE name LIKE %(arg)s' if arg != None and arg != '' else "") 
  cursor = conn.cursor(as_dict=True)
  p = {"arg": f"{arg}%"}

  cursor.execute(q, p)
  data = cursor.fetchall()
  print(data)
  if len(data) < 10:
    p = {"arg": f"%{arg}%"}

    cursor.execute(q, p)
    if cursor.fetchall() not in data:
      data += cursor.fetchall()
      print(data)
    if len(data) > 10:
      data = data[:10]
  
  res.append(data)

  return jsonify(res)

@app.route("/register/data", methods=["POST"])
def dati_registrazione():
  username = request.form["username"]
  email = request.form["email"]
  password = request.form["password"]
  Cpassword = request.form["Cpassword"]
  print(username)
  return  username


  


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)
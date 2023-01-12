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

#'select albums.*,artists.[name] as artist from (select top 10 * from spotify.albums ' + ('where [name] like %(arg)s) ' if arg != None and arg != '' else ")") + 'as albums inner join spotify.r_albums_artists as r on albums.id = r.album_id inner join spotify.artists on r.artist_id = artists.id'

  q = 'select albums.*,artists.[id] as artist_id,artists.[name] as artist from (select top 10 * from spotify.albums ' + ('where [name] like %(arg)s) ' if arg != None and arg != '' else ")") + 'as albums left join spotify.r_albums_artists as r on albums.id = r.album_id left join spotify.artists on r.artist_id = artists.id'
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

#'select artists.*,genre.[id] as genre from (select top 10 * from spotify.artists ' + ('where [name] like %(arg)s) ' if arg != None and arg != '' else ")") + 'as artists inner join spotify.r_artist_genre as r on artists.id = r.artist_id'

  q = 'select artists.*,genres.[id] as genre from (select top 10 * from spotify.artists ' + ('where [name] like %(arg)s) ' if arg != None and arg != '' else ")") + 'as artists left join spotify.r_artist_genre as r on artists.id = r.artist_id left join spotify.genres on r.genre_id = genres.id' 
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


#'select tracks.*,albums.[name] as album from (select top 10 * from spotify.tracks ' + ('where [name] like %(arg)s) ' if arg != None and arg != '' else ")") + 'as tracks inner join spotify.r_albums_tracks as r on tracks.id = r.track_id inner join spotify.albums on r.album_id = albums.id'

  q = 'select tracks.*,albums.[id] as album_id,albums.[name] as album from (select top 10 * from spotify.tracks ' + ('where [name] like %(arg)s) ' if arg != None and arg != '' else ")") + 'as tracks left join spotify.r_albums_tracks as r on tracks.id = r.track_id left join spotify.albums on r.album_id = albums.id'
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

  return jsonify(res)


@app.route("/search/album", methods=["GET"])
def infoalbum():
  res = []
  arg = request.args.get("search")
  q = 'select albums.*,artists.[name] as artist from (select * from spotify.albums ' + ('where [id] like %(arg)s) ') + 'as a left join spotify.r_albums_artists as r on a.id = r.album_id left join spotify.artists on r.artist_id = artists.id '
  cursor = conn.cursor(as_dict=True)
  p = {"arg": f"{arg}%"}

  cursor.execute(q, p)
  data = cursor.fetchall()

  res.append(data)

  print(data)

  q = 'select tracks.* from (select * from spotify.tracks ' + ('where [id] in (select track_id from spotify.r_albums_tracks as at inner join (select albums.id from spotify.albums %(arg)s) as a on a.id = at.album_id)) ')
  cursor = conn.cursor(as_dict=True)
  p = {"arg": f"{arg}%"}

  cursor.execute(q, p)
  data = cursor.fetchall()

  res.append(data)

  print(data)

  return jsonify(res)

@app.route("/register/data", methods=["POST"])
def dati_registrazione():
  username = request.form["username"]
  email = request.form["email"]
  password = request.form["password"]
  Cpassword = request.form["Cpassword"]
  return  username


# FARE LA QUERY PER LA TRACCIA IN BASE ALL'ARTISTA
# TOGLIERE IL GENERE NELLA QUERY DELL'ARTISTA


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)
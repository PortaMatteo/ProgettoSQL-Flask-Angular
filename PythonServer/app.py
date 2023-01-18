from flask import Flask, render_template, request,redirect,url_for,Response,url_for,redirect, jsonify
import io
import pandas as pd
import pymssql
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

angular_url = 'https://4200-portamatteo-progettosql-uyt5134aw7w.ws-eu82.gitpod.io'

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

  q = 'select tracks.*,albums.[id] as album_id,albums.[name] as album, artists.name as nome_a,artists.id as id_a from (select top 10 * from spotify.tracks ' + ('where [name] like %(arg)s) ' if arg != None and arg != '' else ")") + 'as tracks left join spotify.r_albums_tracks as r on tracks.id = r.track_id left join spotify.albums on r.album_id = albums.id left join spotify.r_track_artist as ta on tracks.[id] = ta.track_id left join spotify.artists on ta.artist_id = artists.id'
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
  q = 'select a.*,artists.[id],artists.[name] as artist from (select * from spotify.albums ' + ('where [id] like %(arg)s) ') + 'as a left join spotify.r_albums_artists as r on a.id = r.album_id left join spotify.artists on r.artist_id = artists.id '
  cursor = conn.cursor(as_dict=True)
  p = {"arg": f"{arg}"}

  cursor.execute(q, p)
  data = cursor.fetchall()

  res.append(data)


  q = 'select t.* from (select * from spotify.tracks where [id] in (select track_id from spotify.r_albums_tracks as at ' + ('where at.album_id like %(arg)s') + '))as t'
  cursor = conn.cursor(as_dict=True)
  p = {"arg": f"{arg}"}

  cursor.execute(q, p)
  data = cursor.fetchall()

  res.append(data)

  print(res)

  return jsonify(res)

@app.route("/search/artist", methods=["GET"])
def infoartist():
  res = []
  arg = request.args.get("search")
  q = 'select * from (select * from spotify.artists ' + ('where [id] like %(arg)s) ') + 'as a inner join (select * from spotify.r_artist_genre ' + ('where [artist_id] like %(arg)s) ') + 'as g on a.id = g.artist_id'
  cursor = conn.cursor(as_dict=True)
  p = {"arg": f"{arg}"}

  cursor.execute(q, p)
  data = cursor.fetchall()


  res.append(data)

  q = 'select t.* from (select * from spotify.albums where [id] in (select album_id from spotify.r_albums_artists as aa ' + ('where aa.artist_id like %(arg)s') + '))as t'
  cursor = conn.cursor(as_dict=True)
  p = {"arg": f"{arg}"}

  cursor.execute(q, p)
  data = cursor.fetchall()

  res.append(data)

  q = 'select t.* from (select * from spotify.tracks where [id] in (select track_id from spotify.r_track_artist as ta ' + ('where ta.artist_id like %(arg)s') + '))as t'
  cursor = conn.cursor(as_dict=True)
  p = {"arg": f"{arg}"}

  cursor.execute(q, p)
  data = cursor.fetchall()

  res.append(data)

  print(res)

  return jsonify(res)

@app.route("/search/track", methods=["GET"])
def infotrack():
  res = []
  arg = request.args.get("search")
  q = 'select * from spotify.tracks ' + ('where [id] like %(arg)s ')
  cursor = conn.cursor(as_dict=True)
  p = {"arg": f"{arg}"}

  cursor.execute(q, p)
  data = cursor.fetchall()


  res.append(data)
  
  q = 'select a.name,ag.genre_id as genre from (select * from spotify.artists where [id] in (select artist_id from spotify.r_track_artist where track_id LIKE ' + ('%(arg)s') + ')) as a inner join spotify.r_artist_genre as ag on a.id = ag.artist_id '
  cursor = conn.cursor(as_dict=True)
  p = {"arg": f"{arg}"}

  cursor.execute(q, p)
  data = cursor.fetchall()

  res.append(data)

  q = 'select t.* from (select * from spotify.tracks where [id] in (select track_id from spotify.r_albums_tracks as at ' + ('where at.album_id in (select album_id from spotify.r_albums_tracks where track_id LIKE %(arg)s)') + '))as t ' + ('where [id] not like %(arg)s ')
  cursor = conn.cursor(as_dict=True)
  p = {"arg": f"{arg}"}

  cursor.execute(q, p)
  data = cursor.fetchall()

  res.append(data)

  print(res)

  return jsonify(res)

@app.route("/register/data", methods=["POST"])
def dati_registrazione():
  form_data = request.get_json()
  username = form_data["username"]
  email = form_data["email"]
  password = form_data["password"]
  print(username)
  Cq = "select * from spotify.users where username = %(username)s"
  Ccursor = conn.cursor(as_dict=True)
  Cp = {"username": f"{username}","email": f"{email}","password": f"{password}"}
  Ccursor.execute(Cq, Cp)
  Cdata = Ccursor.fetchall()
  if Cdata != []:
    return redirect(angular_url + '/register')
  else:
    q = 'insert into spotify.users (username, email, password) values (%(username)s,%(email)s,%(password)s)'
    cursor = conn.cursor(as_dict=True)
    p = {"username": f"{username}","email": f"{email}","password": f"{password}"}

    cursor.execute(q, p)
    conn.commit()
    #print(data)
    return redirect(angular_url + '/login')

@app.route("/login/data", methods=["POST"])
def dati_login():
  form_data = request.get_json()
  print(form_data)
  email = form_data['email']
  password = form_data['password']
  q = "select * from spotify.users where email = %(email)s and password = %(password)s "
  cursor = conn.cursor(as_dict=True)
  p = {"email": f"{email}","password": f"{password}"}

  cursor.execute(q, p)
  data = cursor.fetchall()
  
  if data == []:
    return redirect(angular_url + '/login')
  else:
    return  jsonify(data) 

@app.route("/modify", methods=["POST"])
def modifica_dati():
  form_data = request.get_json()
  username = form_data['username']
  email = form_data['email']
  #email = request.form["email"]
  print(username,'',email)
  return email 


# FARE LA QUERY PER LA TRACCIA IN BASE ALL'ARTISTA
# TOGLIERE IL GENERE NELLA QUERY DELL'ARTISTA
# LE CANZIONI CON PIù ARTISTI VENGONO RIPETUTE, e sti cazzi?

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)
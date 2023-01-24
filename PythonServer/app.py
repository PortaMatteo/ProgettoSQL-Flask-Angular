from flask import Flask, render_template, request,redirect,url_for,Response,url_for,redirect, jsonify,json,session 
from flask_session import Session
import io
import pandas as pd
import datetime
import pymssql
import random
import string
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

angular_url = 'https://4200-portamatteo-progettosql-nyjfa3kgy7b.ws-eu83.gitpod.io'

conn = pymssql.connect(server='213.140.22.237\SQLEXPRESS', user='porta.matteo', password='xxx123##', database='porta.matteo')

@app.route("/search", methods=["GET"])
def search():
  res = []

  arg = request.args.get("search")

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

@app.route("/search/genre", methods=["GET"])
def infogenre():
  res = []
  arg = request.args.get("search")
  q = 'select TOP 50 b.* from (select * from spotify.artists where id in (select artist_id from spotify.r_artist_genre ' + ('where genre_id like %(arg)s ))as b ') + 'order by b.followers desc'
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
  print(form_data)
  status = 'user'
  if username == '' or username == None or email == '' or email == None or password == '' or password == None:
    print('noooooooooooooooo')
    return json.dumps(False)
  Cq = "select * from spotify.users where email = %(email)s"
  Ccursor = conn.cursor(as_dict=True)
  Cp = {"email": f"{email}"}
  Ccursor.execute(Cq, Cp)
  Cdata = Ccursor.fetchall()
  if Cdata != []:
    print(Cdata)
    return json.dumps(False)
  q = 'insert into spotify.users (username, email, password, status) values (%(username)s,%(email)s,%(password)s,%(status)s)'
  cursor = conn.cursor(as_dict=True)
  p = {"username": f"{username}","email": f"{email}","password": f"{password}","status":f"{status}"}
  
  cursor.execute(q,p)
  
  #print(data)
  return json.dumps(True)

@app.route("/login/data", methods=["POST"])
def dati_login():
  form_data = request.get_json()
  print(form_data)
  email = form_data['email']
  password = form_data['password']
  if email == '' or email == None or password == '' or password == None:
    return json.dumps(False)
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
  try:
    id = form_data['id']
    username = form_data['username']
    print(id,username)
  except:
    id = None
    username = None
  if id == '' or id == None or username == '' or username == None:
    return json.dumps(False)

  q = 'update spotify.users set username = %(username)s where id = %(id)s'
  cursor = conn.cursor(as_dict=True)
  p = {"username": f"{username}","id": f"{id}"}

  cursor.execute(q, p)

  return json.dumps(True)

@app.route("/listartist", methods=["GET"])
def listartist():

  name = request.args.get("search")
  q = 'select top 50 artists.name,artists.id from spotify.artists where name LIKE %(name)s'
  cursor = conn.cursor(as_dict=True)
  p = {"name": f"{name}%"}

  cursor.execute(q, p)
  data = cursor.fetchall()
  if len(data) < 50:
    p = {"name": f"%{name}%"}

    cursor.execute(q, p)
    if cursor.fetchall() not in data:
      data += cursor.fetchall()
    if len(data) > 50:
      data = data[:50]

  return jsonify(data)

@app.route("/listalbum", methods=["GET"])
def listalbum():

  name = request.args.get("search")
  q = 'select top 50 albums.name,albums.id from spotify.albums where name LIKE %(name)s'
  cursor = conn.cursor(as_dict=True)
  p = {"name": f"{name}%"}

  cursor.execute(q, p)
  data = cursor.fetchall()
  if len(data) < 50:
    p = {"name": f"%{name}%"}

    cursor.execute(q, p)
    if cursor.fetchall() not in data:
      data += cursor.fetchall()
    if len(data) > 50:
      data = data[:50]

  return jsonify(data)

@app.route("/addTrack", methods=["POST"])
def addTrack():
  chars = string.ascii_uppercase + string.digits
  def randStr(N):
	  return ''.join(random.choice(chars) for _ in range(N))
  id = randStr(N=20)
  form_data = request.get_json()
  track_name = form_data["track_name"]
  duration = int(float(form_data["duration"])*1000)
  artista = form_data["artista"]
  try:
    album = form_data["album"]
  except:
    album = None

  if artista != '' and artista != None:
    q = 'insert into spotify.tracks (name, duration,id) values (%(track_name)s,%(duration)s,%(id)s)'
    cursor = conn.cursor(as_dict=True)
    p = {"track_name": f"{track_name}","duration": f"{duration}","id": f"{id}"}

    cursor.execute(q, p)
    conn.commit()
    q = 'insert into spotify.r_track_artist (artist_id,track_id) values (%(artista)s,%(id)s)'
    cursor = conn.cursor(as_dict=True)
    p = {"artista": f"{artista}","id": f"{id}"}

    cursor.execute(q, p)
    conn.commit()
    if album != '' and album != None:
      q = 'insert into spotify.r_albums_tracks (album_id,track_id) values (%(album)s,%(id)s)'
      cursor = conn.cursor(as_dict=True)
      p = {"album": f"{album}","id": f"{id}"}

      cursor.execute(q, p)
  print(id)
  return json.dumps(True)

@app.route("/addArtist", methods=["POST"])
def addArtist():
  chars = string.ascii_uppercase + string.digits
  def randStr(N):
	  return ''.join(random.choice(chars) for _ in range(N))
  id = randStr(N=20)
  form_data = request.get_json()
  try:
    artist_name = form_data["artist_name"]
  except:
    artist_name = None
  if artist_name != '' and artist_name != None:
    q = 'insert into spotify.artists (name,id) values (%(artist_name)s,%(id)s)'
    cursor = conn.cursor(as_dict=True)
    p = {"artist_name": f"{artist_name}","id": f"{id}"}

    cursor.execute(q, p)
    




  print(id)
  return json.dumps(True)

@app.route("/addAlbum", methods=["POST"])
def addAlbum():
  chars = string.ascii_uppercase + string.digits
  def randStr(N):
	  return ''.join(random.choice(chars) for _ in range(N))
  id = randStr(N=20)
  form_data = request.get_json()
  try:
    artista = form_data["artista"]
    album_name = form_data["album_name"]
  except:
    artista = None
    album_name = None
  if album_name != '' and album_name != None and artista != '' and artista != None:
    q = 'insert into spotify.albums (name,id) values (%(album_name)s,%(id)s)'
    cursor = conn.cursor(as_dict=True)
    p = {"album_name": f"{album_name}","id": f"{id}"}

    cursor.execute(q, p)
    conn.commit()


    q = 'insert into spotify.r_albums_artists (album_id,artist_id) values (%(id)s,%(artista)s)'
    cursor = conn.cursor(as_dict=True)
    p = {"id": f"{id}","artista": f"{artista}"}

    cursor.execute(q, p)
    




  print(id)
  return json.dumps(True)


@app.route("/like", methods=["POST"])
def like_():
  now = datetime.datetime.now()
  now = now.strftime('%Y-%m-%d %H:%M:%S')
  form_data = request.get_json()
  print(form_data)
  id_u = form_data['id_u']
  id_t = form_data['id_t']
  Cq = "select * from spotify.favs where track_id = %(id_t)s and user_id = %(id_u)s"
  Ccursor = conn.cursor(as_dict=True)
  Cp = {"id_t": f"{id_t}","id_u": f"{id_u}"}
  Ccursor.execute(Cq, Cp)
  Cdata = Ccursor.fetchall()
  if Cdata != []:
    return json.dumps(False)
  else:
    q = 'insert into spotify.favs (track_id, user_id, date) values (%(id_t)s,%(id_u)s,%(now)s)'
    cursor = conn.cursor(as_dict=True)
    p = {"id_t": f"{id_t}","id_u": f"{id_u}","now": f"{now}"}

    cursor.execute(q, p)
    conn.commit()
    return json.dumps(True)

@app.route("/dislike", methods=["POST"])
def dislike_():
  form_data = request.get_json()
  id_u = form_data['id_u']
  id_t = form_data['id_t']
  q = 'delete from spotify.favs where track_id = %(id_t)s and user_id = %(id_u)s'
  cursor = conn.cursor(as_dict=True)
  p = {"id_t": f"{id_t}","id_u": f"{id_u}"}
  cursor.execute(q, p)
  conn.commit()
  return json.dumps(True)

@app.route("/liked", methods=["GET"])
def liked_():
  id = request.args.get("id")
  print(id)
  q = "select * from spotify.tracks where id in (select track_id from spotify.favs where user_id = %(id)s)"
  cursor = conn.cursor(as_dict=True)
  p = {"id": f"{id}"}
  cursor.execute(q, p)
  data = cursor.fetchall()

  return jsonify(data)
   
@app.route("/delete", methods=["POST"])
def cancellazione_account():
  form_data = request.get_json()
  id = form_data["id"]
  print(id)
  q = 'delete from spotify.r_track_playlist where playlist_id in (select id from spotify.playlists where user_id = %(id)s);delete from spotify.playlists where user_id = %(id)s; delete from spotify.favs where user_id = %(id)s ;delete from spotify.users where id = %(id)s'
  cursor = conn.cursor(as_dict=True)
  p = {"id": f"{id}"}

  cursor.execute(q,p)
  return json.dumps(True)
  
@app.route("/playlist/add", methods=["POST"])
def creazione_playlist():
  form_data = request.get_json()
  id = form_data["id_u"]
  name = form_data["name"]
  description = form_data["description"]
  print(id, name,description)
  Cq = "select * from spotify.playlists where name = %(name)s and user_id = %(id)s"
  Ccursor = conn.cursor(as_dict=True)
  Cp = {"name": f"{name}","id": f"{id}"}
  Ccursor.execute(Cq, Cp)
  Cdata = Ccursor.fetchall()
  if Cdata != []:
    return json.dumps(False)
  else:
    q = 'insert into spotify.playlists (user_id, name, description) values (%(id)s,%(name)s,%(description)s)'
    cursor = conn.cursor(as_dict=True)
    p = {"name": f"{name}","id": f"{id}","description":f"{description}"}

    cursor.execute(q, p)
 
    return json.dumps(True)

@app.route("/playlist/watch", methods=["GET"])
def visualizza_playlist():
  try:
    id = request.args.get("id")
  except:
    id = None

  if id != None and id != '': 
    q = "select * from spotify.playlists where user_id = %(id)s"
    cursor = conn.cursor(as_dict=True)
    p = {"id": f"{id}"}
    cursor.execute(q,p)
    data = cursor.fetchall()
    print(data)
  return jsonify(data)

@app.route("/playlist/delete", methods=["POST"])
def cancella_playlist():
  form_data = request.get_json()
  id_p = form_data["id_p"]
  print(id_p)
  q = 'delete from spotify.r_track_playlist where playlist_id = %(id_p)s; delete from spotify.playlists where id = %(id_p)s'
  cursor = conn.cursor(as_dict=True)
  p = {"id_p": f"{id_p}"}

  cursor.execute(q, p)
  conn.commit()
  return json.dumps(True)

@app.route("/addplaylist", methods=["POST"])
def addplaylist():
  form_data = request.get_json()
  playlist_id = form_data["playlist_id"]
  track_id = form_data["track_id"]
  q = 'insert into spotify.r_track_playlist (track_id,playlist_id) values (%(track_id)s,%(playlist_id)s)'
  cursor = conn.cursor(as_dict=True)
  p = {"track_id": f"{track_id}","playlist_id": f"{playlist_id}"}

  cursor.execute(q, p)
  conn.commit()
  return json.dumps(True)

@app.route("/playlistview", methods=["GET"])
def playlistview():
  id = request.args.get("id")
  q = "select a.* from (select * from spotify.tracks where id in (select track_id from spotify.r_track_playlist where playlist_id = %(id)s))a"
  cursor = conn.cursor(as_dict=True)
  p = {"id": f"{id}"}
  cursor.execute(q, p)
  data = cursor.fetchall()

  return jsonify(data)

@app.route("/deletetrack", methods=["POST"])
def deletetrack():
  form_data = request.get_json()
  id_t = form_data["id_t"]
  id_p = form_data["id_p"]
  print(id_t,id_p)
  q = 'delete from spotify.r_track_playlist where track_id = %(id_t)s and playlist_id = %(id_p)s'
  cursor = conn.cursor(as_dict=True)
  p = {"id_t": f"{id_t}", "id_p":f"{id_p}"}

  cursor.execute(q, p)
  conn.commit()
  return json.dumps(True)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)
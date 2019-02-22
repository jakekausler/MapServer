from flask import Flask, send_file, request
import json
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="ec2-user",
    passwd="Jake021f2f1!",
    database="map"
)
cursor = db.cursor()

@app.route('/maptiles/<int:z>/<int:x>/<string:y>')
def MapTiles(z, x, y):
    z = '{:03d}'.format(z)
    x = '{:03d}'.format(x)
    y = '{:03d}'.format(int(y.split('.')[0]))
    fn = 'map/{}/{}/{}.jpg'.format(z, x, y)
    if int(z) < 6:
        return send_file(fn)
    return ''

@app.route('/gridtiles/<int:z>/<int:x>/<string:y>')
def GridTiles(z, x, y):
    z = '{:03d}'.format(z)
    x = '{:03d}'.format(x)
    y = '{:03d}'.format(int(y.split('.')[0]))
    fn = 'grid/{}/{}/{}.png'.format(z, x, y)
    if int(z) < 6:
        return send_file(fn)
    return ''

@app.route('/bordertiles/<int:z>/<int:x>/<string:y>')
def BorderTiles(z, x, y):
    z = '{:03d}'.format(z)
    x = '{:03d}'.format(x)
    y = '{:03d}'.format(int(y.split('.')[0]))
    fn = 'borders/{}/{}/{}.png'.format(z, x, y)
    if int(z) < 6:
        return send_file(fn)
    return ''

@app.route('/roadsandcitiestiles/<int:z>/<int:x>/<string:y>')
def RoadsAndCitiesTiles(z, x, y):
    z = '{:03d}'.format(z)
    x = '{:03d}'.format(x)
    y = '{:03d}'.format(int(y.split('.')[0]))
    fn = 'roadsandcities/{}/{}/{}.png'.format(z, x, y)
    if int(z) < 6:
        return send_file(fn)
    return ''

@app.route('/')
def Index():
    return send_file('index.html')

@app.route('/DnDGenerators')
def DnDGenerators(self, f):
    print f
    return send_file("DnDGenerators/{}".format(f))

@app.route('/markers', methods=['GET', 'PUT', 'DELETE', 'POST'])
def Markers():
    if request.method == 'GET':
        return json.dumps(GetMarkers()), 200

    if request.method == 'PUT':
        data = request.get_data()
        AddMarker(json.loads(data))
        return "Successfully added marker", 200

    if request.method == 'DELETE':
        data = request.get_data()
        DeleteMarker(data)
        return "Successfully deleted marker", 200

    if request.method == 'POST':
        data = request.get_data()
        UpdateMarker(json.loads(data))
        return "Successfully updated marker", 200

def GetMarkers():
    cursor.execute("SELECT * from markers")
    vals = cursor.fetchall()
    for i in range(len(vals)):
        vals[i] = {
            "id": vals[i][0],
            "title": vals[i][1],
            "content": vals[i][2],
            "icon": vals[i][3],
            "position": {
                "lat": str(vals[i][4]),
                "lng": str(vals[i][5])
            }
        }
    return vals

def AddMarker(marker):
    cursor.execute("INSERT INTO markers (id, title, content, icon, lat, lng) VALUES (%s, %s, %s, %s, %s, %s)",
            (marker["id"], marker["title"], marker["content"], marker["icon"], marker["position"]["lat"], marker["position"]["lng"]))
    db.commit()
    return

def DeleteMarker(id):
    cursor.execute("DELETE FROM markers WHERE id=%s", (id,))
    db.commit()
    return

def UpdateMarker(marker):
    cursor.execute("UPDATE markers SET title=%s, content=%s, icon=%s, lat=%s, lng=%s WHERE id=%s",
            (marker["title"], marker["content"], marker["icon"], marker["position"]["lat"], marker["position"]["lng"], marker["id"]))
    db.commit()
    return

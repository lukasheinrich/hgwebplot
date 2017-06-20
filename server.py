import requests
import json
from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room, emit

app = Flask('hgwebplot')
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<viewid>', methods = ['GET'])
def view(viewid):
    return render_template('hgview.html', viewid = viewid)

@app.route('/<viewid>', methods = ['POST'])
def update(viewid):
    print request.json
    r = requests.put('https://hgwebplot.firebaseio.com/{}/vega.json'.format(viewid), data = json.dumps(request.json))
    print r.content
    emit('hg_update', request.json, room = viewid, namespace = '/hg')
    return ''

@socketio.on('connect', namespace='/hg')
def connect():
    print('Client connected')

@socketio.on('join', namespace='/hg')
def enter(data):
    print('data',data)
    print('Joining room {}'.format(data['room']))
    join_room(data['room'])

@socketio.on('roomit', namespace='/hg')
def roomit(data):
    print('Emitting to Room: {}'.format(data['room']))
    emit('join_ack', {'data': 'Welcome to the room {}'.format(data['room'])}, room = data['room'], namespace='/hg')

@socketio.on('disconnect', namespace='/hg')
def disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app, host = '0.0.0.0')


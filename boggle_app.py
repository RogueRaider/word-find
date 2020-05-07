from flask import Flask, render_template, request, make_response
from flask_socketio import SocketIO, join_room, leave_room, send, emit
from pprint import pprint
import json
import logging

from game_engine import game_rooms, player, boggle_room

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)


app = Flask(__name__)
app.config['SECRET_KEY'] = 'aqwerqwer!##$@#@$'
app.config['ENV'] = 'development'
app.config['DEBUG'] = True
socketio = SocketIO(app)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/game_hub', methods=['POST'])
def game_hub():
    p_username = request.form["username"]
    p_room_name = request.form["room_name"]
    if server_game_rooms.is_room_active( p_room_name, boggle_room ):
        logger.debug(f"Room { p_room_name } exits" )
    else:
        logger.debug(f"Creating room {p_room_name}")
        server_game_rooms.active_rooms.append(boggle_room(p_room_name))

    boggle_r = server_game_rooms.get_room(p_room_name, boggle_room)

    if boggle_r.is_player_active(p_username):
        logger.info(f"Player {p_username} is reconnecting to session for {p_room_name}")
    else:
        logger.info(f"Player {p_username} is joining session for {p_room_name}")
        boggle_r.players.append(player(p_username))
    resp = make_response(render_template('game_hub.html', room_name=p_room_name))
    resp.set_cookie("username", p_username)
    resp.set_cookie("room", p_room_name)
    return resp

@socketio.on('entering_room')
def enter_room(data):
    logger.debug(f'User {data["username"]} is entering {data["room"]}')
    join_room(data['room'])
    boggle_r = server_game_rooms.get_room(data['room'], boggle_room)
    player_selected = boggle_r.get_player(data['username'])
    player_selected.sid = request.sid
    logger.debug(f'Updated {player_selected.username} with sid {request.sid}')
    emit('successful_entry', {
        'board' : boggle_r.board, 
        'player': player_selected.__dict__ } )    

@socketio.on('connect')
def connection_message():
    print("Welcome new players")

@socketio.on('submit_word')
def process_word(word):
    logger.debug("received " + str(word))
    logger.debug(request)


if __name__ == '__main__':
    server_game_rooms = game_rooms()
    socketio.run(app, port=8000, host="0.0.0.0")
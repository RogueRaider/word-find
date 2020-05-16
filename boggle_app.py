from flask import Flask, render_template, request, make_response
from flask_socketio import SocketIO, join_room, leave_room, send, emit
from pprint import pprint

import json
import logging
import time

from game_engine import game_rooms, player, boggle_room

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)


app = Flask(__name__)
app.config['SECRET_KEY'] = 'aqwerqwer!##$@#@$'
app.config['ENV'] = 'development'
app.config['DEBUG'] = True

socketio = SocketIO(app)

server_game_rooms = game_rooms()


@app.route('/')
def index():
	return render_template('index.html')

@app.route('/game_hub', methods=['POST'])
def game_hub():
    p_username = request.form["username"]
    p_room_name = request.form["room_name"]
    if server_game_rooms.is_room_active( p_room_name, boggle_room ):
        logger.debug(f"Room { p_room_name } exits")
    else:
        logger.debug(f"Creating room {p_room_name}")
        server_game_rooms.active_rooms.append(boggle_room(p_room_name))

    boggle_r = server_game_rooms.get_room(p_room_name, boggle_room)

    if boggle_r.is_player_active(p_username):
        logger.info(f"Player {p_username} is reconnecting to session for {p_room_name}")
    else:
        logger.info(f"Player {p_username} is joining session for {p_room_name}")
    resp = make_response(render_template('game_hub.html', room_name=p_room_name))
    resp.set_cookie("username", p_username)
    resp.set_cookie("room", p_room_name)
    return resp

@socketio.on('connect')
def connection_message():
    logger.debug("new connection established")

@socketio.on('disconnect')
def disconnect_housekeepting():
    logger.debug(f'disconnect detected from {request.sid}')
    for x, room in enumerate(server_game_rooms.active_rooms):
        for y, player in enumerate(room.players):
            if player.sid == request.sid: # and check that game isn't running
                logger.info(f'Removing {player.username} from {room.name}')
                del room.players[y]
        if len(room.players) == 0:
            logger.info(f'Removing empty room {room.name}')
            del server_game_rooms.active_rooms[x]


@socketio.on('entering_room')
def enter_room(data):
    p_username = data['username']
    p_room_name = data['room']
    logger.debug(f'User {p_username} is entering {p_room_name}')

    if server_game_rooms.is_room_active( p_room_name , boggle_room ):
        boggle_r = server_game_rooms.get_room( p_room_name, boggle_room )
        join_room(p_room_name)
    else:
        logger.error(f"Could not find instance of room '{p_room_name}' for player '{p_username}' to enter")
        emit('room_closed')
        return

    if not boggle_r.is_player_active(p_username):
        logger.debug(f'Creating new player "{p_username}"')
        boggle_r.players.append(player(p_username))

    player_selected = boggle_r.get_player(p_username)
    player_selected.sid = request.sid
    logger.debug(f'Updated {player_selected.username} with sid {request.sid}')
    logger.debug(f'Game state {boggle_r.state} game board {boggle_r.board}')
    emit('player_update', {
        'player': player_selected.__dict__
        })
    send_game_update(boggle_r, player_selected.sid)


@socketio.on('game_control')
def handle_control_input(data):
    logger.debug(f'Received control request{data}')

    game = data['game']
    p_room_name = request.cookies['room']
    if not server_game_rooms.is_room_active( p_room_name , boggle_room ):
        logger.error(f"Could not find instance of room '{p_room_name}' to start")
        emit('room_closed')
        return

    boggle_r = server_game_rooms.get_room(p_room_name, boggle_room)

    if boggle_r.state == 'running':
        logger.error(f'Can not start game that is already running')
        return

    if game['state'] == 'start':
        boggle_r.length_seconds  = game['seconds_remaining']
        boggle_r.seconds_remaining = game['seconds_remaining']
        boggle_r.minimum_letters = game['minimum_letters']
        run_game(boggle_r)


@socketio.on('submit_word')
def process_word(word):
    logger.debug("Submitted word received " + str(word))
    p_room_name = request.cookies['room']
    p_sid = request.sid

    if server_game_rooms.is_room_active( p_room_name , boggle_room ):
        boggle_r = server_game_rooms.get_room(p_room_name, boggle_room)
    else:
        logger.error(f"Could not find instance of room '{p_room_name}' to submit word")
        return
    # not sure if this will work well
    player_selected = boggle_r.get_player_by_sid(p_sid)
    player_selected.entries['numbers'].append(word['entry_number'])
    player_selected.entries['words'].append(word['entry_word'])
    word_points = boggle_r.scoring_matrix[len(word['entry_word'])]
    player_selected.entries['points'].append(word_points)
    emit('player_update', { 
        'player': player_selected.__dict__
        })


def run_game(game_room):
    game_room.generate_board()
    game_room.state = 'running'
    send_game_update(game_room)

    for player in game_room.players:
        socketio.emit('player_update', { 
            'player': player.__dict__
            }, room=player.sid)

    end_time = time.time() + game_room.seconds_remaining
    while time.time() < end_time:
        game_room.seconds_remaining = round(end_time - time.time())
        logger.debug(f'Seconds remaining {game_room.seconds_remaining} for {game_room.name}')
        send_game_update(game_room)
        time.sleep(1)
        
    logger.debug(f'Sending last game update')
    send_game_update(game_room)
    game_results = game_room.get_players_final_scores()
    logger.debug(f'Sending game results {game_results}')
    socketio.emit('game_results', game_results, room=game_room.name)
    # reset game
    for player in game_room.players:
        player.entries = {
            'words': [],
            'numbers': [],
            'points': []
        }
    game_room.board = game_room.blank_board
    game_room.state = 'waiting'
    game_room.seconds_remaining = 0
    logger.debug(f'Sending reset game room')
    send_game_update(game_room)



def send_game_update(game_room, sid=None):
    if sid is not None:
        emit('game_update', {
            'game' : {
                'state': game_room.state,
                'board': game_room.board,
                'minimum_letters': game_room.minimum_letters,
                'seconds_remaining': game_room.seconds_remaining,
                'length_seconds': game_room.length_seconds
                }
            },
            room=sid)
    else:
        emit('game_update', {
            'game' : {
                'state': game_room.state,
                'board': game_room.board,
                'minimum_letters': game_room.minimum_letters,
                'seconds_remaining': game_room.seconds_remaining,
                'length_seconds': game_room.length_seconds
                }
            },
            room=game_room.name)

if __name__ == '__main__':
    socketio.run(app, port=8000)

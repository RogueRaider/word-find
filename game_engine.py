import random

class game_rooms:
    def __init__(self):
        self.active_rooms = []

    def is_room_active(self, room_name, room_type):
        for room in self.active_rooms:
            if room.name == room_name and type(room) == room_type:
                return True
        return False

    def get_room(self, room_name, room_type):
        for room in self.active_rooms:
            if room.name == room_name and type(room) == room_type:
                return room
        return None

class player:
    def __init__(self, username):
        self.username = username
        self.sid = None
        self.connected = True
        self.entries = {
            'words': [],
            'numbers': [],
            'points': []
        }

class boggle_room:
    def __init__(self, name):
        self.name = name
        self.players = []
        self.minimum_letters = 4
        self.state = 'waiting'
        self.length_seconds = 120
        self.seconds_remaining = self.length_seconds
        self.blank_board = ['-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-',]
        self.board = self.blank_board
        self.scoring_matrix  = {
            3: 1,
            4: 2,
            5: 4,
            6: 6, 
            7: 10,
            8: 12,
            9: 15,
            10: 20,
            12: 30,
            13: 40,
            14: 50,
            15: 60,
            16: 100
        }

    def is_player_active(self, player_name):
        for player in self.players:
            if player.username == player_name:
                return True
        return False

    def get_player(self, player_name):
        for player in self.players:
            if player.username == player_name:
                return player
        return None

    def get_player_by_sid(self, player_sid):
        for player in self.players:
            if player.sid == player_sid:
                return player
        return None

    def get_players_final_scores(self):
        winning_entries = []
        losing_entries = []
        for player in self.players:
            for entry in player.entries['numbers']:
                # entry gets no points because it's duplicated
                if entry in winning_entries: 
                    winning_entries.remove(entry)
                    losing_entries.append(entry)
                # entry is not duplicated and has not been previously removed    
                elif entry not in losing_entries: 
                    winning_entries.append(entry)

        results = {}
        for player in self.players:
            results[player.username] = {}
            results[player.username]['total_points'] = 0
            results[player.username]['entries'] = {}
            results[player.username]['entries']['words'] = []
            results[player.username]['entries']['points'] = []
            results[player.username]['entries']['numbers'] = []
            for i in range(0, len(player.entries['numbers'])):
                if player.entries['numbers'][i] in winning_entries:
                    results[player.username]['total_points'] += player.entries['points'][i]
                    results[player.username]['entries']['words'].append(player.entries['words'][i])
                    results[player.username]['entries']['points'].append(player.entries['points'][i])
                    results[player.username]['entries']['numbers'].append(player.entries['numbers'][i])
                else:
                    results[player.username]['entries']['words'].append(player.entries['words'][i])
                    results[player.username]['entries']['points'].append(0)
                    results[player.username]['entries']['numbers'].append(player.entries['numbers'][i])
                    

        return results

    def generate_board(self):

        dice_matrix = [
        ['R', 'D', 'E', 'D', 'L', 'I'],
        ['D', 'E', 'Y', 'L', 'V', 'R'],
        ['F', 'K', 'A', 'S', 'P', 'F'],
        ['C', 'P', 'S', 'O', 'H', 'A'],
        ['V', 'R', 'E', 'W', 'H', 'T'],
        ['J', 'B', 'B', 'O', 'O', 'A'],
        ['G', 'A', 'E', 'E', 'N', 'A'],
        ['T', 'O', 'W', 'O', 'A', 'T'],
        ['S', 'E', 'I', 'S', 'O', 'T'],
        ['W', 'E', 'E', 'N', 'G', 'H'],
        ['H', 'N', 'R', 'P', 'L', 'N'],
        ['S', 'U', 'I', 'E', 'E', 'N'],
        ['M', 'U', 'I', 'C', 'H', 'N'],
        ['O', 'U', 'I', 'M', 'C', 'T'],
        ['T', 'R', 'L', 'T', 'E', 'Y'],
        ['I', 'T', 'D', 'Y', 'T', 'S']
        ]

        board = []

        random.shuffle(dice_matrix)
        for die in dice_matrix:
            random.shuffle(die)
            board.append(die[0])

        self.board = board

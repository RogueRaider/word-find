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
        self.entries = {
            'words': [],
            'numbers': [],
            'points': []
        }

class boggle_room:
    def __init__(self, name):
        self.name = name
        self.players = []
        self.minimum_letters = 3
        self.state = 'waiting'
        self.seconds_remaining = 120
        self.blank_board = ['-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-',]
        self.board = self.blank_board
        self.scoring_matrix  = {
            3: 1,
            4: 1,
            5: 2,
            6: 3,
            7: 5,
            8: 11,
            9: 11,
            10: 11,
            12: 11,
            13: 11,
            14: 11,
            15: 11,
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
        for player in self.players:
            for entry in player.entries['numbers']:
                if entry not in winning_entries:
                    winning_entries.append(entry)
                else:
                    winning_entries.remove(entry)
        results = {}
        for player in self.players:
            results[player.username] = {}
            results[player.username]['total_points'] = 0
            results[player.username]['entries'] = {}
            results[player.username]['entries']['words'] = []
            results[player.username]['entries']['points'] = []
            for i in range(0, len(player.entries['numbers'])):
                if player.entries['numbers'][i] in winning_entries:
                    results[player.username]['total_points'] += player.entries['points'][i]
                    results[player.username]['entries']['words'].append(player.entries['words'][i])
                    results[player.username]['entries']['points'].append(player.entries['points'][i])
                else:
                    results[player.username]['entries']['words'].append(player.entries['words'][i])
                    results[player.username]['entries']['points'].append(0)

        return results

    def generate_board(self):

        dice_matrix = [
        ['R', 'D', 'E', 'X', 'L', 'I'],
        ['D', 'E', 'Y', 'L', 'V', 'R'],
        ['F', 'K', 'A', 'S', 'P', 'F'],
        ['C', 'P', 'S', 'O', 'H', 'A'],
        ['V', 'R', 'E', 'W', 'H', 'T'],
        ['J', 'B', 'B', 'O', 'O', 'A'],
        ['G', 'A', 'E', 'E', 'N', 'A'],
        ['T', 'O', 'W', 'O', 'A', 'T'],
        ['S', 'E', 'I', 'S', 'O', 'T'],
        ['W', 'E', 'E', 'N', 'G', 'H'],
        ['H', 'N', 'R', 'Z', 'L', 'N'],
        ['S', 'U', 'I', 'E', 'E', 'N'],
        ['M', 'U', 'I', 'QU', 'H', 'N'],
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

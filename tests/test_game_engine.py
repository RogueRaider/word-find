# Tests can be run from the project root with 'python3 -m unittest discover'

import unittest
from game_engine import game_rooms, player, boggle_room

class TestGameRoomsMethods(unittest.TestCase):

    def test_is_room_active(self):
        br = boggle_room("12345")
        server_game_rooms = game_rooms()
        server_game_rooms.active_rooms.append(br)
        self.assertEqual(True, server_game_rooms.is_room_active("12345", boggle_room))

    def test_get_room(self):
        br = boggle_room("1")
        server_game_rooms = game_rooms()
        self.assertEqual(None, server_game_rooms.get_room("1", boggle_room))
        server_game_rooms.active_rooms.append(br)
        self.assertEqual(server_game_rooms.active_rooms[0], server_game_rooms.get_room("1", boggle_room))

class TestBoggleRoomMethods(unittest.TestCase):

    def test_is_player_active(self):
        br = boggle_room("12345")
        br.players.append(player("matthew"))
        self.assertEqual(True, br.is_player_active("matthew"))

    def test_get_player(self):
        br = boggle_room("12345")
        p = player("matthew")
        br.players.append(p)
        self.assertEqual(p, br.get_player(p.username))

    def test_generate_board(self):
        br = boggle_room("12345")
        self.assertEqual(16, len(br.board))

    def test_get_players_final_scores(self):
        br = boggle_room("test01")
        br.players.append(player("matthew"))
        br.players.append(player("rodney"))
        br.players.append(player("acacia"))
        m = br.get_player("matthew")
        r = br.get_player("rodney")
        a = br.get_player("acacia")

        a.entries = {
            'words': ['figs', 'figs', 'spaceship'],
            'numbers': ['1,2,3,4', '1,3,4,2', '5,4,3,6,2,1,5,3,4'],
            'points': [1, 1, 10]
        }

        r.entries = {
            'words': ['figs', 'apples'],
            'numbers': ['1,2,3,4', '4,5,2,4,8,16'],
            'points': [1, 2]
        }

        m.entries = {
            'words': ['bedroom'],
            'numbers': ['4,5,6,7,2,10,11'],
            'points': [5]
        }

        test_case_01 = {
                      'acacia': {
                        'entries': {
                            'points': [0, 1, 10],
                            'words': ['figs','figs','spaceship', ],
                            'numbers': ['1,2,3,4', '1,3,4,2', '5,4,3,6,2,1,5,3,4']
                            },
                        'total_points': 11
                        },
                     'matthew': {
                        'entries': {
                            'points': [5], 
                            'words': ['bedroom'],
                            'numbers': ['4,5,6,7,2,10,11']
                            }, 
                        'total_points': 5
                        },
                     'rodney': {
                        'entries': {
                            'points': [0, 2], 
                            'words': ['figs', 'apples'],
                            'numbers': ['1,2,3,4', '4,5,2,4,8,16']
                            },
                        'total_points': 2
                        }
                    }

        self.assertEqual(test_case_01, br.get_players_final_scores())

        self.maxDiff = None
        br02 = boggle_room("test02")
        br02.players.append(player("Rodney"))
        br02.players.append(player("Paula"))
        br02.players.append(player("johnf"))
        br02.players.append(player("RUBEUS"))
        br02.players.append(player("Mark"))
        br02.players.append(player("Kendall"))
        br02.players.append(player("Rache"))

        Rodney = br02.get_player("Rodney")
        Paula = br02.get_player("Paula")
        JohnF = br02.get_player("johnf")
        Rubeus = br02.get_player("RUBEUS")
        Mark = br02.get_player("Mark")
        Kendall = br02.get_player("Kendall")
        Rachel = br02.get_player("Rache")

        Rodney.entries = {
                "words": [ "hat", "ton", "ton", "than", "sad", "sad", "sat", "vat", "tan", "tan"],
                "points": [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ],
                "numbers": ["0,5,4", "4,8,9", "4,8,13", "4,0,5,9", "2,5,1", "2,5,6", "7,10,14", "15,10,14", "14,10,9", "14,10,13"]
              }
 
        Paula.entries = {
                "words": ["sat", "hat", "dad", "dads", "adds", "than", "tan", "tan", "tan", "van"],
                "points": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ],
                "numbers": ["2,5,4", "0,5,4", "1,5,6", "1,5,6,2", "5,1,6,7", "4,0,5,9", "4,5,9", "14,10,9", "14,10,13", "15,10,9"]
              }

        JohnF.entries = {
                "words": ["tad", "hat"],
                "points": [1, 1 ],
                "numbers": ["4,5,6", "0,5,4"]
              }

        Rubeus.entries = {
                "words": ["sat", "sands", "sand", "hand", "hands", "hands", "tan", "tan", "tan", "ton", "ton"],
                "points": [1, 2, 1, 1, 2, 2, 1, 1, 1, 1, 1 ],
                "numbers": ["2,5,4", "2,5,9,6,7", "2,5,9,6", "0,5,9,6", "0,5,9,6,7", "0,5,9,6,2", "14,10,13", "14,10,9", "4,5,9", "4,8,9", "4,8,13"]
              }

        Mark.entries = {
                "words": ["not"],
                "points": [1 ],
                "numbers": ["9,8,4"]
              }

        Rachel.entries = {
                "words": ["tan", "tan", "van", "van", "sat", "has", "hat", "had", "hast"],
                "points": [1, 1, 1, 1, 1, 1, 1, 1, 1 ],
                "numbers": ["14,10,9", "14,10,13", "15,10,9", "15,10,13", "7,10,14", "0,5,2", "0,5,4", "0,5,6", "0,5,2,3"]
              }

        Kendall.entries = {
                "words": ["dad", "dads", "dads", "ant", "not", "not", "nor", "sat", "vat", "van", "van", "hat", "toad"],
                "points": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ],
                "numbers": ["1,5,6", "1,5,6,2", "1,5,6,7", "5,9,4", "13,8,4", "9,8,4", "9,8,12", "7,10,14", "15,10,14", "15,10,13", "15,10,9", "0,5,4", "4,8,5,6"]
              }

        test_case_02 = {
            "Rodney": {
              "total_points": 2,
              "entries": {
                "words": ["hat", "ton", "ton", "than", "sad", "sad", "sat", "vat", "tan", "tan"],
                "points": [0, 0, 0, 0, 1, 1, 0, 0, 0, 0 ],
                "numbers": ["0,5,4", "4,8,9", "4,8,13", "4,0,5,9", "2,5,1", "2,5,6", "7,10,14", "15,10,14", "14,10,9", "14,10,13"]
              }
            },
            "Paula": {
              "total_points": 1,
              "entries": {
                "words": ["sat", "hat", "dad", "dads", "adds", "than", "tan", "tan", "tan", "van"],
                "points": [0, 0, 0, 0, 1, 0, 0, 0, 0, 0 ],
                "numbers": ["2,5,4", "0,5,4", "1,5,6", "1,5,6,2", "5,1,6,7", "4,0,5,9", "4,5,9", "14,10,9", "14,10,13", "15,10,9"]
              }
            },
            "johnf": {
              "total_points": 1,
              "entries": {
                "words": ["tad", "hat"],
                "points": [1, 0 ],
                "numbers": ["4,5,6", "0,5,4"]
              }
            },
            "RUBEUS": {
              "total_points": 8,
              "entries": {
                "words": ["sat", "sands", "sand", "hand", "hands", "hands", "tan", "tan", "tan", "ton", "ton"],
                "points": [0, 2, 1, 1, 2, 2, 0, 0, 0, 0, 0 ],
                "numbers": ["2,5,4", "2,5,9,6,7", "2,5,9,6", "0,5,9,6", "0,5,9,6,7", "0,5,9,6,2", "14,10,13", "14,10,9", "4,5,9", "4,8,9", "4,8,13"]
              }
            },
            "Mark": {
              "total_points": 0,
              "entries": {
                "words": ["not"],
                "points": [0 ],
                "numbers": ["9,8,4"]
              }
            },
            "Rache": {
              "total_points": 3,
              "entries": {
                "words": ["tan", "tan", "van", "van", "sat", "has", "hat", "had", "hast"],
                "points": [0, 0, 0, 0, 0, 1, 0, 1, 1 ],
                "numbers": ["14,10,9", "14,10,13", "15,10,9", "15,10,13", "7,10,14", "0,5,2", "0,5,4", "0,5,6", "0,5,2,3"]
              }
            },
            "Kendall": {
              "total_points": 5,
              "entries": {
                "words": ["dad", "dads", "dads", "ant", "not", "not", "nor", "sat", "vat", "van", "van", "hat", "toad"],
                "points": [0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1 ],
                "numbers": ["1,5,6", "1,5,6,2", "1,5,6,7", "5,9,4", "13,8,4", "9,8,4", "9,8,12", "7,10,14", "15,10,14", "15,10,13", "15,10,9", "0,5,4", "4,8,5,6"]
              }
            }
          }

        self.assertEqual(test_case_02, br02.get_players_final_scores())

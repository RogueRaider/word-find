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
        br = boggle_room("12345")
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

        test_case = {'acacia': {'entries': {'points': [0, 1, 10],'words': ['figs','figs','spaceship', ]},'total_points': 11},
                     'matthew': {'entries': {'points': [5], 'words': ['bedroom']}, 'total_points': 5},
                     'rodney': {'entries': {'points': [0, 2], 'words': ['figs', 'apples',]},'total_points': 2}}


        self.assertEqual(test_case, br.get_players_final_scores())

import unittest
from game_engine import game_rooms, player, boggle_room

class TestGameRoomsMethods(unittest.TestCase):

    def test_is_room_active(self):
        br = boggle_room("12345")
        server_game_rooms = game_rooms()
        server_game_rooms.active_rooms.append(br)
        self.assertEqual(True, server_game_rooms.is_room_active("12345", boggle_room))

    def test_get_room(self):
        br = boggle_room("12345")
        server_game_rooms = game_rooms()
        self.assertEqual(None, server_game_rooms.get_room("12345", boggle_room))
        server_game_rooms.active_rooms.append(br)
        self.assertEqual(server_game_rooms.active_rooms[0], server_game_rooms.get_room("12345", boggle_room))

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

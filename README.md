# Boggle

This is a simple game of boggle that can be played by multiple people.

## To Do

* Handle players joining room in the middle of a game
* Build game flow
* Destroy rooms if they have no players left
* Check only unique player names can be added.

## Architecture

When users hit / they are invited to put in a user name and a room name.
This submits a POST request which then puts them into the room.

The username must be unique in the room that was created. If the user leaves then comes back the data must be retained while that room is valid. A user joining multiple times will just broadcast the information.


## Program flow

* Server start
* Client connects and logs in
* Once connection has been established client requests to enter the room
* Server creates room and player instances
* If successful the server sends updates to the player and game objects
* Server sends player data to client
* Client starts game
* Server generates game data
* Client uses interface to create players working entry
* Client handles legal board moves
* Client checks that the entries_numbers is unique
* Client checks working entry is in dictionary
* Client submits the working_entry to the server
* Server adds the entry to the player instance
* Server sends updated player object to the client


## Game flow

1. waiting
2. running
3. waiting


## Player

The player properties
`entries_numbers` used to store js arrays that have been converted to numbers. This is used to make sure each entry is unique.
`entries_words` used to store entered words as simple readable strings


## Managing connection issues

Managing connections with phones is a little tricky. Phone go into standby
very quickly causing socketio to disconnect. We don't know if/when they will
reconnect so it is difficult to know when they should be removed from the
room.

When the phone screen goes blank while waiting the disconnect event is fired.
Then the phone continues to reconnect every few minutes. The SID of the
player continually changes.

Players complete a post request using the index page form. This sets up the
cookie with the 'username' and 'room' keys allowing the connection to
socektio.

Players are added to the server python room instances only through the
"entering_room" socketio message. This attempts to keep the player instances in
sync with the socketio messages.

If the players try to connect to rooms that don't exist they are sent back to
the index page.
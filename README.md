# Boggle

This is a simple game of boggle that can be played by multiple people.

## Architecture

When users hit / they are invited to put in a user name and a room name.
This submits a POST request which then puts them into the room.

The username must be unique in the room that was created. If the user leaves then comes back the data must be retained while that room is valid. A user joining multiple times will just broadcast the information.



## Player

The player properties
`entries_numbers` used to store js arrays that have been converted to numbers. This is used to make sure each entry is unique.
`entries_words` used to store entered words as simple readable strings

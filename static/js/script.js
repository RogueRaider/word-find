const parseCookie = str =>
  str
    .split(';')
    .map(v => v.split('='))
    .reduce((acc, v) => {
      acc[decodeURIComponent(v[0].trim())] = decodeURIComponent(v[1].trim());
      return acc;
    }, {});

set_valid_word_list(english_word_list);
var lower_thresh = 0.7;

var game = {
  "state": "waiting",
  "minimum_letters": 3,
  "board": {}
}

var game_message_handler;

var player = {
  "entries_numbers": [],
  "entries_words": []
}

var working_entry = [];

var legal_letter_add_matrix = {
  0: [1, 5, 4],
  1: [0, 4, 5, 6, 2],
  2: [1, 3, 5, 6, 7],
  3: [2, 6, 7],
  4: [0, 1, 5, 8, 9],
  5: [0, 1, 2, 4, 6, 8, 9, 10],
  6: [1, 2, 3, 5, 7, 9, 10, 11],
  7: [2, 3, 6, 10, 11],
  8: [4, 5, 9, 12, 13],
  9: [4, 5, 6, 8, 10, 12, 13, 14],
  10: [5, 6, 7, 9, 11, 13, 14, 15],
  11: [6, 7, 10, 14, 15],
  12: [8, 9, 13],
  13: [8, 9, 10, 12, 14],
  14: [9, 10, 11, 13, 15],
  15: [10, 11, 14]
}

var socket = io();

$(document).ready(function(){

  var cookie = parseCookie(document.cookie);

  game.state = "running"

  socket.on('connect', function() {
    data = {
      'username': cookie.username,
      'room': cookie.room
    };
    socket.emit('entering_room', data);
  });

  socket.on('successful_entry', function(data) {
    console.log(data)
    game.board = data.board
    player = data.player
    draw_board(game.board)
    $("#b_username").text(player.username)
  });
});

function b_submit () {
  var submitted_word = $("#working_entry").attr("value").toLowerCase();
  var stringed_working = working_entry.toString()
  if (player.entries_numbers.includes(stringed_working)) {
    entry_reset("Already entered '" + submitted_word + "'");
    return;
  }
  var word_check = find_similar(submitted_word, lower_thresh)[0];
  if (word_check.includes(submitted_word)) {
    player.entries_numbers.push(stringed_working);
    entry_reset("Accepted '" + submitted_word + "'");
    socket.emit('submit_word', {
      'entry_word' : submitted_word,
      'entry_number' : stringed_working
      }
    );
  } else {
    entry_reset("Sorry '" + submitted_word + "' is not a legal word ");
  }
}

function b_reset () {
  entry_reset("Entry Reset");
}

function entry_reset (game_message) {
  display_game_message(game_message);
  working_entry = [];
  $("#working_entry").attr("value", "");
  $(".selected_input").removeClass("selected_input");
  $("#b_submit").prop("disabled", true);
}

function b_click (board_number) {
  if (game.state != "running") {
    console.log("The game isn't running");
    return;
  }
  if (working_entry.length == 0) {
    update_working_entry(board_number)
  } else if (check_letter_selection_legal(board_number) && ! working_entry.includes(board_number)){
    update_working_entry(board_number)
  } else {
    display_game_message("Illegal selection")
    $("#b_" + board_number).toggleClass("illegal_selection");
    setTimeout( function () {
      $("#b_" + board_number).toggleClass("illegal_selection");
    }, 1000);
  }
}

function update_working_entry (board_number) {
  working_entry.push(board_number);
  $("#b_" + board_number).toggleClass("selected_input");
  var working_entry_string = "";
  for (var i = 0; i < working_entry.length; i++) {
    working_entry_string += game.board[working_entry[i]];
  }
  $("#working_entry").attr("value", working_entry_string);
  if ( working_entry.length >= game.minimum_letters ) {
    $("#b_submit").removeAttr("disabled");
  }

}

function display_game_message (message) {
  clearTimeout(game_message_handler);
  $("#game_message").text(message);
  game_message_handler = setTimeout(function(){
      $("#game_message").text("");
  }, 1000);  
}

function check_letter_selection_legal (board_number) {
  var last_number = working_entry[working_entry.length - 1];
  var legal_numbers = legal_letter_add_matrix[last_number];
  return legal_numbers.includes(board_number);
}


function draw_board (board) {
  for (var i = board.length - 1; i >= 0; i--) {
    var b_id = "#b_" + i;
    $(b_id).attr("value", board[i])
  }
}

function update_submitted_words (words) {
  for (var i = words.length - 1; i >= 0; i--) {
    words[i]
  }
}


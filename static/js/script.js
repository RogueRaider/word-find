const parseCookie = str =>
  str
    .split(';')
    .map(v => v.split('='))
    .reduce((acc, v) => {
      acc[decodeURIComponent(v[0].trim())] = decodeURIComponent(v[1].trim());
      return acc;
    }, {});

var game;
var room;
var player;
var game_message_handler;
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

var dictionary = new Typo("en_GB", false, false, { dictionaryPath: "static/js/dictionaries", asyncLoad: true, loadedCallback: function(data) { console.log("dictionary ready");}} );

$(document).ready(function(){

  var cookie = parseCookie(document.cookie);

  socket.on('connect', function() {
    data = {
      'username': cookie.username,
      'room': cookie.room
    };

    socket.emit('entering_room', data);

  });
});


socket.on('player_update', function (data) {
  player_update(data.player);
});

socket.on('game_update', function (data) {
  game_update(data.game);
});

socket.on('room_update', function (data) {
  room_update(data.room);
})

socket.on('game_results', function (data) {
  console.log('received game results');
  console.log(data);
  var results_table = "";
  for (var player in data) {
    var p = data[player];
    results_table += '<tr class="result_section"><td>' + player + '</td><td>' + p.total_points + '</td></tr>'
    for (var i = p.entries.words.length - 1; i >= 0; i--) {
      var row = '<tr class="result_row"><td>' + p.entries.words[i] + '</td><td>' + p.entries.points[i] + '</td><td>' + p.entries.numbers[i] + '</td></tr>';
      results_table += row;
    }
  }
  $('#results_table').empty();
  $('#results_table').html(results_table);
  $('#results-modal').modal('show');
});

socket.on('room_closed', function (data) {
  console.log('The room is closed, redirecting to room entry');
  alert('Sorry, the room is closed. Please start again.');
  window.location.replace('/');
})

function b_submit () {
  var submitted_word = $("#working_entry").attr("value").toLowerCase();
  var stringed_working = working_entry.toString()
  if (player.entries.numbers.includes(stringed_working)) {
    entry_reset("Already entered '" + submitted_word + "'");
    return;
  }
  if (dictionary.check(submitted_word)) {
    $("#working_entry").toggleClass("submit_success");
    setTimeout( function () {
      $("#working_entry").toggleClass("submit_success");
    }, 1000);
    player.entries.numbers.push(stringed_working);
    entry_reset("Accepted '" + submitted_word + "'");
    socket.emit('submit_word', {
      'entry_word' : submitted_word,
      'entry_number' : stringed_working,
      'username' : player.username
      }
    );
  } else {
    $("#working_entry").toggleClass("submit_fail");
    setTimeout( function () {
      $("#working_entry").toggleClass("submit_fail");
    }, 1000);
    entry_reset("Sorry '" + submitted_word + "' is not a legal word ");
  }
}

function b_start () {
  console.log('requesting game start')
  console.log(game);
  switch (game.state) {
    case 'waiting':
      console.log('Starting game');
      var game_length = parseInt($('#game_length').children("option:selected").val(), 10)
      var minimum_letters = parseInt($('#minimum_letters').children("option:selected").val(), 10)
      console.log(minimum_letters)
      socket.emit('game_control', {'game': {
        'state': 'start',
        'seconds_remaining': game_length,
        'minimum_letters': minimum_letters
      }});
      break;
    case 'running':
      console.log('Game is already running');
      break;
    default:
      console.log('Unknown game state returned')
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
  if ( working_entry_string.length >= game.minimum_letters ) {
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

function player_update (player_data) {
  console.log('updating player')
  console.log(player_data);
  player = player_data
  var table_rows;
  for (var i = player_data.entries.words.length - 1; i >= 0; i--) {
    var row = '<tr><td>' + player_data.entries.words[i] + '</td><td class="word_points">' + player_data.entries.points[i] + '</td></tr>';
    table_rows += row;
  }
  $("#b_username").text(player_data.username);
  $('#submitted_words').empty();
  $('#submitted_words').html(table_rows);
}

function room_update (room_data) {
  console.log('updating room');
  console.log(room_data);
  room = room_data;
  var table_rows;
  for (var i = room_data.players.length - 1; i >= 0; i--) {
    var row = '<tr><td>' + room_data.players[i].username + '</td><td>' + room_data.players[i].connected + '</td></tr>';
    table_rows += row;
  }
  $('#players_in_room').html(table_rows)
}

function game_update (game_data) {
  console.log('updating game');
  console.log(game_data);
  game = game_data;
  $('#clock').text(game.seconds_remaining)
  $('#minimum_letters').val(game.minimum_letters)
  $('#game_length').val(game.length_seconds)
  draw_board(game.board)
  if ( game.state == "running" ) {
    $("#b_start").prop("disabled", true);
  } else {
    $('#b_start').removeAttr("disabled");
  }
  if ( game.seconds_remaining == 0 ) {
    entry_reset("Game is finished")
  }
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


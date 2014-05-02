// array if all active elements on the canvas
var canvas_directory = new Array();

// static final values for canvas dimensions 
var CANVAS_WIDTH = 6;
var CANVAS_HEIGHT = 5;

stageid = null;

// stage named, to be chosen by the user
var CANVAS_NAME = 'STAGE NOT NAMED';

var CURRENT_ACTION = '';

var currentElement = "block";

function resizeCanvas(width, height) {
  // Process to verify use of integers
  if (!isNaN(parseInt(width)))
    CANVAS_WIDTH = parseInt(width);
  if (!isNaN(parseInt(height)))
    CANVAS_HEIGHT = parseInt(height);
  $('#allrows').html( '' );
  init_canvas();
}


// initialize all the divs for the canvas
function init_canvas() {
  // initialtize draggable start tiles 
  // $("<div id='elements-start' class='elements'>start</div>").data('element-type', 'start-type').appendTo( '#elements-start-slot' ).draggable({
  //   revert: true,
  //   helper: 'clone'
  // });

  // // initialize draggable goal tiles
  // $("<div id='elements-goal' class='elements'>goal</div>").data('element-type', 'goal-type').appendTo( '#elements-goal-slot' ).draggable({
  //   revert: true,
  //   helper: 'clone'
  // });

  // // initialize draggable block tiles
  // $("<div id='elements-block' class='elements'>block</div>").data('element-type', 'block-type').appendTo( '#elements-block-slot' ).draggable({
  //   revert: true,
  //   helper: 'clone'
  // });

  // Clear the canvas_directory
  canvas_directory = new Array();

  var box_width = 100 / CANVAS_WIDTH;

  // add the #canvas-row divs in '#allrows'
  for (var y = 0; y < CANVAS_HEIGHT; y++) {
    // unique row id
    var div_id = "row_" + y

    // common #canvas-row class
    var canvas_row_class = 'canvas-row';

    // add #canvas-first-row to first row to help with positioning
    if (y == 0) {
      canvas_row_class = 'canvas-row canvas-first-row'
    } 

    // add the div with the specified id and classes to #allrows
    $("<div id='" + div_id + "' class='" + canvas_row_class + "'></div>").appendTo( '#allrows' );

    // for each row, add the droppable elements 
    for (var x = 0; x < CANVAS_WIDTH; x++) {

      // text to be in the tile
      //var tile_text = "(" + x + " , " + y + ")";
      var tile_text = "";

      var canvas_col_class = 'canvas-droppable';
      if (x == 0) {
        canvas_col_class += ' canvas-first-col';
      }

      // add the droppable div with the specified text
      $("<div class='" + canvas_col_class + "' style='width:" + box_width + "%;'>" + tile_text + "</div>").data( {'coordinates': [x, y]} ).appendTo('#' + div_id).droppable({
        accept: '.elements',
        hoverClass: 'hovered',
      });

      // Set height equal to width
      $(".canvas-droppable").height($(".canvas-droppable").width());
    }
  }

  // add click event to each div
  $('.canvas-droppable').click(function() {
    var placedClass = "placed-element-" + currentElement;
    var coordinates = $(this).data('coordinates');
    if ($(this).hasClass(placedClass)) {
      $(this).removeClass(placedClass);
      $.each(canvas_directory, function(i){
        if(canvas_directory[i].coordinates === coordinates) {
          canvas_directory.splice(i,1);
        }
      });
    } else {
      $(this).removeClass();
      $.each(canvas_directory, function(i){
        if(canvas_directory[i].coordinates === coordinates)
          canvas_directory.splice(i,1);
      });
      $(this).addClass("canvas-droppable ui-droppable");
      $(this).addClass(placedClass);
      // create a canvas_node object and add to the canvas directory
      canvas_directory.push(new canvas_node(currentElement + '-type', $(this).data('coordinates')));
    }
  });
}

// Set height equal to width every tim
window.addEventListener("resize", function(e) { $(".canvas-droppable").height($(".canvas-droppable").width()); });

// Loads a saved stage into memory via JSON data (passed in via Django templating)
// Also saves the stage ID so that you don't create a new stage every time you save
function load_stage(json_data) {
  data = jQuery.parseJSON(json_data);
  resizeCanvas(data.width, data.height);
  var stage_data = (data.data).replace(/(\\n|\n)+/g, '');
  stageid = data.stageid;
  $('.canvas-droppable').each(function(i) {
    $(this).removeClass();
    $(this).addClass("canvas-droppable ui-droppable");
    switch(stage_data.charAt(i)) {
      case 'S':
        $(this).addClass("placed-element-start");
        canvas_directory.push(new canvas_node('start-type', $(this).data('coordinates')));
        break;
      case 'E':
        $(this).addClass("placed-element-goal");
        canvas_directory.push(new canvas_node('goal-type', $(this).data('coordinates')));
        break;
      case '#':
        $(this).addClass("placed-element-block");
        canvas_directory.push(new canvas_node('block-type', $(this).data('coordinates')));
        break;
      case 'x':
        $(this).addClass("placed-element-enemy");
        canvas_directory.push(new canvas_node('enemy-type', $(this).data('coordinates')));
        break;
    }
  });
}


// canvas node objects with a specified element type and its coordinate
function canvas_node(element_type, coordinates) {
  this.element_type = element_type;
  this.coordinates = coordinates;
}

// grab the x-coordinate of the given coordinates
function getX(coords) {
  return coords[0];
}

// grab the y-coordinate of the given coordinates
function getY(coords) {  
  return coords[1];
}

// renders via loading the stage into the database 
// action is either "play" or "save"

function setStageName(action) {
  CURRENT_ACTION = action;
  if (stageid == null)
    $( "#stagename-dialog-form" ).modal( "show" );
  else
    renderStage(action);
}

function renderStage(action) {

  // create two-dimensional array with dimensions: CANVAS_WIDTH x CANVAS_HEIGHT
  var stage_data_arr = new Array(CANVAS_HEIGHT);
  for (var i = 0; i < CANVAS_HEIGHT; i++) {
    stage_data_arr[i] = new Array(CANVAS_WIDTH);
  }

  // init the 2d-array with a single space (representing open spot)
  // if a element actually exists there, it will be overwritten
  for (var i = 0; i < CANVAS_HEIGHT; i++) {
    for (var j = 0; j < CANVAS_WIDTH; j++) {

      stage_data_arr[i][j] = " ";
    }
  }

  var num_start = 0;
  var num_end = 0;

  // for each element in the directory, overwrite the 2d-array
  for (var i = 0; i < canvas_directory.length; i++) {
    // grab the element-type and the coordinates
    var element = canvas_directory[i].element_type;
    var coordinates = canvas_directory[i].coordinates;

    // set the correct type
    elm = "";
    if (element == "start-type") {
      elm = "S";
      num_start += 1;
    } else if (element == "goal-type") {
      elm = "E";
      num_end += 1;
    } else if (element == "block-type") {
      elm = "#";
    } else if (element == "enemy-type") {
      elm = "x";
    } else {
      console.log("ERROR: Invalid type on map");
    }

    // grab individual coordinates
    var xcoord = getX(coordinates);
    var ycoord = getY(coordinates);

    // update the 2d array
    // x-y are reversed due to the ordering of the rows and columns
    stage_data_arr[ycoord][xcoord] = elm;
  }

  // read the finished the 2d array and build a string representation
  var string_out = "";
  for (var y = 0; y < CANVAS_HEIGHT; y++) {
    for (var x = 0; x < CANVAS_WIDTH; x++) {
      // append to already calculated string
      string_out += stage_data_arr[y][x];
    }
    // new line for each row
    string_out += "\n";
  }

  // console.log(string_out);

  // Check that there is exactly one start position and at least one end position
  if (num_start == 1 && num_end > 0) {
    // all data to be sent in the request: width, height, data
    // stage owner managed by django, so we don't need it here
    var stage_width = CANVAS_WIDTH;
    var stage_height = CANVAS_HEIGHT;
    var stage_data = string_out;
    var stage_name = CANVAS_NAME;

    // fire of the json request to load the database
    json_request( "/stage/render", 
      { width: stage_width, height: stage_height, name: stage_name, data: stage_data, id: stageid }, 
      function(data) { 
        return handle_render_response(data, action);
      }, 
      function(xhr, status, error) { 
        //var err = eval("(" + xhr.responseText + ")");
        //console.log(xhr.responseText); 
        //console.log(status);
      });
  } else {
    // If it doesn't, send an alert. (Make sure it's an alert and not console.log so a customer sees it)
    if (num_start == 0) 
      alert("You don't have a start element!");
    else if (num_start > 1) 
      alert("You can only have one start element!");
    if (num_end == 0) 
      alert("You don't have any goal elements!");
  }
  return false;
}

function handle_render_response(data, action) {
  if (action == "play") {
    location.href = '/game/game.html?stageid=' + data.stageid;
  }
}

function json_request(page, dict, success, failure) {
  $.ajax({
    type: 'POST',
    url: page,
    data: JSON.stringify(dict),
    contentType: "application/json",
    dataType: "json",
    success: success,
    error: failure
  });
}

function rate(stage, rating, user) {
  if (!(user in stage.rated)){
    stage.rating += rating;
    stage.rated[user] = rating;
  } else{
    if (rating == stage.rated[user]){
      stage.rated[user] = 0;
    } else{
      stage.rated[user] = rating;
    }
  }
  print(stage.rating);
}

function clearStage() {
  $('.canvas-droppable').each( function() {
    $(this).removeClass();
    $(this).addClass("canvas-droppable ui-droppable");
  });
  canvas_directory = new Array();
}

$(function () {
  $('#savebutton').click(function() { setStageName("save"); });
  $('#renderbutton').click(function() { setStageName("play"); });
  $('#restartbutton').click(function() { clearStage(); });

  $('#elements-start-slot').click(function() {
    currentElement = "start";
    $('.elements-slot-current').attr('id', 'elements-current-start');
  });
  $('#elements-goal-slot').click(function() {
    currentElement = "goal";
    $('.elements-slot-current').attr('id', 'elements-current-goal');
  });
  $('#elements-block-slot').click(function() {
    currentElement = "block";
    $('.elements-slot-current').attr('id', 'elements-current-block');
  });
  $('#elements-enemy-slot').click(function() {
    currentElement = "enemy";
    $('.elements-slot-current').attr('id', 'elements-current-enemy');
  });
});


// this code is run to initialize dialog form for change stage dimensions
$(function() {

//  $( "#stagename-dialog-form" ).dialog({
//    autoOpen: false,
//    height: 300,
//    width: 350,
//    modal: true,
//    buttons: {
//      "Submit": function() {
//        CANVAS_NAME = stagename.value;
//        $( this ).dialog( "close" );
//        renderStage(CURRENT_ACTION);
//      }
//    }
//  });

//  $( "#dialog-form" ).dialog({
//    autoOpen: false,
//    height: 300,
//    width: 350,
//    modal: true,
//    buttons: {
//      "Set the dimensions": function() {
//        resizeCanvas(width.value, height.value);
//        $( this ).dialog( "close" );
//      },
//      Cancel: function() {
//        $( this ).dialog( "close" );
//      }
//    },
//    close: function() {
//      //allFields.val( "" ).removeClass( "ui-state-error" );
//    }
//  });

//  $( "#set-dimensions" )
//    .button()
//    .click(function() {
//      $( "#dialog-form" ).dialog( "open" );
//  });

  function hideModal(modalwindow){
    $(modalwindow).modal('hide');
  }

  $("#resize").click(function(e) {
    e.preventDefault();
    resizeCanvas(width.value, height.value);
    hideModal("#resizeModal");
  });

  $("#setName").click(function(e) {
    e.preventDefault();
    CANVAS_NAME = stagename.value;
    hideModal("#stagename-dialog-form");
    renderStage(CURRENT_ACTION);
  });
});

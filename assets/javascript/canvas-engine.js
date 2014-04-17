// array if all active elements on the canvas
var canvas_directory = new Array();

// static final values for canvas dimensions 
var CANVAS_WIDTH = 6;
var CANVAS_HEIGHT = 5;

// initialize all the divs for the canvas
function init_canvas() {
  // initialtize draggable start tiles 
  $("<div id='elements-start' class='elements'>start</div>").data('element-type', 'start-type').appendTo( '#elements-start-slot' ).draggable({
    cursor: 'move',
    revert: true,
    helper: 'clone'
  });

  // initialize draggable goal tiles
  $("<div id='elements-goal' class='elements'>goal</div>").data('element-type', 'goal-type').appendTo( '#elements-goal-slot' ).draggable({
    cursor: 'move',
    revert: true,
    helper: 'clone'
  });

  // initialize draggable block tiles
  $("<div id='elements-block' class='elements'>block</div>").data('element-type', 'block-type').appendTo( '#elements-block-slot' ).draggable({
    cursor: 'move',
    revert: true,
    helper: 'clone'
  });

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
      var tile_text = "(" + x + " , " + y + ")";

      var canvas_col_class = 'canvas-droppable';
      if (x == 0) {
        canvas_col_class += ' canvas-first-col';
      }

      // add the droppable div with the specified text
      $("<div class='" + canvas_col_class + "'>" + tile_text + "</div>").data( {'coordinates': [x, y]} ).appendTo('#' + div_id).droppable({
        accept: '.elements',
        hoverClass: 'hovered',
        drop: handleElementDrop
      });
    }
  }
}

// canvas node objects with a specified element type and its coordinate
function canvas_node(element_type, coordinates) {
  this.element_type = element_type;
  this.coordinates = coordinates;
}

// called anytime a tile is dropped onto the canvas
function handleElementDrop(event, ui) {
  // grab the coordinates and the element type of the dropped tile
  var coordinates = $(this).data( 'coordinates' );
  var element_type = ui.draggable.data ( 'element-type' );

  // draggable features
  ui.draggable.position( { of: $(this), my: 'left top', at: 'left top' } );
  ui.draggable.draggable( 'option', 'revert', false );

  if (element_type == 'start-type') {  // start-type element
    // add tile to canvas slot with darkened color
    $( this ).addClass( "placed-elements-screen" ).html("start");
    $( this ).css( "background", "#666" );

    // empty the elements slot 
    $('#elements-start-slot').html( '' );

    // create a new tile in the elements slots
    $("<div id='elements-start' class='elements'>start</div>").data('element-type', 'start-type').appendTo( '#elements-start-slot' ).draggable({
    cursor: 'move',
    revert: true,
    helper: 'clone'
  });
  } else if (element_type == 'goal-type') {  // goal-type element
    // add tile to canvas slot with darkened color
    $( this ).addClass( "placed-elements-screen" ).html("goal");
    $( this ).css( "background", "#666" );

    // empty the elements slot
    $('#elements-goal-slot').html( '' );

    // create a new tile in the elements slots
    $("<div id='elements-goal' class='elements'>goal</div>").data('element-type', 'goal-type').appendTo( '#elements-goal-slot' ).draggable({
    cursor: 'move',
    revert: true,
    helper: 'clone'
  });
  } else if (element_type == 'block-type') { // block-type element
    // add tile to canvas slot with darkened color
    $( this ).addClass( "placed-elements-screen" ).html("block");
    $( this ).css( "background", "#666" );

    // empty the elements slot
    $('#elements-block-slot').html( '' );

    // create a new tile in the elements slots
    $("<div id='elements-block' class='elements'>block</div>").data('element-type', 'block-type').appendTo( '#elements-block-slot' ).draggable({
    cursor: 'move',
    revert: true,
    helper: 'clone'
  });
  } else {
    // should NOT reach here
    alert("ERROR: incorrect element type has been dropped");
  }

  // create a canvas_node object and add to the canvas directory
  canvas_directory.push(new canvas_node(element_type, coordinates));    
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
function renderStage() {

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

  // for each element in the directory, overwrite the 2d-array
  for (var i = 0; i < canvas_directory.length; i++) {
    // grab the element-type and the coordinates
    var element = canvas_directory[i].element_type;
    var coordinates = canvas_directory[i].coordinates;

    // set the correct type
    elm = "";
    if (element == "start-type") {
      elm = "S";
    } else if (element == "goal-type") {
      elm = "E";
    } else if (element == "block-type") {
      elm = "#";
    } else {
      alert("ERROR");
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

  // alert(string_out);

  // all data to be sent in the request: width, height, data
  // stage owner managed by django, so we don't need it here
  var stage_width = CANVAS_WIDTH;
  var stage_height = CANVAS_HEIGHT;
  var stage_data = string_out;

  // fire of the json request to load the database
  json_request( "/stage/render", 
    { width: stage_width, height: stage_height, data: stage_data }, 
    function(data) { 
      return handle_render_response(data);
    }, 
    function(xhr, status, error) { 
      //var err = eval("(" + xhr.responseText + ")");
      //alert(xhr.responseText); 
      alert(status);
    });
  return false;
}

// add a button link to the playable stage -- should fix this
function handle_render_response(data) {
  alert(data.stageid);
  var stage_link = '/game/game.html';
  $("<form action='" + stage_link + "' method='get'><input type='hidden' name='stageid' value='" + data.stageid + "'/> <button id='play-button' class='navbutton'>Play stage!</button> </form>").appendTo('#play-button-position');
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

function rate(stage, rating) {
  stage.rating += rating;
  print(stage.rating);
}

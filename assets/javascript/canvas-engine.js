// array if all active elements on the canvas
var canvas_directory = new Array();

// static final values for canvas dimensions 
var CANVAS_WIDTH = 6;
var CANVAS_HEIGHT = 5;

var currentElement = "block";

function resizeCanvas(width, height) {
  CANVAS_WIDTH = width;
  CANVAS_HEIGHT = height;
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
      $("<div class='" + canvas_col_class + "'>" + tile_text + "</div>").data( {'coordinates': [x, y]} ).appendTo('#' + div_id).droppable({
        accept: '.elements',
        hoverClass: 'hovered',
        // drop: handleElementDrop
      });
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
          return false;
        }
      });
    } else {
      $(this).removeClass();
      $(this).addClass("canvas-droppable ui-droppable");
      $(this).addClass(placedClass);
      // create a canvas_node object and add to the canvas directory
      canvas_directory.push(new canvas_node(currentElement + '-type', $(this).data('coordinates')));
    }
  });
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
    $( this ).addClass("placed-element-start");

    // empty the elements slot 
    $('#elements-start-slot').html( '' );

    // create a new tile in the elements slots
    $("<div id='elements-start' class='elements'>start</div>").data('element-type', 'start-type').appendTo( '#elements-start-slot' ).draggable({
    revert: true,
    helper: 'clone'
  });
  } else if (element_type == 'goal-type') {  // goal-type element
    // add tile to canvas slot with darkened color
    $( this ).addClass( "placed-element-goal" );

    // empty the elements slot
    $('#elements-goal-slot').html( '' );

    // create a new tile in the elements slots
    $("<div id='elements-goal' class='elements'>goal</div>").data('element-type', 'goal-type').appendTo( '#elements-goal-slot' ).draggable({
    revert: true,
    helper: 'clone'
  });
  } else if (element_type == 'block-type') { // block-type element
    // add tile to canvas slot with darkened color
    $( this ).addClass( "placed-element-block" );

    // empty the elements slot
    $('#elements-block-slot').html( '' );

    // create a new tile in the elements slots
    $("<div id='elements-block' class='elements'>block</div>").data('element-type', 'block-type').appendTo( '#elements-block-slot' ).draggable({
    revert: true,
    helper: 'clone'
  });
  } else {
    // should NOT reach here
    console.log("ERROR: incorrect element type has been dropped");
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
// action is either "play" or "save"
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
      console.log("ERROR");
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

  // all data to be sent in the request: width, height, data
  // stage owner managed by django, so we don't need it here
  var stage_width = CANVAS_WIDTH;
  var stage_height = CANVAS_HEIGHT;
  var stage_data = string_out;

  // fire of the json request to load the database
  json_request( "/stage/render", 
    { width: stage_width, height: stage_height, data: stage_data }, 
    function(data) { 
      return handle_render_response(data, action);
    }, 
    function(xhr, status, error) { 
      //var err = eval("(" + xhr.responseText + ")");
      //console.log(xhr.responseText); 
      //console.log(status);
    });
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
  $('#savebutton').click(function() { renderStage("save"); });
  $('#renderbutton').click(function() { renderStage("play"); });
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
});


// this code is run to initialize dialog form for change stage dimensions
$(function() {
  $( "#dialog-form" ).dialog({
    autoOpen: false,
    height: 300,
    width: 350,
    modal: true,
    buttons: {
      "Set the dimensions": function() {
        resizeCanvas(width.value, height.value);
        $( this ).dialog( "close" );
      },
      Cancel: function() {
        $( this ).dialog( "close" );
      }
    },
    close: function() {
      //allFields.val( "" ).removeClass( "ui-state-error" );
    }
  });

  $( "#set-dimensions" )
    .button()
    .click(function() {
      $( "#dialog-form" ).dialog( "open" );
  });
});
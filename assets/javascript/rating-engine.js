// $(function () {
//   $('#upvote').click(function() { castVote("up"); });
//   $('#downvote').click(function() { castVote("down"); });
// });


function castVote(vote_dir, stageid) {

    // need to change this
    var stage_id = stageid;

    json_request( "/stage/vote", 
    { stageid: stage_id, vote: vote_dir}, 
    function(data) { 
      return handle_vote_response(data);
    }, 
    function(xhr, status, error) { 
      //var err = eval("(" + xhr.responseText + ")");
      //console.log(xhr.responseText); 
      //console.log(status);
    });
}

function handle_vote_response(data) {
  var new_score = "<span class='fui-heart'></span> " + data.new_rating;
  $( '#rating' ).html(new_score);
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
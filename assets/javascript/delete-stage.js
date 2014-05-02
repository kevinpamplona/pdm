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

function handle_delete_response(data) {
	location.href = '/game/';
}

function delete_stage(sid) {
	json_request( "/stage/delete",
				  { stage_id: sid },
				  function(data) {
				  	return handle_delete_response(data);
				  },
				  function(xhr, status, error) {
			          // hopefully this is not reached	  
				  });
}

$(function () {
	var stageid = $("#deletebutton").val()
    $('#deletebutton').click(
        function() { 
        	delete_stage(stageid); 
        });
});

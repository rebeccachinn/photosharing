$(document).ready(function() {
	var socket = io.connect('http://127.0.0.1:5000');

	//keeps chat box scrolled to bottom
	$('#messages').scrollTop($('#messages')[0].scrollHeight);

	socket.on('connect', function() {
		// socket.send('User has connected!');
		console.log("User connected");
		//
	});

	
	socket.on('message', function(msg) {
		console.log('Received message');
		var block = getMessageBlock(msg);
		$("#messages").append(block);
		$('#messages').scrollTop($('#messages')[0].scrollHeight);

	});

	$('#sendbutton').on('click', function() {
		socket.send($('#myMessage').val(),$('#client_room_id').text());
		$('#myMessage').val('');
		console.log("message sent!")
	});


	//enter -- > submit
	$('#myMessage').keypress(function (e) {
	  if (e.which == 13) {
	    $('#sendbutton').click();
	    return false;
	  }
	});

	//returns html template literal of new block
	function getMessageBlock(msg){
		var msgContent = msg.messageContent, author = msg.author, date = msg.date


		var newDiv = document.createElement('div');

		newDiv.innerHTML = `
			<article class='media content-section'>
	        <div class='media-body'>
	          <div class='article-metadata'>
	            <a class='mr-2' href='{{ url_for("clients.client_progress", ${author} )}}'>${author}</a>
	            <small class='text-muted'>${date}</small>
	          </div>
	          <p class="article-content">${msgContent}</p>
	        </div>
	      </article>
		`;
		return newDiv
	}

});

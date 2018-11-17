$(document).ready(function() {
	var socket = io.connect('http://127.0.0.1:5000');
	socket.on('connect', function() {
		// socket.send('User has connected!');
		console.log("User connected");
	});
	socket.on('message', function(msg) {
		// $("#messages").append('<li>' + msg +'</li>');
		location.reload()
		console.log('Received message');
	});

	$('#sendbutton').on('click', function() {
		socket.send($('#myMessage').val());
		$('#myMessage').val('');
		console.log("message sent!")
	});


	// const realFileBtn = $("#real-file");
	// const customBtn = $("#custom-button");
	// const customTxt = $("#custom-text");

	// customBtn.click(function() {
	// 	realFileBtn.click();
	// })

	// realFileBtn.change(function(){
	// 	if (realFileBtn.val()){
	// 		console.log(realFileBtn.val());
	// 		customTxt.html(realFileBtn.val().match(/[\/\\]([\w\d\s\.\-\(\)]+)$/)[1]);
	// 	}
	// })
});

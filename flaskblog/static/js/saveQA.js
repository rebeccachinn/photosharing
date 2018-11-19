$(document).ready(function() {
	var client_room_id = $('#client_room_id').text()

	$("#openSaveQAModal").click(function(){


		var latestMessage = $.get('/get_latest_message', {
        	"client_room_id" : client_room_id ,
      	})
      		.done(function(){
      			var latestMessageText = latestMessage.responseJSON.message;
      			var currentAnswer = $("#myMessage").val();
      			$("#questionTextbox").text(latestMessageText);
      			$("#answerTextbox").text(currentAnswer);
      		});
      	})

	$("#saveQA").click(function(){
		var question= $("#questionTextbox").text();
		var answer = $("#answerTextbox").text();

		var qaData = {
			questionText : question,
			client_room_id : client_room_id,
			answerText : answer,
		}

		$.post("/saveQA", qaData, function(){
			$("#myMessage").val(answer);
			$("#closeQA").click();
			$('#sendbutton').click();
		});
	})
	
})





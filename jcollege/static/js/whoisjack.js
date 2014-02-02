$(document).ready(function(){	
	$('.question-form').submit(submitAnswer)
	console.log($('.question-form'))
});

function submitAnswer(event) {
	event.preventDefault();
	var frm = $('.question-form')
	console.log('submitting form')
	console.log(frm.serialize())
	$.ajax({
        type: frm.attr('method'),
        url: '/answer_question/',
        data: frm.serialize(),
        success: function (data) {
        	$('.submit-answer').remove()
        	$('.footer-container').append(data.footer);
			$('.next-question').click(newQuestion)
			$('.profile-content').empty();
			console.log(data.levelup)
			$('.profile-content').append(data.profile)
            $('.highscores-panels').empty()
            $('.highscores-panels').append(data.highscores)
        },
        error: function(data) {
            console.log('bad')
        }
    });
}

function newQuestion() {
	console.log('new question')
	$.getJSON("/new_question/", function(data) {
		console.log(data.question)
		$('.question-wrapper').empty()
		$('.question-wrapper').append(data.question)
		var frm = $('.question-form');
		frm.submit(submitAnswer);
	}); 
}
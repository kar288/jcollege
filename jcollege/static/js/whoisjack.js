$(document).ready(function(){	
	$('.question-form').submit(submitAnswer)
});

function submitAnswer(event) {
	if($('.answer').attr('type') == "text" && $('.answer').val()) {
    	$('.submit-answer').remove()		
	} else if ($('input[name=answer]:checked').val()) {
    	$('.submit-answer').remove()
	}
	event.preventDefault();
	var frm = $('.question-form')
	$.ajax({
        type: frm.attr('method'),
        url: '/answer_question/',
        data: frm.serialize(),
        success: function (data) {
        	console.log(data.levelup)
        	if (data.levelup) {
        		console.log('leveledup')
        		console.log(data.levelup)
				$('.question-wrapper').empty();
				$('.question-wrapper').append(data.levelup)
				$('.continue').click(newQuestion);
			}
        	$('.footer-container').append(data.footer);
			$('.next-question').click(newQuestion)
			$('.profile-content').empty();
			$('.profile-content').append(data.profile)
			$("input").prop('disabled', true);
            $('.highscores-panels').empty()
            $('.highscores-panels').append(data.highscores)
        },
        error: function(data) {
            console.log('bad')
        }
    });
}

function newQuestion() {
	$.getJSON("/new_question/", function(data) {
		$('.question-wrapper').empty()
		$('.question-wrapper').append(data.question)
		var frm = $('.question-form');
		frm.submit(submitAnswer);
	}); 
}
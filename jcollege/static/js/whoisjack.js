$(document).ready(function(){	
	(function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
	(i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
	m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
	})(window,document,'script','//www.google-analytics.com/analytics.js','ga');

	ga('create', 'UA-47726965-1', 'whoisjack.herokuapp.com');
	ga('send', 'pageview');

	$('.question-form').submit(submitAnswer)
	$('.points-header').tooltip('show')
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
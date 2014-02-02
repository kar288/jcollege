$(document).ready(function(){
	$('.submit-answer').click(submitAnswer);
});

function submitAnswer() {
	var frm = $('.question-form');
	$.ajax({
        type: frm.attr('method'),
        url: '/answer_question/',
        data: frm.serialize(),
        success: function (data) {
        	$('.submit-answer').remove()
        	$('.footer-container').append(data.footer);
			$('.next-question').click(newQuestion)
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
		$('.submit-answer').click(submitAnswer);
	}); 
}
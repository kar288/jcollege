$(document).ready(function(){
	var frm = $('.question-form');
	var dataToBeSent = $("form").serialize()
	console.log(frm.serialize())
	$('.submit-answer').click(function() {
		console.log(frm.serialize());
		$.ajax({
            type: frm.attr('method'),
            url: '/answer_question/',
            data: frm.serialize(),
            success: function (data) {
                console.log(data)
                console.log('success');
            },
            error: function(data) {
                console.log('bad')
            }
        });
	})
});

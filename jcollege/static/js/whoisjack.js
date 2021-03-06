$(document).ready(function(){	
	(function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
	(i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
	m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
	})(window,document,'script','//www.google-analytics.com/analytics.js','ga');

	ga('create', 'UA-47727668-1', 'whoisjack.herokuapp.com');
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

    // Tab problems
    var col_popularity_tab = $('a[href="#college-popularity"]').parent().hasClass('active')
    var std_popularity_tab = $('a[href="#individual-popularity"]').parent().hasClass('active')

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

            if (col_popularity_tab) {
                $('a[href="#college-popularity"]').tab('show');
            }
            if (std_popularity_tab) {
                $('a[href="#individual-popularity"]').tab('show');
            }
        },
        error: function(data) {
            console.log('bad')
        }
    });
}

function newQuestion() {
    $.ajax({
        method: "post",
        dataType: "json",
        data: "csrfmiddlewaretoken=" + $('input[name="nextcsrf"]').val(),
        url: '/new_question/',
        success: function(data) {
            $('.question-wrapper').empty()
            $('.question-wrapper').append(data.question)
            var frm = $('.question-form');
            frm.submit(submitAnswer);
        }
    });
}
var target_date = new Date('Mar, 3, 2014').getTime();
var countdown = $('#timer');

setInterval(function () {
    // find the amount of "seconds" between now and target
    var current_date = new Date().getTime();
    var seconds_left = (target_date - current_date) / 1000;
 
    // do some time calculations
    hours = parseInt(seconds_left / 3600);
    seconds_left = seconds_left % 3600;
     
    minutes = parseInt(seconds_left / 60);
    seconds = parseInt(seconds_left % 60);
     
    // format countdown string + set tag value
    countdown.html( hours + ' <b>Hours</b> ' + minutes + ' <b>Minutes</b> ' + seconds + ' <b>Seconds</b> ');
 
}, 1000);
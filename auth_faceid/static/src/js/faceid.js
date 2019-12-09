
odoo.define('auth_faceid.capture_video', function (require) {
"use strict";

    require('web.dom_ready');
    var $camera = $("#camera-faceid");
    var $video = $('#video');
    var $snap = $('#snap');
	var mediaConfig =  { video: true };
	var canvas = document.getElementById('canvas');
	var context = canvas.getContext('2d');
	var video = document.getElementById("video");
	var img_snap = $("#screenshot-img");
    if (!$camera.length || !$video.length) {
        return;
    }
    $('#outer').click(function(e) {
        $(this).fadeOut();
    });
/*var w,h,ratio;
	  video.addEventListener('loadedmetadata', function() {
	    ratio = video.videoWidth/video.videoHeight;
	    w = video.videoWidth-100;
	    h = parseInt(w/ratio,10);
	    canvas.width = w;
	    canvas.height = h;
	  },false);*/

	$snap.on('click', function(e) {
    	e.stopImmediatePropagation();
		canvas.width = video.videoWidth;
		canvas.height = video.videoHeight;
		canvas.getContext('2d').drawImage(video, 0, 0);
	});
    $camera.on('click', function(ev) {
    	if (!video.srcObject){
		    // запрашиваем разрешение на доступ к поточному видео камеры
		    if (navigator.mediaDevices.getUserMedia  && navigator.mediaDevices.getUserMedia){
		   		navigator.mediaDevices.getUserMedia(mediaConfig).then(function(stream) {
		   			// разрешение от пользователя получено
		            video.srcObject = stream;
		            video.play();
			    }, function () {
			    	alert('что-то не так с видеостримом или пользователь запретил его использовать');
			    });
		    }
		    else {
		    	alert("Не поддерживается браузером");
		    }
		}
		$('#outer').fadeIn();
    });
 });


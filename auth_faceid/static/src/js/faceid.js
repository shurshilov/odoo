
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
	
var lat = -13.268355,
  lng = -39.6611378;
var point = new L.LatLng(lat, lng);

	//var map = L.map('map').setView(point, 15);
	var mymap = L.map('mapid').setView([51.505, -0.09], 13);

	L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  		attribution: 'Map data © <a href="http://openstreetmap.org">OpenStreetMap</a> contributors'
	}).addTo(mymap);
	const provider = new GeoSearch.OpenStreetMapProvider();

var circle = L.circle(point, {
  fillColor: '#42A5F5',
  fillOpacity: 0.2,
  radius: 500
}).addTo(mymap);
var marker = L.marker(point).addTo(mymap);

provider.search({
  query: lat + ',' + lng
}).then(function(result) {
  marker.bindPopup(result[0].label).openPopup();
});

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


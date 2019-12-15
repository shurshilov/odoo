odoo.define('website_form_map.leaflet', function (require) {
"use strict";

    require('web.dom_ready');

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

 });


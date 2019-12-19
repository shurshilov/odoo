odoo.define('website_form_map.leaflet', function (require) {
"use strict";

  require('web.dom_ready');
	var rpc = require('web.rpc');
  var lat = 55.505,
      lng = 38.6611378,
      enable = false,
      size = 230;
  var deferred1 = $.Deferred(),
      deferred2 = $.Deferred(),
      deferred3 = $.Deferred(),
      deferred4 = $.Deferred();
  rpc.query({
                model: 'ir.config_parameter',
                method: 'search_read',
                args: [[['key','=','website_leaflet_lat']]],
            })
    .then(function(result){
        lat = result[0].value;
        deferred1.resolve();
  });
  rpc.query({
                model: 'ir.config_parameter',
                method: 'search_read',
                args: [[['key','=','website_leaflet_lng']]],
            })
    .then(function(result){
        lng = result[0].value;
        deferred2.resolve();
  });
  rpc.query({
                model: 'ir.config_parameter',
                method: 'search_read',
                args: [[['key','=','website_leaflet_enable']]],
            })
    .then(function(result){
        enable =  (result[0].value == 'True');
        deferred3.resolve();
  });
  rpc.query({
                model: 'ir.config_parameter',
                method: 'search_read',
                args: [[['key','=','website_leaflet_size']]],
            })
    .then(function(result){
        size = result[0].value;
        $('#mapid').css('width',size);
        $('#mapid').css('height',size);
        deferred4.resolve();
  });

  deferred1.done(function () {
      deferred2.done(function () {
          deferred3.done(function () {
              if (enable){
              	var point = new L.LatLng(lat, lng);
              	var mymap = L.map('mapid').setView(point, 13);
              	L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                		attribution: 'Map data © <a href="http://openstreetmap.org">OpenStreetMap</a> contributors'
              	}).addTo(mymap);
              }
          });
      });
    });
 });


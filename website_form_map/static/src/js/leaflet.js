// Copyright 2019 Shurshilov Artem
// License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
odoo.define('website_form_map.leaflet', function (require) {
"use strict";

  require('web.dom_ready');
  //var rpc = require('web.rpc');
  var lat = 55.505,
      lng = 38.6611378,
      enable = false,
      size = 230;

  $.get( "/map/config", function( data ) {
      var data_json = JSON.parse(data);
      lat = data_json['lat'];
      lng = data_json['lng'];
      enable = data_json['enable'];
      size = data_json['size'];

      if (enable && $('#mapid').length){
          var point = new L.LatLng(lat, lng);
          var mymap = L.map('mapid').setView(point, 13);
          L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
              attribution: 'Map data © <a href="http://openstreetmap.org">OpenStreetMap</a> contributors'
          }).addTo(mymap);
          $('#mapid').css('width',size);
          $('#mapid').css('height',size);
          // hide google icon
          $('.img-fluid').hide();
      }
  });

 });


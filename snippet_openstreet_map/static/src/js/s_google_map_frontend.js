odoo.define('snippet_openstreet_map.s_google_map_frontend', function (require) {
    'use strict';

    var sAnimation = require('website.content.snippets.animation');
    var googleScriptLoaded = $.Deferred();

    sAnimation.registry.s_google_map = sAnimation.Class.extend({
        selector: 'section.s_google_map',

        start: function () {
            var defs = [this._super.apply(this, arguments)];
            this.redraw();
            return $.when.apply($, defs);
        },
    map: null,
    add_marker: function(points=null) {
    	//[[55.75, 37.62],[-12.07173, -76.97581],[29.29255, 48.0808],[-7.551281599999999, 110.8784625],[55.7048496, 37.6223873]]
        var self = this;
        if (!points)
	        var points = [
	            [ 55.75, 37.62, "http://www.url_address_01.com/"],
	            [ -12.07173, -76.97581, "http://www.url_address_02.com/"],
	            [ 29.29255, 48.0808, "http://www.url_address_03.com/"],
	            [ -7.551281599999999, 110.8784625, "http://www.url_address_03.com/"],
	            [ 55.7048496, 37.6223873, "http://www.url_address_03.com/"]
	        ];
        var marker = [];
        var i;
        for (i = 0; i < points.length; i++) {
            marker[i] = new L.Marker([points[i][0], points[i][1]]);
            marker[i].addTo(self.map);
            //marker[i].on('click', onClick);
        };
    },

    redraw: function () {
      var self = this;
      var p = this.$target.attr('data-map-gps').substring(1).slice(0, -1).split(',');
      var zoom =this.$target.attr('data-map-zoom');
      var markers =this.$target.attr('data-markers');
      //console.log(zoom)
      //console.log(markers)
      if (markers)
      	markers = JSON.parse(markers);

      var mapC = this.$target.find('.map_container');
      if (mapC.length){
          var point = new L.LatLng(p[0], p[1]);
          
          //console.log("LEAFLET")
          self.map = L.map(mapC.get(0)).setView(point, zoom);
          L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
              attribution: 'Map data © <a href="http://openstreetmap.org">OpenStreetMap</a> contributors'
          }).addTo(self.map);
          mapC.css('width',"100%");
          mapC.css('height', "100%");
          if (markers)
          	self.add_marker(markers);
          else
          	self.add_marker();
        }
      },
    });

    // This prototype permit to save if the google maps script is already loading or not.
    // This script cannot be loaded 2 times, so if we have 2 snippets in the same view
    // we don't want to call 2 times the scripts because the first one is not finished.
    // And we cannot put in in an asset because we don't want to load this script on each
    // page, but only page with a google maps snippet...
    sAnimation.registry.s_google_map.prototype.isScriptLoading = false;

    return {
        googleScriptLoaded: googleScriptLoaded,
    };
});

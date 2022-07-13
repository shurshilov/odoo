odoo.define('snippet_openstreet_map.s_openstreet_map_frontend', function (require) {
    'use strict';

    var sAnimation = require('website.content.snippets.animation');

    sAnimation.registry.s_openstreet_map = sAnimation.Class.extend({
        selector: 'section.s_openstreet_map',

        // start: function () {
        //     return $.when.apply( this.redraw(),[this._super.apply(this, arguments)]);
        // },
        start: function () {
            this.redraw()
            return this._super.apply(this, arguments);
        },

        add_markers: function (points = null) {
            //[[55.75, 37.62],[-12.07173, -76.97581],[29.29255, 48.0808],[-7.551281599999999, 110.8784625],[55.7048496, 37.6223873]]
            var self = this;
            if (!points)
                var points = [
                    [55.75, 37.62, "http://www.url_address_01.com/"],
                    [-12.07173, -76.97581, "http://www.url_address_02.com/"],
                    [29.29255, 48.0808, "http://www.url_address_03.com/"],
                    [-7.551281599999999, 110.8784625, "http://www.url_address_03.com/"],
                    [55.7048496, 37.6223873, "http://www.url_address_03.com/"]
                ];
            var marker = [];
            var i;
            for (i = 0; i < points.length; i++) {
                marker[i] = new L.Marker([points[i][0], points[i][1]]);
                marker[i].addTo(self.map);
                //marker[i].on('click', onClick);
            };
        },

        redraw: async function () {
            console.log(this.el.dataset)

            if (this.el.dataset.mapMarkers){
                let markers = JSON.parse(this.el.dataset.mapMarkers);
                
                var container = L.DomUtil.get('mapid');
                if (container != null) {
                    container._leaflet_id = null;
                }
                this.map = L.map($('.map_container')[0]).setView([51.505, -0.09], this.el.dataset.mapZoom);
                L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                    attribution: 'Map data © <a href="http://openstreetmap.org">OpenStreetMap</a> contributors'
                }).addTo(this.map);
                this.add_markers(markers)
                $('.openstreet_description').hide()
                setTimeout(()=> { this.map.invalidateSize() }, 400);
            }

        },
    });

});

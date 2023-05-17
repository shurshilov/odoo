odoo.define('char_geo_widget', function (require) {
  "use strict";
  // const FieldBinaryFile = require("web.basic_fields").FieldBinaryFile;
  // const fieldRegistry = require('web.field_registry');
  var registry = require('web.field_registry');
  var base_f = require('web.basic_fields');
  var FieldChar = base_f.FieldChar;

  var CharGeoWidget = FieldChar.extend({
    template: 'FieldCharGeo',
    _render: function () {
      this._super.apply(this, arguments);
      var info = JSON.parse(this.value.replace(/'/g, '"'));
      if (!info) {
        this.$el.html('');
        return;
      }

      if (this.mode == "readonly")
        // if (this.value) {
        var $el = this.$el[0];
      $($el).css({ width: '50%', height: '50%', top: "300px", right: "100px", position: "fixed" });
      // self.$('#openDiv').on('click', function (event) {
      // this.$el[0].toggle('show');

      // });

      var container = L.DomUtil.get('map');
      if (container != null) {
        container._leaflet_id = null;
      }
      // display map with current marker user
      this.point = new L.LatLng(info.geolocation.lat, info.geolocation.long);
      this.mymap = L.map(this.$el[0]).setView(this.point, 13);
      this.mymap.addControl(new L.Control.Fullscreen());
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: 'Map data © <a href="http://openstreetmap.org">OpenStreetMap</a> contributors'
      }).addTo(this.mymap);
      var marker = L.marker(this.point).addTo(this.mymap);
      setTimeout(() => { this.mymap.invalidateSize() }, 400);


      // const map = new ol.Map({
      //     layers: [
      //       new ol.layer.Tile({
      //         source: new ol.source.OSM(),
      //       }),
      //     ],
      //     target: target,
      //     // target: 'map',
      //     view: new ol.View({
      //       center: [12, 15],
      //       zoom: 2,
      //     }),
      //     controls: ol.control.defaults().extend([
      //       new ol.control.FullScreen(),
      //       new ol.control.ScaleLine(),
      //       new ol.control.ZoomSlider()
      //   ]),
      //   });
      // new BackgroundLayers()..create([field_infos.edit_raster,])


      // }
    },
  });

  registry.add('char_geo_widget', CharGeoWidget);
  return CharGeoWidget;
})

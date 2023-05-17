L.GeoIP = L.extend({

    getPosition: function (ip) {
        var url = "https://freegeoip.net/json/";
        var result = L.latLng(0, 0);

        if (ip !== undefined) {
            url = url + ip;
        } else {
            //lookup our own ip address
        }
        $.get(
            url,
            function(data) {
                console.log(data)
                var geoip_response = JSON.parse(data);
                result.lat = geoip_response.latitude;
                result.lng = geoip_response.longitude;
            }
        );
        return result;
    },

    centerMapOnPosition: function (map, zoom, ip) {
        var position = L.GeoIP.getPosition(ip);
        map.setView(position, zoom);
    }
});
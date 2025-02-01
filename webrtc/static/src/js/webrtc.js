odoo.define('webrtc.webrtc', function(require) {
    var core = require('web.core');
    var base_f = require('web.basic_fields');
    var FieldChar = base_f.FieldChar;
    var session = require('web.session');
    var utils = require('web.utils');
    var field_utils = require('web.field_utils');
    var AbstractField = require('web.AbstractField');
    var registry = require('web.field_registry');
    var qweb = core.qweb;
    
    var FieldWebrtc = FieldChar.extend({
        //template: 'FieldWebrtc',
        //className: 'o_field_char',
        //tagName: 'span',
        //supportedFieldTypes: ['char'],

/*        events: _.extend({}, AbstractField.prototype.events, {
            'click .fa-magic': 'on_magic',
        }),
*/
        _render: function () {
            var self =this;
            this._super.apply(this, arguments);
            
            console.log('webrtc', this);
            console.log(this.value);
            console.log(this.attrs.options.webrtc_server);
            //var def = this._super.apply(this, arguments);
            var webRtcServer = null;
//            window.onload = function() { 
                    if (this.attrs.options.webrtc_server && this.attrs.options.iframe) {
                        var url = this.attrs.options.webrtc_server + '/webrtcstreamer.html?' + this.value;
                        this.$el.append('<div id="webrtc" class="video-container"><iframe src="'+ url+'" height="300" width="400" allowfullscreen="" frameborder="0"></iframe></div><span class="togglebutton" id="toggle_webrtc">Toggle</span>');
                    }
                    else if (this.attrs.options.webrtc_server ) {
                        this.$el.append($(qweb.render('FieldWebrtc', {widget: this})));
                        webRtcServer = new WebRtcStreamer(self.$('#video')[0], this.attrs.options.webrtc_server);
                        var url = {'video':this.value}
                        var options = "rtptransport=tcp&timeout=60";
                        webRtcServer.connect(url.video,url.audio,options);
                    }
                    else {
                        //var url = 'https://webrtc-streamer.herokuapp.com/webrtcstreamer.html?' + this.value;
                        //this.$el.append('<div id="webrtc"><iframe src="'+ url+'" height="300" width="400" allowfullscreen="" frameborder="0"></iframe></div><span class="togglebutton" id="toggle_webrtc">Toggle</span>');
                        this.$el.append($(qweb.render('FieldWebrtc', {widget: this})));
                        webRtcServer = new WebRtcStreamer(self.$('#video')[0], 'https://webrtc-streamer.herokuapp.com');
                        var url = {'video':this.value};
                        var options = "rtptransport=tcp&timeout=60";
                        webRtcServer.connect(url.video,url.audio,options);
                    }

            this.$el.find("#toggle_webrtc").click(function (evt) {
                evt.stopPropagation();
                evt.preventDefault();
                $('#webrtc').toggleClass("maximized");
            });
            //}
            window.onbeforeunload = function() { 
                if (webRtcServer) 
                    webRtcServer.disconnect(); 
            }
            //return def;
        },
    });
    registry.add('webrtc', FieldWebrtc)


});
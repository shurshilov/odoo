odoo.define('audio_widget', function (require) {
    var FieldBinaryFile = require("web.basic_fields").FieldBinaryFile;
    var fieldRegistry = require('web.field_registry');
    var core = require('web.core');
    var _t = core._t;

    var AttachmentAudioWidget = FieldBinaryFile.extend({

        supportedFieldTypes: ['binary', 'many2one'],
        accepted_file_extensions: 'audio/*,application/ogg',

        _getAudioUrl: function (attachment) {
            return '/web/content/' + attachment.res_id + '?download=true';
        },

        _renderReadonly: function () {
            if (this.mode == "readonly")
                if (this.value) {
                    const url = this._getAudioUrl(this.value);

                    let audio = $('<audio>', {
                        'src': url,
                        'controls': true,
                        'preload': "metadata",
                    })

                    this.$el.append(audio);

                    audio.on("error", () => {
                        this.displayNotification({
                            title: _t('Wrong Extension Audio File'),
                            message: _t("Format should be in wav, ogg, mp3, mp4, oga, ogx, mpeg"),
                            type: 'danger',
                        });
                    })
                }
        },

        on_file_change: function (ev) {
            this._super.apply(this, arguments);

            let files = ev.target.files;

            if (!files || files.length === 0)
                return;

            let dotArray = files[0].name.split(".");
            let extension = dotArray[dotArray.length - 1];

            if (!['wav', 'ogg', 'mp3', 'mp4', 'oga', 'ogx', 'mpeg'].includes(extension))
                this.displayNotification({
                    title: _t('Wrong Extension Audio File'),
                    message: _t("Format should be in wav, ogg, mp3, mp4, oga, ogx, mpeg"),
                    type: 'danger',
                });
        }
    });

    fieldRegistry.add('attachment_audio_widget', AttachmentAudioWidget);
    return { AttachmentAudioWidget: AttachmentAudioWidget };
})

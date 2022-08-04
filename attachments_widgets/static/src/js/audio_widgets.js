odoo.define('audio_widget', function (require) {
    const FieldBinaryFile = require("web.basic_fields").FieldBinaryFile;
    const fieldRegistry = require('web.field_registry');
    const relational_fields = require('web.relational_fields');
    const FieldMany2One = relational_fields.FieldMany2One;
    const session = require('web.session');
    const core = require('web.core');
    const _t = core._t;


    const AttachmentMany2OneAudioWidget = FieldMany2One.extend({

        supportedFieldTypes: ['many2one'],
        accepted_file_extensions: 'audio/*,application/ogg',

        _getUrl: function (attachment) {
            return '/web/content/' + attachment.res_id + '?download=true';
        },

        _computeIsAudio(extension) {
            const audioExtensions = [
                'wav',
                'ogg',
                'mp3',
                'mp4',
                'oga',
                'ogx',
                'mpeg'
            ];
            return audioExtensions.includes(extension);
        },

        _computeExtension(filename) {
            const extension = filename && filename.split('.').pop();
            if (extension) {
                return extension;
            }
            return clear();
        },

        _renderReadonly: function () {
            this._super.apply(this, arguments);
            if (this.mode == "readonly")
                if (this.value) {
                    const url = this._getUrl(this.value);

                    let audio = $('<audio>', {
                        'src': url,
                        'controls': true,
                        'preload': "metadata",
                    })

                    // this.$el.append(audio);
                    this.$el = audio;

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

            const filename = files[0].name;
            const extension = this._computeExtension(filename);

            if (!this._computeIsAudio(extension))
                this.displayNotification({
                    title: _t('Wrong Extension Audio File'),
                    message: _t("Format should be in wav, ogg, mp3, mp4, oga, ogx, mpeg"),
                    type: 'danger',
                });
        }
    });

    const AttachmentBinaryAudioWidget = FieldBinaryFile.extend({

        supportedFieldTypes: ['binary'],
        accepted_file_extensions: 'audio/*,application/ogg',

        _getUrl: function () {
            if (this.field.type == 'binary')
                return session.url('/web/content', {
                    model: this.model,
                    id: JSON.stringify(this.res_id),
                    field: this.name,
                });
        },

        _computeIsAudio(extension) {
            const audioExtensions = [
                'wav',
                'ogg',
                'mp3',
                'mp4',
                'oga',
                'ogx',
                'mpeg'
            ];
            return audioExtensions.includes(extension);
        },

        _computeExtension(filename) {
            const extension = filename && filename.split('.').pop();
            if (extension) {
                return extension;
            }
            return clear();
        },

        _renderReadonly: function () {
            this._super.apply(this, arguments);
            if (this.mode == "readonly")
                if (this.value) {
                    const url = this._getUrl(this.value);

                    let audio = $('<audio>', {
                        'src': url,
                        'controls': true,
                        'preload': "metadata",
                    })

                    // this.$el.append(audio);
                    this.$el = audio;

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

            const filename = files[0].name;
            const extension = this._computeExtension(filename);

            if (!this._computeIsAudio(extension))
                this.displayNotification({
                    title: _t('Wrong Extension Audio File'),
                    message: _t("Format should be in wav, ogg, mp3, mp4, oga, ogx, mpeg"),
                    type: 'danger',
                });
        }
    });

    fieldRegistry.add('attachment_many2one_audio_widget', AttachmentMany2OneAudioWidget);
    fieldRegistry.add('attachment_binary_audio_widget', AttachmentBinaryAudioWidget);

    return {
        AttachmentMany2OneAudioWidget: AttachmentMany2OneAudioWidget,
        AttachmentBinaryAudioWidget: AttachmentBinaryAudioWidget
    };
})

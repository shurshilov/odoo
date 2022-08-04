odoo.define('audio_widget', function (require) {
    const FieldBinaryFile = require("web.basic_fields").FieldBinaryFile;
    const fieldRegistry = require('web.field_registry');
    const session = require('web.session');
    const core = require('web.core');
    const _t = core._t;

    const AttachmentVideoWidget = FieldBinaryFile.extend({

        supportedFieldTypes: ['binary', 'many2one'],
        accepted_file_extensions: 'video/*,audio/mpeg',

        _getUrl: function (attachment) {
            if (this.field.type == 'binary')
                return session.url('/web/content', {
                    model: this.model,
                    id: JSON.stringify(this.res_id),
                    field: this.name,
                });
            else
                return '/web/content/' + attachment.res_id + '?download=true';
        },

        _computeIsVideo(mimetype) {
            const videoExtensions = [
                'audio/mpeg',
                'video/x-matroska',
                'video/mp4',
                'video/webm',
            ];
            return videoExtensions.includes(mimetype);
        },

        _computeExtension(filename) {
            const extension = filename && filename.split('.').pop();
            if (extension) {
                return extension;
            }
            return clear();
        },

        _renderReadonly: function () {
            console.log(this, "7777")
            if (this.mode == "readonly")
                if (this.value) {
                    const url = this._getUrl(this.value);

                    let video = $('<video>', {
                        'src': url,
                        'controls': true,
                        'preload': "metadata",
                    })

                    this.$el.append(video);

                    audio.on("error", () => {
                        this.displayNotification({
                            title: _t('Wrong Extension Video File'),
                            message: _t("Format should be in webm, mp4, mpeg"),
                            type: 'danger',
                        });
                    })
                }
        },

        on_file_change: function (ev) {
            console.log(this, "7777")
            this._super.apply(this, arguments);

            let files = ev.target.files;

            if (!files || files.length === 0)
                return;

            const filename = files[0].name;
            const extension = this._computeExtension(filename);

            if (!this._computeIsVideo(extension))
                this.displayNotification({
                    title: _t('Wrong Extension Video File'),
                    message: _t("Format should be in webm, mp4, mpeg"),
                    type: 'danger',
                });
        }
    });

    fieldRegistry.add('attachment_video_widget', AttachmentVideoWidget);
    return { AttachmentVideoWidget: AttachmentVideoWidget };
})

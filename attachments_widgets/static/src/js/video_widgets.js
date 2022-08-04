odoo.define('video_widget', function (require) {
    const FieldBinaryFile = require("web.basic_fields").FieldBinaryFile;
    const fieldRegistry = require('web.field_registry');
    const relational_fields = require('web.relational_fields');
    const FieldMany2One = relational_fields.FieldMany2One;
    const session = require('web.session');
    const core = require('web.core');
    const _t = core._t;

    const AttachmentMany2oneVideoWidget = FieldMany2One.extend({

        supportedFieldTypes: ['many2one'],
        accepted_file_extensions: 'video/*,audio/mpeg',

        _getUrl: function (attachment) {
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
            if (this.mode == "readonly")
                if (this.value) {
                    const width = this.nodeOptions.width ? this.nodeOptions.width : "50%";
                    const url = this._getUrl(this.value);

                    let video = $('<video>', {
                        'src': url,
                        'controls': true,
                        'preload': "metadata",
                        'width': width
                    })

                    this.$el.append(video);

                    video.on("error", () => {
                        this.displayNotification({
                            title: _t('Wrong Extension Video File'),
                            message: _t("Format should be in webm, mp4, mpeg"),
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

            if (!this._computeIsVideo(extension))
                this.displayNotification({
                    title: _t('Wrong Extension Video File'),
                    message: _t("Format should be in webm, mp4, mpeg"),
                    type: 'danger',
                });
        }
    });

    const AttachmentBinaryVideoWidget = FieldBinaryFile.extend({

        supportedFieldTypes: ['binary'],
        accepted_file_extensions: 'video/*,audio/mpeg',

        _getUrl: function () {
            if (this.field.type == 'binary')
                return session.url('/web/content', {
                    model: this.model,
                    id: JSON.stringify(this.res_id),
                    field: this.name,
                });
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
            if (this.mode == "readonly")
                if (this.value) {
                    const width = this.nodeOptions.width ? this.nodeOptions.width : "50%";
                    const url = this._getUrl(this.value);

                    let video = $('<video>', {
                        'src': url,
                        'controls': true,
                        'preload': "metadata",
                        'width': width
                    })

                    this.$el.append(video);

                    video.on("error", () => {
                        this.displayNotification({
                            title: _t('Wrong Extension Video File'),
                            message: _t("Format should be in webm, mp4, mpeg"),
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

            if (!this._computeIsVideo(extension))
                this.displayNotification({
                    title: _t('Wrong Extension Video File'),
                    message: _t("Format should be in webm, mp4, mpeg"),
                    type: 'danger',
                });
        }
    });

    fieldRegistry.add('attachment_binary_video_widget', AttachmentBinaryVideoWidget);
    fieldRegistry.add('attachment_many2one_video_widget', AttachmentMany2oneVideoWidget);
    return {
        AttachmentBinaryVideoWidget: AttachmentBinaryVideoWidget,
        AttachmentMany2oneVideoWidget: AttachmentMany2oneVideoWidget,
    };
})

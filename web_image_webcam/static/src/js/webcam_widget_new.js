/*
    Copyright 2019-2022 Shurshilov Artem <shurshilov.a@yandex.ru>
    License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
*/
odoo.define('web_image_webcam.webcam_widget', function (require) {
    "use strict";

    var core = require('web.core');
    var Dialog = require('web.Dialog');
    var base_f = require('web.basic_fields');
    var imageWidget = base_f.FieldBinaryImage;
    var _t = core._t;
    var QWeb = core.qweb;

    var WebcamDialogNew = Dialog.extend({
        template: 'WebcamDialogNew',

        handleStream: async function (stream) {
            let def = $.Deferred();
            const video = this.$el.find('video')[0];

            // устанавливаем выбранную камеру
            if (stream && stream.getVideoTracks().length)
                this.$('.custom-select').val(stream.getVideoTracks()[0].getSettings().deviceId);

            // отображаем видео в диалоге
            video.srcObject = stream;

            video.addEventListener("canplay", () => {
                video.play();
            });

            video.addEventListener("loadedmetadata", () => {
                this.streamStarted = true;
                def.resolve();
            }, false);

            return def
        },

        stop_video: function () {
            // останавливае видео поток
            this.streamStarted = false;
            this.$el.find('video')[0].srcObject.getTracks().forEach((track) => {
                track.stop();
            });
        },

        take_snapshot: function(video) {
            var canvas = document.createElement("canvas");
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            var canvasContext = canvas.getContext("2d");
            canvasContext.drawImage(video, 0, 0);
            return canvas.toDataURL('image/jpeg');
        },

        start_video: async function (device) {
            try {
                let config = {
                    width: { min: 640, ideal: 1280 },
                    height: { min: 480, ideal: 720 },
                    facingMode: this.shouldFaceUser ? 'user' : 'environment',
                }
                if (device)
                    config.deviceId = { exact: device }

                const videoStream = await navigator.mediaDevices.getUserMedia({
                    video: config
                })
                await this.handleStream(videoStream)
            } catch (e) {
                console.error('*** getUserMedia', e)
            } finally {
            }
        },

        init: function (parent, options) {
            options = options || {};
            options.fullscreen = true;
            options.dialogClass = options.dialogClass || '' + ' o_act_window';
            options.size = 'large';
            options.title = _t("Webcam dialog");
            options.buttons = [
                {
                    text: _t("Take Snapshot"), classes: 'btn-primary take_snap_btn',
                    click: () => {
                        const video = this.$el.find('video')[0];
                        this.img_data = this.take_snapshot(video)
                        // Display Snap besides Live WebCam Preview
                        this.$("#webcam_result").html('<img src="' + this.img_data + '"/>');

                        // Remove "disabled" attr from "Save & Close" button
                        $('.save_close_btn').removeClass('disabled');
                    }
                },
                {
                    text: _t("Save & Close"), classes: 'btn-primary disabled save_close_btn', close: true,
                    click: () => {
                        var img_data_base64 = this.img_data.split(',')[1];
                        // From the above info, we doing the opposite stuff to find the approx size of Image in bytes.
                        var approx_img_size = 3 * (img_data_base64.length / 4)  // like... "3[n/4]"

                        // Upload image in Binary Field
                        this.parent.on_file_uploaded(approx_img_size, "web-cam-preview.jpeg", "image/jpeg", img_data_base64);
                    }
                },
                {
                    text: _t("Flip"), classes: 'btn-primary flip_btn',
                    click: () => {
                        this.flip()
                    }
                },
                {
                    text: _t("Close"), close: true
                }
            ]
            this.parent = parent;
            this._super(parent, options);
        },

        start: function (device = null) {
            return this._super.apply(this, arguments).then(async () => {
                const cameraOptions = this.$('.custom-select');
                // добавляем обработчик смены камеры
                cameraOptions.empty().off().on('change', (e) => {
                    this.device = $(e.target).val();
                    this.restart(this.device)
                });

                // добавляем все доступные камеры в селекшен
                const devices = await navigator.mediaDevices.enumerateDevices();
                const videoDevices = devices.filter(device => device.kind === 'videoinput');
                videoDevices.map(videoDevice => {
                    var opt = document.createElement('option');
                    opt.value = videoDevice.deviceId;
                    opt.innerHTML = videoDevice.label;
                    cameraOptions.append(opt);
                    return opt;
                });

                // устанавливаем камеру если уже выбрали
                if (device)
                    cameraOptions.val(device);

                // запрашиваем разрешение на доступ к поточному видео камеры
                // и запускаем видео с камеры
                await this.start_video(device);

            });
        },

        flip: function () {
            this.stop_video();
            this.shouldFaceUser = !this.shouldFaceUser;
            this.start(this.device);
        },

        restart: function (device) {
            this.stop_video();
            this.start(device)
        },

        destroy: function () {
            this.stop_video();
            this._super.apply(this, arguments);
        },

    })

    imageWidget.include({
        _render: async function () {
            this._super.apply(this, arguments);
            this.$el.find('.o_form_binary_file_web_cam').off().on('click', () => {
                // Init Webcam
                new WebcamDialogNew(this).open();
            });
        },
    });

});

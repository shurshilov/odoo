/*
    Copyright 2016 Siddharth Bhalgami <siddharth.bhalgami@techreceptives.com>
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

        drawVideoPrepare: function (sourceSelector, canvasSelector) {
            let def = $.Deferred();
            let video = null;

            if (this.streamStarted)
                video = this.$el.find(sourceSelector)[0];

            // не нашли видео элемента или поток не запущен
            // или распознование завершено
            if (!video || !this.streamStarted)
                def.resolve(null);

            var canvas = this.$el.find(canvasSelector)[0];
            if (!canvas)
                def.resolve(null);

            def.resolve([canvas, video]);
            return def
        },

        drawVideo: async function (canvas, video) {
            // отрисовка прекращается при закрытии диалога
            if (!this.streamStarted)
                return

            // если изображение с камеры слишком большое
            // уменьшаем его до размера диалогового окна
            if (video.videoWidth > this.$el.width()) {
                canvas.width = this.$el.width();
                canvas.height = (this.$el.width() * video.videoHeight) / video.videoWidth;
            }
            else {
                canvas.width = video.videoWidth;
                canvas.height = video.videoHeight;
            }

            // отрисовываем видео
            canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);
            // рисуем видео с камеры 100fps
            await this.sleep(10);

            this.drawVideo(canvas, video);

        },

        handleStream: async function (stream) {
            let def = $.Deferred();
            const video = this.$el.find('video')[0];

            // отображаем видео в диалоге
            video.srcObject = stream;
            video.play();
            video.addEventListener("loadedmetadata", (e) => {
                this.streamStarted = true;
                def.resolve();
            }, false);

            return def
        },

        sleep(ms) {
            return new Promise(resolve => setTimeout(resolve, ms));
        },

        start_video: async function () {
            try {
                const videoStream = await navigator.mediaDevices.getUserMedia({
                    video: {
                        width: { min: 640, ideal: 1280 },
                        height: { min: 480, ideal: 720 },
                        facingMode: this.shouldFaceUser ? 'user' : 'environment',
                        // .deviceId = { exact: select.value }
                    }
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
                        this.img_data = this.res[0].toDataURL()
                        // Display Snap besides Live WebCam Preview
                        this.$("#webcam_result").html('<img src="' + this.img_data + '"/>');

                        // Remove "disabled" attr from "Save & Close" button
                        this.$('.save_close_btn').removeAttr('disabled');
                    }
                },
                {
                    text: _t("Save & Close"), classes: 'btn-primary save_close_btn', close: true,
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

                        if (this.streamStarted) {
                            // останавливае распознование, если отключаем камеру
                            this.streamStarted = false;
                            this.$el.find('video')[0].srcObject.getTracks().forEach((track) => {
                                track.stop();
                            });
                          }
                          this.shouldFaceUser = !this.shouldFaceUser;
                          this.start()
                    }
                },
                {
                    text: _t("Close"), close: true
                }
            ]
            this.parent = parent;
            this._super(parent, options);
        },

        start: function () {
            return this._super.apply(this, arguments).then(async () => {
                // At time of Init "Save & Close" button is disabled
                this.$('.save_close_btn').attr('disabled', 'disabled');
                this.$('.take_snap_btn').attr('disabled', 'disabled');

                const cameraOptions = this.$('.custom-select');
                const devices = await navigator.mediaDevices.enumerateDevices();
                const videoDevices = devices.filter(device => device.kind === 'videoinput');
                const options = videoDevices.map(videoDevice => {
                    var opt = document.createElement('option');
                    opt.value = videoDevice.deviceId;
                    opt.innerHTML = videoDevice.label;
                    cameraOptions.append(opt);
                    return opt;
                });

                // запрашиваем разрешение на доступ к поточному видео камеры
                // и запускаем видео с камеры
                await this.start_video()

                // подготавливаем канвас для отрисовки видео
                this.res = await this.drawVideoPrepare("video", "#faceid_canvas");
                if (this.res)
                    // отрисовываем видео на канвас
                    this.drawVideo(this.res[0], this.res[1]);
                    $('.take_snap_btn').removeAttr('disabled');
            });
        },

        destroy: function () {
            // останавливае распознование, если отключаем камеру
            this.streamStarted = false;
            this.$el.find('video')[0].srcObject.getTracks().forEach((track) => {
                track.stop();
            });
            this._super.apply(this, arguments);
        },

    })

    imageWidget.include({
        _render: async function () {
            this._super.apply(this, arguments);
            this.$el.find('.o_form_binary_file_web_cam').off().on('click', () =>{
                // Init Webcam
                new WebcamDialogNew(this).open();
            });
        },
    });

});

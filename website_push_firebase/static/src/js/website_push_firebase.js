/**
Copyright (C) 2020 Artem Shurshilov <shurshilov.a@yandex.ru>
Odoo Proprietary License v1.0

This software and associated files (the "Software") may only be used (executed,
modified, executed after modifications) if you have purchased a valid license
from the authors, typically via Odoo Apps, or if you have received a written
agreement from the authors of the Software (see the COPYRIGHT file).

You may develop Odoo modules that use the Software as a library (typically
by depending on it, importing it and using its resources), but without copying
any source code or material from the Software. You may distribute those
modules under the license of your choice, provided that this license is
compatible with the terms of the Odoo Proprietary License (For example:
LGPL, MIT, or proprietary licenses similar to this one).

It is forbidden to publish, distribute, sublicense, or sell copies of the Software
or modified copies of the Software.

The above copyright notice and this permission notice must be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.**/

odoo.define("website_firebase_push_notifications", function (require) {
  "use strict";
  var ajax = require("web.ajax");
  //var sAnimations = require('website.content.snippets.animation');
  var publicWidget = require("web.public.widget");

  //sAnimations.registry.websiteFirebasePush = sAnimations.Class.extend({
  publicWidget.registry.websiteFirebasePush = publicWidget.Widget.extend({
    selector: "#top_menu",

    sendTokenToServer: function (currentToken) {
      if (!this.isTokenSentToServer(currentToken)) {
        console.log("Отправка токена на сервер...");

        ajax
          .jsonRpc("/website/firebase_push_notifications", "call", {
            currentToken: currentToken,
          })
          .then(function () {
            //location.reload();
            console.log("Token success send to server");
          });

        this.setTokenSentToServer(currentToken);
      } else {
        console.log("Токен уже отправлен на сервер.");
      }
    },

    // используем localStorage для отметки того,
    // что пользователь уже подписался на уведомления
    isTokenSentToServer: function (currentToken) {
      return (
        window.localStorage.getItem("sentFirebaseMessagingToken") ==
        currentToken
      );
    },

    setTokenSentToServer: function (currentToken) {
      window.localStorage.setItem(
        "sentFirebaseMessagingToken",
        currentToken ? currentToken : "",
      );
    },

    subscribe: function () {
      this.messaging
        .requestPermission()
        .then(() => {
          // Get Instance ID token. Initially this makes a network call, once retrieved
          // subsequent calls to getToken will return from cache.
          this.messaging
            .getToken()
            .then((currentToken) => {
              if (currentToken) {
                this.sendTokenToServer(currentToken);
                //updateUIForPushEnabled(currentToken);
              } else {
                console.log(
                  "No Instance ID token available. Request permission to generate one",
                );
                //updateUIForPushPermissionRequired();
                this.setTokenSentToServer(false);
              }
            })
            .catch((error) => {
              console.log("An error occurred while retrieving token", error);
              //updateUIForPushPermissionRequired();
              this.setTokenSentToServer(false);
            });
        })
        .catch((error) => {
          //showError('Unable to get permission to notify', error);
          console.log("Unable to get permission to notify", error);
        });
    },

    init: function () {
      this._super.apply(this, arguments);
      console.log("WORK");
      // браузер поддерживает уведомления
      // вообще, эту проверку должна делать библиотека Firebase, но она этого не делает
      if ("Notification" in window) {
        this._rpc({
          route: "/mail/firebase_push_notifications/conf",
        }).then((conf) => {
          console.log(conf);
          if (firebase.apps.length === 0) {
            // Your web app's Firebase configuration
            var firebaseConfig = conf;
            // Initialize Firebase
            firebase.initializeApp(firebaseConfig);
            // Retrieve Firebase Messaging object.
            this.messaging = firebase.messaging();

            // Handle incoming messages. Called when:
            // - a message is received while the app has focus
            // - the user clicks on an app notification created by a service worker
            //   `messaging.setBackgroundMessageHandler` handler.
            this.messaging.onMessage(function (payload) {
              debugger;
              console.log("Message received. ", payload);
              //new Notification(payload.notification.title, payload.notification);
              // регистрируем пустой ServiceWorker каждый раз
              if ("serviceWorker" in navigator) {
                window.addEventListener("load", function () {
                  navigator.serviceWorker
                    .register("/mail-firebase-messaging-sw.js")
                    .then(
                      function (registration) {
                        // Registration was successful
                        console.log(
                          "ServiceWorker registration successful with scope: ",
                          registration.scope,
                        );
                        registration.showNotification(
                          payload.notification.title,
                          payload.notification,
                        );
                      },
                      function (err) {
                        alert(error);
                        // registration failed :(
                        console.log("ServiceWorker registration failed: ", err);
                      },
                    );
                });
              }
            });

            // пользователь уже разрешил получение уведомлений
            // подписываем на уведомления если ещё не подписали
            console.log(Notification.permission);
            if (Notification.permission !== "denied") {
              this.subscribe();
              console.log("subscribe");
            }

            // по клику, запрашиваем у пользователя разрешение на уведомления
            // и подписываем его
            /*                $('#subscribe').on('click', function () {
                            this.subscribe();
                        });*/

            // Callback fired if Instance ID token is updated.
            this.messaging.onTokenRefresh(() => {
              this.messaging
                .getToken()
                .then((refreshedToken) => {
                  console.log("Token refreshed.");
                  // Indicate that the new Instance ID token has not yet been sent to the
                  // app server.
                  this.setTokenSentToServer(false);
                  // Send Instance ID token to app server.
                  this.sendTokenToServer(refreshedToken);
                  // ...
                })
                .catch((err) => {
                  alert(err);
                  console.log("Unable to retrieve refreshed token ", err);
                  //showToken('Unable to retrieve refreshed token ', err);
                });
            });
          }
        });
      } else {
        console.log("Browser not support Notification");
      }
    },
  });
});

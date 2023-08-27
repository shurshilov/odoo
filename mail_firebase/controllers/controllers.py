# Copyright 2020 Artem Shurshilov
# Odoo Proprietary License v1.0

# This software and associated files (the "Software") may only be used (executed,
# modified, executed after modifications) if you have purchased a valid license
# from the authors, typically via Odoo Apps, or if you have received a written
# agreement from the authors of the Software (see the COPYRIGHT file).

# You may develop Odoo modules that use the Software as a library (typically
# by depending on it, importing it and using its resources), but without copying
# any source code or material from the Software. You may distribute those
# modules under the license of your choice, provided that this license is
# compatible with the terms of the Odoo Proprietary License (For example:
# LGPL, MIT, or proprietary licenses similar to this one).

# It is forbidden to publish, distribute, sublicense, or sell copies of the Software
# or modified copies of the Software.

# The above copyright notice and this permission notice must be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

from odoo import SUPERUSER_ID, http
from odoo.http import request


class FirebasePushNotifications(http.Controller):
    @http.route(["/mail/firebase_push_notifications"], type="json", auth="user")
    def firebase_push_notifications(self, currentToken):
        # ADD new DEVICE
        request.env["mail.firebase"].sudo().create(
            {
                "user_id": request.env.user.id,
                "os": "",
                "token": currentToken,
            }
        )

    @http.route(
        ["/mail/firebase_push_notifications/conf"], type="json", auth="user"
    )
    def firebase_push_notifications_cond(self):
        env = request.env(user=SUPERUSER_ID)
        config_parameters = env["ir.config_parameter"]
        conf = {
            "apiKey": config_parameters.get_param("mail_firebase_apiKey"),
            "authDomain": config_parameters.get_param(
                "mail_firebase_authDomain"
            ),
            "databaseURL": config_parameters.get_param(
                "mail_firebase_databaseURL"
            ),
            "projectId": config_parameters.get_param("mail_firebase_projectId"),
            "storageBucket": config_parameters.get_param(
                "mail_firebase_storageBucket"
            ),
            "messagingSenderId": config_parameters.get_param(
                "mail_firebase_messagingSenderId"
            ),
            "appId": config_parameters.get_param("mail_firebase_appId"),
            "measurementId": config_parameters.get_param(
                "mail_firebase_measurementId"
            ),
        }
        return conf

    @http.route(
        ["/firebase-messaging-sw.js"], type="http", auth="public", website=True
    )
    def firebase_message_sw2(self):
        env = request.env(user=SUPERUSER_ID)
        config_parameters = env["ir.config_parameter"]
        mail_firebase_apiKey = config_parameters.get_param(
            "mail_firebase_apiKey"
        )
        mail_firebase_authDomain = config_parameters.get_param(
            "mail_firebase_authDomain"
        )
        mail_firebase_databaseURL = config_parameters.get_param(
            "mail_firebase_databaseURL"
        )
        mail_firebase_projectId = config_parameters.get_param(
            "mail_firebase_projectId"
        )
        mail_firebase_storageBucket = config_parameters.get_param(
            "mail_firebase_storageBucket"
        )
        mail_firebase_messagingSenderId = config_parameters.get_param(
            "mail_firebase_messagingSenderId"
        )
        mail_firebase_appId = config_parameters.get_param("mail_firebase_appId")
        mail_firebase_measurementId = config_parameters.get_param(
            "mail_firebase_measurementId"
        )

        service_worker = (
            """
            // Give the service worker access to Firebase Messaging.
            // Note that you can only use Firebase Messaging here, other Firebase libraries
            // are not available in the service worker.
            importScripts('https://www.gstatic.com/firebasejs/7.17.1/firebase-app.js');
            importScripts('https://www.gstatic.com/firebasejs/7.17.1/firebase-messaging.js');

            // Initialize the Firebase app in the service worker by passing in
            // your app's Firebase config object.
            // https://firebase.google.com/docs/web/setup#config-object
            // Your web app's Firebase configuration
            var firebaseConfig = {
                apiKey: '"""
            + mail_firebase_apiKey
            + """',
                authDomain: '"""
            + mail_firebase_authDomain
            + """',
                databaseURL: '"""
            + mail_firebase_databaseURL
            + """',
                projectId: '"""
            + mail_firebase_projectId
            + """',
                storageBucket: '"""
            + mail_firebase_storageBucket
            + """',
                messagingSenderId: '"""
            + mail_firebase_messagingSenderId
            + """',
                appId: '"""
            + mail_firebase_appId
            + """',
                measurementId: '"""
            + mail_firebase_measurementId
            + """',
            };
            // Initialize Firebase
            firebase.initializeApp(firebaseConfig);


            // Retrieve an instance of Firebase Messaging so that it can handle background
            // messages.
            const messaging = firebase.messaging();

            // Customize notification handler
            messaging.setBackgroundMessageHandler(function(payload) {
              console.log('[firebase-messaging-sw.js] Received background message ', payload);
              // Customize notification here
              // Copy data object to get parameters in the click handler
              payload.data.data = JSON.parse(JSON.stringify(payload.data));

              //return self.registration.showNotification(payload.data.title, payload.data);
              return self.registration.showNotification(payload.notification.title, payload.notification);
            });


            self.addEventListener('notificationclick', function(event) {
              const target = event.notification.data.click_action || '/';
              event.notification.close();

              // This looks to see if the current is already open and focuses if it is
              event.waitUntil(clients.matchAll({
                type: 'window',
                includeUncontrolled: true
              }).then(function(clientList) {
                // clientList always is empty?!
                for (var i = 0; i < clientList.length; i++) {
                  var client = clientList[i];
                  if (client.url === target && 'focus' in client) {
                    return client.focus();
                  }
                }

                return clients.openWindow(target);
              }));
        });
        """
        )
        return request.make_response(
            service_worker,
            headers=[
                ("Content-Type", "text/javascript; charset=UTF-8"),
            ],
        )

    @http.route(
        ["/mail-firebase-messaging-sw.js"],
        type="http",
        auth="public",
        website=True,
    )
    def firebase_message_sw(self):
        env = request.env(user=SUPERUSER_ID)
        config_parameters = env["ir.config_parameter"]
        mail_firebase_apiKey = config_parameters.get_param(
            "mail_firebase_apiKey"
        )
        mail_firebase_authDomain = config_parameters.get_param(
            "mail_firebase_authDomain"
        )
        mail_firebase_databaseURL = config_parameters.get_param(
            "mail_firebase_databaseURL"
        )
        mail_firebase_projectId = config_parameters.get_param(
            "mail_firebase_projectId"
        )
        mail_firebase_storageBucket = config_parameters.get_param(
            "mail_firebase_storageBucket"
        )
        mail_firebase_messagingSenderId = config_parameters.get_param(
            "mail_firebase_messagingSenderId"
        )
        mail_firebase_appId = config_parameters.get_param("mail_firebase_appId")
        mail_firebase_measurementId = config_parameters.get_param(
            "mail_firebase_measurementId"
        )

        service_worker = (
            """
            // Give the service worker access to Firebase Messaging.
            // Note that you can only use Firebase Messaging here, other Firebase libraries
            // are not available in the service worker.
            importScripts('https://www.gstatic.com/firebasejs/7.17.1/firebase-app.js');
            importScripts('https://www.gstatic.com/firebasejs/7.17.1/firebase-messaging.js');

            // Initialize the Firebase app in the service worker by passing in
            // your app's Firebase config object.
            // https://firebase.google.com/docs/web/setup#config-object
            // Your web app's Firebase configuration
            var firebaseConfig = {
                apiKey: '"""
            + mail_firebase_apiKey
            + """',
                authDomain: '"""
            + mail_firebase_authDomain
            + """',
                databaseURL: '"""
            + mail_firebase_databaseURL
            + """',
                projectId: '"""
            + mail_firebase_projectId
            + """',
                storageBucket: '"""
            + mail_firebase_storageBucket
            + """',
                messagingSenderId: '"""
            + mail_firebase_messagingSenderId
            + """',
                appId: '"""
            + mail_firebase_appId
            + """',
                measurementId: '"""
            + mail_firebase_measurementId
            + """',
            };
            // Initialize Firebase
            firebase.initializeApp(firebaseConfig);


            // Retrieve an instance of Firebase Messaging so that it can handle background
            // messages.
            const messaging = firebase.messaging();

            // Customize notification handler
            messaging.setBackgroundMessageHandler(function(payload) {
              console.log('[firebase-messaging-sw.js] Received background message ', payload);
              // Customize notification here
              // Copy data object to get parameters in the click handler
              payload.data.data = JSON.parse(JSON.stringify(payload.data));

              //return self.registration.showNotification(payload.data.title, payload.data);
              return self.registration.showNotification(payload.notification.title, payload.notification);
            });


            self.addEventListener('notificationclick', function(event) {
              const target = event.notification.data.click_action || '/';
              event.notification.close();

              // This looks to see if the current is already open and focuses if it is
              event.waitUntil(clients.matchAll({
                type: 'window',
                includeUncontrolled: true
              }).then(function(clientList) {
                // clientList always is empty?!
                for (var i = 0; i < clientList.length; i++) {
                  var client = clientList[i];
                  if (client.url === target && 'focus' in client) {
                    return client.focus();
                  }
                }

                return clients.openWindow(target);
              }));
        });
        """
        )
        return request.make_response(
            service_worker,
            headers=[
                ("Content-Type", "text/javascript; charset=UTF-8"),
            ],
        )

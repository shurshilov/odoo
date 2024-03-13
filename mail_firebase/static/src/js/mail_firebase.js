/** @odoo-module */

// import { DiscussContainer } from "@mail/components/discuss_container/discuss_container";
import { Discuss } from "@mail/core/common/discuss";
import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";

patch(Discuss.prototype, {
  setup() {
    // this._super(...arguments);
    super.setup();
    this.rpc = useService("rpc");
    console.log("WORK");
    // браузер поддерживает уведомления
    // вообще, эту проверку должна делать библиотека Firebase, но она этого не делает
    if ("Notification" in window) {
      this.rpc("/mail/firebase_push_notifications/conf").then((conf) => {
        console.log(conf);
        if (firebase.apps.length === 0) {
          // Your web app's Firebase configuration
          const firebaseConfig = conf;

          // Initialize Firebase
          // const app = initializeApp(firebaseConfig);
          // const analytics = getAnalytics(app);

          // Initialize Firebase
          firebase.initializeApp(firebaseConfig);
          // Retrieve Firebase Messaging object.
          this.messagingFirebase = firebase.messaging();

          // Handle incoming messages. Called when:
          // - a message is received while the app has focus
          // - the user clicks on an app notification created by a service worker
          //   `messaging.setBackgroundMessageHandler` handler.

          // TODO:по идее можно удалить
          if ("serviceWorker" in navigator) {
            window.addEventListener("load", () => {
              navigator.serviceWorker.register(
                "/mail-firebase-messaging-sw.js",
              );
            });
          }

          // this.messagingFirebase.onMessage(function (payload) {
          //   debugger;
          //   console.log("Message received. ", payload);
          //   //new Notification(payload.notification.title, payload.notification);
          //   // регистрируем пустой ServiceWorker каждый раз
          //   if ("serviceWorker" in navigator) {
          //     window.addEventListener("load", function () {
          //       navigator.serviceWorker
          //         .register("/mail-firebase-messaging-sw.js")
          //         .then(
          //           function (registration) {
          //             // Registration was successful
          //             console.log(
          //               "ServiceWorker registration successful with scope: ",
          //               registration.scope,
          //             );
          //             registration.showNotification(
          //               payload.notification.title,
          //               payload.notification,
          //             );
          //           },
          //           function (err) {
          //             alert(error);
          //             // registration failed :(
          //             console.log("ServiceWorker registration failed: ", err);
          //           },
          //         );
          //     });
          //   }
          // });

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
          this.messagingFirebase.onTokenRefresh(() => {
            this.messagingFirebase
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

  sendTokenToServer(currentToken) {
    if (!this.isTokenSentToServer(currentToken)) {
      console.log("Отправка токена на сервер...");

      this.rpc("/mail/firebase_push_notifications", {
        currentToken: currentToken,
      }).then((data) => {
        console.log("Token success send to server");
      });

      this.setTokenSentToServer(currentToken);
    } else {
      console.log("Токен уже отправлен на сервер.");
    }
  },

  // используем localStorage для отметки того,
  // что пользователь уже подписался на уведомления
  isTokenSentToServer(currentToken) {
    return (
      window.localStorage.getItem("sentFirebaseMessagingTokenMail") ==
      currentToken
    );
  },

  setTokenSentToServer(currentToken) {
    window.localStorage.setItem(
      "sentFirebaseMessagingTokenMail",
      currentToken ? currentToken : "",
    );
  },

  subscribe() {
    this.messagingFirebase
      .requestPermission()
      .then(() => {
        // Get Instance ID token. Initially this makes a network call, once retrieved
        // subsequent calls to getToken will return from cache.
        this.messagingFirebase
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
            alert(error);
            console.log("An error occurred while retrieving token", error);
            //updateUIForPushPermissionRequired();
            this.setTokenSentToServer(false);
          });
      })
      .catch((error) => {
        alert(error);
        //showError('Unable to get permission to notify', error);
        console.log("Unable to get permission to notify", error);
      });
  },
});

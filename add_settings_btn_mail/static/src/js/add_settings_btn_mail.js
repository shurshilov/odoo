odoo.define(
  "add_settings_btn_mail.mail_settings_widget_extend",
  function (require) {
    "use strict";

    var Followers = require("mail.Followers");
    var ThreadField = require("mail.ThreadField");
    var ChatThread = require("mail.ChatThread");
    var concurrency = require("web.concurrency");
    var core = require("web.core");
    var session = require("web.session");
    var data = require("web.data");
    var ActionManager = require("web.ActionManager");
    var chat_manager = require("mail.chat_manager");
    var Chatter = require("mail.Chatter");
    var _t = core._t;
    var QWeb = core.qweb;
    var time = require("web.time");
    var rpc = require("web.rpc");
    var config = require("web.config");

    var ORDER = {
      ASC: 1,
      DESC: -1,
    };

    Chatter.include({
      //action by click
      events: {
        "click .o_chatter_button_new_message": "_onOpenComposerMessage",
        "click .o_chatter_button_log_note": "_onOpenComposerNote",
        "click .o_chatter_button_schedule_activity": "_onScheduleActivity",
        "click .o_filter_checkbox": "_update",
      },
      // public
      //read from DB from go record to record and NOT run start function
      update: function (record, fieldNames) {
        var self = this;
        //console.log("update");
        if (this.record.res_id !== record.res_id) {
          //this._closeComposer(true);
          if (this.fields.thread) {
            this.fields.thread.res_id = record.res_id;
            rpc
              .query({
                model: this.fields.thread.model,
                method: "read",
                args: [[this.fields.thread.res_id], ["hide_notification"]],
              })
              .then(function (result) {
                if (result[0].hide_notification) {
                  self.$(".o_filter_checkbox").prop("checked", true);
                  _.extend(self.fields.thread.thread.options, {
                    filter: "yes",
                  });
                } else {
                  self.$(".o_filter_checkbox").prop("checked", false);
                  _.extend(self.fields.thread.thread.options, { filter: "no" });
                }

                self.update(record);
              });
          }
        }
        this._super.apply(this, arguments);
      },
      //read from DB field hide_notification and change checkbox and reload message
      start: function () {
        var res = this._super.apply(this, arguments);
        var self = this;
        if (this.fields.thread)
          rpc
            .query({
              model: this.fields.thread.model,
              method: "read",
              args: [[this.fields.thread.res_id], ["hide_notification"]],
            })
            .then(function (result) {
              if (result[0].hide_notification) {
                self.$(".o_filter_checkbox").prop("checked", true);
                _.extend(self.fields.thread.thread.options, { filter: "yes" });
              } else {
                self.$(".o_filter_checkbox").prop("checked", false);
                _.extend(self.fields.thread.thread.options, { filter: "no" });
              }
              self.trigger_up("reload");
              //self.update(self.fields.thread.record);
            });

        return res;
      },

      //Write to current model status checkbox and reload message (filtered)
      _update: function () {
        var check = false;
        //console.log("_update");
        if (this.$(".o_filter_checkbox")[0].checked) {
          _.extend(this.fields.thread.thread.options, { filter: "yes" });
          check = true;
        } else _.extend(this.fields.thread.thread.options, { filter: "no" });

        rpc.query({
          model: this.fields.thread.model,
          method: "write",
          args: [
            [this.fields.thread.res_id],
            {
              hide_notification: check,
            },
          ],
        });
        this.update(this.fields.thread.record);
      },
    });
    ChatThread.include({
      render: function (messages, options) {
        //          console.log(messages);
        //           if (options.filter == 'yes')
        //               messages = _.filter(messages, function(msg){ return (msg.message_type == 'email'); });
        var self = this;
        var msgs = _.map(messages, this._preprocess_message.bind(this));
        if (this.options.display_order === ORDER.DESC) {
          msgs.reverse();
        }
        options = _.extend({}, this.options, options);

        // Hide avatar and info of a message if that message and the previous
        // one are both comments wrote by the same author at the same minute
        // and in the same document (users can now post message in documents
        // directly from a channel that follows it)
        var prev_msg;
        _.each(msgs, function (msg) {
          if (
            !prev_msg ||
            Math.abs(msg.date.diff(prev_msg.date)) > 60000 ||
            prev_msg.message_type !== "comment" ||
            msg.message_type !== "comment" ||
            prev_msg.author_id[0] !== msg.author_id[0] ||
            prev_msg.model !== msg.model ||
            prev_msg.res_id !== msg.res_id
          ) {
            msg.display_author = true;
          } else {
            msg.display_author = !options.squash_close_messages;
          }
          prev_msg = msg;
        });
        //my
        //console.log(options.filter)
        if (options.filter == "yes")
          msgs = _.filter(msgs, function (msg) {
            return msg.message_type == "comment" || msg.message_type == "email";
          });
        //msgs = _.filter(msgs, function(msg){ return (msg.message_type == 'comment' || msg.message_type == 'email' ); });
        //msgs = _.filter(msgs, function(msg){ return (msg.message_type == 'email'); });

        this.$el.html(
          QWeb.render("mail.ChatThread", {
            messages: msgs,
            options: options,
            ORDER: ORDER,
            date_format: time.getLangDatetimeFormat(),
          }),
        );

        this.attachments = _.uniq(_.flatten(_.map(messages, "attachment_ids")));

        _.each(msgs, function (msg) {
          var $msg = self.$(
            '.o_thread_message[data-message-id="' + msg.id + '"]',
          );
          $msg.find(".o_mail_timestamp").data("date", msg.date);

          self.insert_read_more($msg);
        });

        if (!this.update_timestamps_interval) {
          this.update_timestamps_interval = setInterval(function () {
            self.update_timestamps();
          }, 1000 * 60);
        }
      },
    });

    /*    Followers.include({
        events: {
        // click on '(Un)Follow' button, that toggles the follow for uid
        'click .o_followers_follow_button': '_onFollowButtonClicked',
        // click on a subtype, that (un)subscribes for this subtype
        'click .o_subtypes_list input': '_onSubtypeClicked',
        // click on 'invite' button, that opens the invite wizard
        'click .o_add_follower': '_onAddFollower',
        'click .o_add_follower_channel': '_onAddChannel',
        // click on 'edit_subtype' (pencil) button to edit subscription
        'click .o_edit_subtype': '_onEditSubtype',
        'click .o_remove_follower': '_onRemoveFollower',
        'click .o_mail_redirect': '_onRedirect',
        //add action on settings btn
        'click .o_setting': '_onWizzard',
    },

        _onWizzard: function () {
                var settingsWidget = this;
                var activeModel = settingsWidget.record.model;
                var activeRecordId = settingsWidget.record.data.id;
                var activeField = settingsWidget.attrs.name;

                var openModal = function() {
                    var context = {
                        active_model: activeModel,
                        active_record_id: activeRecordId,
                        active_field: activeField,
                    };
                    var modalAction = {
                        type: 'ir.actions.act_window',
                        res_model: 'neuro.job',
                        name: 'Settings',
                        views: [[false, 'form']],
                        target: 'new',
                        context: context,
                    };
                    settingsWidget.do_action(modalAction);
                };
                openModal();
    },

    });*/
  },
);

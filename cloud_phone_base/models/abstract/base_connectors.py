# -*- coding: utf-8 -*-
from odoo import models, api


class CloudPhoneConnectorFactory(models.AbstractModel):

    _name = "cloud.phone.connector.factory"
    _description = "cloud.phone.connector"

    def _auth_request(self, connector_id):
        """Fetch authorized request"""
        raise NotImplementedError

    def _get_and_update_numbers(self, connector_id):
        raise NotImplementedError

    def _get_record_mp3_attachment(self, connector_id, call_id):
        raise NotImplementedError

    def _create_attachment(self, connector_id, call_id):
        raise NotImplementedError

    def _get_and_update_call(self, connector_id, call):
        raise NotImplementedError

    def _get_and_update_calls(self, connector_id, begin_datetime, end_datetime):
        raise NotImplementedError

    def _update_numbers_and_fetch_calls(
        self, connector_id, days=None, minutes=60, wait_minutes=60
    ):
        raise NotImplementedError

    @staticmethod
    def swipe(str1, str2):
        if str1 in str2:
            return True
        if str2 in str1:
            return True
        return False

    @staticmethod
    def get_hms(timedelta):
        seconds = timedelta.seconds
        hours = seconds // 3600
        minutes = (seconds // 60) % 60
        return "%02d:%02d:%02d" % (hours, minutes, seconds % 60)

    def find_by_number(self, model, number):
        number = "".join(i for i in number if i.isdigit())
        for rec in self.env[model].search([]):
            if rec.work_phone:
                work_phone_digits = "".join(i for i in rec.work_phone if i.isdigit())
                if work_phone_digits:
                    if self.swipe(work_phone_digits, number):
                        return rec
                    if self.swipe(work_phone_digits[1:], number):
                        return rec
                    if self.swipe("7" + work_phone_digits[1:], number):
                        return rec

            if rec.mobile_phone:
                mobile_phone_digits = "".join(
                    i for i in rec.mobile_phone if i.isdigit()
                )
                if mobile_phone_digits:
                    if self.swipe(mobile_phone_digits, number):
                        return rec
                    if self.swipe(mobile_phone_digits[1:], number):
                        return rec
                    if self.swipe("7" + mobile_phone_digits[1:], number):
                        return rec

from odoo.addons.bus.controllers.main import BusController
from odoo.http import request, route


class ViewOnlineFormBusController(BusController):
    # --------------------------
    # Extends BUS Controller Poll
    # --------------------------
    def _poll(self, dbname, channels, last, options):
        if request.session.uid:
            channels = list(channels)
            channels.append((request.db, "view.online.form"))
        return super()._poll(dbname, channels, last, options)

    @route("/longpolling/send/viewonline", type="json", auth="public")
    def send(self, channel, message):
        if not isinstance(channel, str):
            raise Exception("bus.Bus only string channels are allowed.")
        message.update(
            {"user_name": request.env["res.users"].sudo().browse(int(message["uid"])).name}
        )
        return request.env["bus.bus"].sendone((request.db, channel), message)

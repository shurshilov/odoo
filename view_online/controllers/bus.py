import datetime
import random
from dataclasses import asdict, dataclass, field

from odoo.addons.bus.controllers.main import BusController
from odoo.http import request, route


class Viewer:
    pass


class Channel:
    pass


from enum import Enum


class Message(Enum):
    READ = 1
    ALIVE_READ = 2
    EDIT = 3
    ALIVE_EDIT = 4
    DIED = 0


COLORS = ["#3CC157", "#2AA7FF", "#1B1B1B", "#FCBC0F", "#F85F36"]
DIED_SECONDS_DELAY = 7


class Channel(Channel):
    def __init__(self, channel, db_name, res_id):
        self.db_name = db_name
        self.channel = channel
        self.res_id = res_id
        self.viewers: dict[int, Viewer] = {}

    def add_viewer(self, viewer: Viewer):
        self.viewers[viewer.uid] = viewer

    def remove_viewer(self, viewer: Viewer):
        if viewer.uid in self.viewers:
            del self.viewers[viewer.uid]

    def check_died(self):
        now = datetime.datetime.now()
        d = []
        for viewer in self.viewers.values():
            if (
                now - viewer.last_activity[self.channel]
            ).seconds > DIED_SECONDS_DELAY:
                d.append(viewer)
        for viewer in d:
            self.remove_viewer(viewer)

    def add_message(self, viewer: Viewer, message: Message):
        if message == message.DIED:
            self.remove_viewer(viewer)
        else:
            self.add_viewer(viewer)
        viewer.state = message
        viewer.last_activity[self.channel] = datetime.datetime.now()
        self.check_died()
        return [asdict(v) for v in self.viewers.values()]


@dataclass
class Viewer:
    db_name: str
    uid: int
    name: str
    last_activity: dict
    state: Message = Message.READ
    color: str = field(default_factory=lambda: random.choice(COLORS))


class ViewOnlineManager:
    def __init__(self):
        self.channels: dict[str, Channel] = {}
        self.viewers: dict[int, Viewer] = {}
        self.request = None

    def get_channel(self, channel, db_name, res_id) -> Channel:
        if not self.channels.get(channel):
            self.channels[channel] = Channel(channel, db_name, res_id)
        return self.channels[channel]

    def get_viewers(self, db_name, uid: int) -> Viewer:
        if not uid in self.viewers:
            self.viewers[uid] = Viewer(
                db_name,
                uid,
                self.request.env["res.users"].sudo().browse(uid).name,
                last_activity={},
            )
        return self.viewers[uid]

    def message_in(self, channel, db_name, res_id, uid, message, request):
        if self.request is None:
            self.request = request
        channel = self.get_channel(channel, db_name, res_id)
        viewer: Viewer = self.get_viewers(db_name, uid)
        return channel.add_message(viewer, message)


class ViewOnlineFormBusController(BusController):
    # --------------------------
    # Extends BUS Controller Poll
    # --------------------------

    ViewOnlineManager = ViewOnlineManager()

    @route("/longpolling/send/viewonline", type="json", auth="public")
    def send(self, channel, res_id, uid, message):
        if not isinstance(channel, str):
            raise Exception("bus.Bus only string channels are allowed.")
        db_name = request.db
        message = Message(int(message))

        items = self.ViewOnlineManager.message_in(
            channel, db_name, res_id, uid, message, request
        )
        if message in [message.ALIVE_READ, message.ALIVE_EDIT]:
            return items
        elif message in [message.READ, message.EDIT, message.DIED]:
            return request.env["bus.bus"].sendone(channel, (items))

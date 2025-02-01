from odoo import http
from odoo.http import request
from odoo.addons.web.controllers.main import Binary

import io
import webp
from PIL import Image


class BinaryWebp(Binary):
    @http.route(
        [
            "/web/image",
            "/web/image/<string:xmlid>",
            "/web/image/<string:xmlid>/<string:filename>",
            "/web/image/<string:xmlid>/<int:width>x<int:height>",
            "/web/image/<string:xmlid>/<int:width>x<int:height>/<string:filename>",
            "/web/image/<string:model>/<int:id>/<string:field>",
            "/web/image/<string:model>/<int:id>/<string:field>/<string:filename>",
            "/web/image/<string:model>/<int:id>/<string:field>/<int:width>x<int:height>",
            "/web/image/<string:model>/<int:id>/<string:field>/<int:width>x<int:height>/<string:filename>",
            "/web/image/<int:id>",
            "/web/image/<int:id>/<string:filename>",
            "/web/image/<int:id>/<int:width>x<int:height>",
            "/web/image/<int:id>/<int:width>x<int:height>/<string:filename>",
            "/web/image/<int:id>-<string:unique>",
            "/web/image/<int:id>-<string:unique>/<string:filename>",
            "/web/image/<int:id>-<string:unique>/<int:width>x<int:height>",
            "/web/image/<int:id>-<string:unique>/<int:width>x<int:height>/<string:filename>",
        ],
        type="http",
        auth="public",
    )
    def content_image(
        self,
        xmlid=None,
        model="ir.attachment",
        id=None,
        field="datas",
        filename_field="name",
        unique=None,
        filename=None,
        mimetype=None,
        download=None,
        width=0,
        height=0,
        crop=False,
        access_token=None,
        **kwargs
    ):
        # other kwargs are ignored on purpose
        res = super().content_image(
            xmlid=xmlid,
            model=model,
            id=id,
            field=field,
            filename_field=filename_field,
            unique=unique,
            filename=filename,
            mimetype=mimetype,
            download=download,
            width=width,
            height=height,
            crop=crop,
            access_token=access_token,
            **kwargs
        )

        if request and request.session.get("webp_enable", False) or kwargs.get("webp", False):
            browsers_capability = True

            # 'image/gif' show as image, that exclude
            if res.content_type not in [
                "image/png",
                "image/webp",
                "image/jpeg",
                "image/jpg",
                "image/jpe",
            ]:
                browsers_capability = False

            # check safari only > 14 version and not msie
            if request.httprequest.user_agent and browsers_capability:
                safari = request.httprequest.user_agent.browser == "safari"
                if safari and float(request.httprequest.user_agent.version) < 14:
                    browsers_capability = False

                # firefox = request.httprequest.user_agent.browser == 'firefox'
                # if firefox and float(request.httprequest.user_agent.version) < 65:
                #     browsers_capability = False

                edge = request.httprequest.user_agent.browser == "edge"
                if edge and float(request.httprequest.user_agent.version) < 18:
                    browsers_capability = False

                ie = request.httprequest.user_agent.browser == "msie"
                if ie:
                    browsers_capability = False

                # convert image to webp
                if browsers_capability:
                    image_old = io.BytesIO(res.data)
                    image = Image.open(image_old)
                    pic = webp.WebPPicture.from_pil(image)

                    # change quality
                    q = int(kwargs.get("webp_q", False)) or int(
                        request.session.get("webp_quality", 94)
                    )
                    config = webp.WebPConfig.new(preset=webp.WebPPreset.PHOTO, quality=q)
                    content = pic.encode(config).buffer()
                    if len(content) < len(res.data):
                        res.data = content
                        res.content_type = "image/webp"
        return res

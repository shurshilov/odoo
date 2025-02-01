######################################################################################################
#
# Copyright (C) B.H.C. sprl - All Rights Reserved, http://www.bhc.be
# Copyright (c) 2020 Shurshilov Artem (shurshilov.a@yandex.ru)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied,
# including but not limited to the implied warranties
# of merchantability and/or fitness for a particular purpose
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>
######################################################################################################
import json
from google_auth_oauthlib.flow import InstalledAppFlow

from odoo import http
from odoo.http import request
from werkzeug.utils import redirect


SCOPES = [
    "openid",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/drive.file",
]


def credentials_to_dict(credentials):
    return {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes": credentials.scopes,
    }


def get_credentials_from_string(credentials_string):
    json_acceptable_string = credentials_string.replace("'", '"')
    return json.loads(json_acceptable_string)


class Binary(http.Controller):
    @http.route("/authorize_auto_backup_grive", type="http", auth="user")
    def authorize(self):
        CLIENT_SECRETS_FILE = get_credentials_from_string(
            request.env["ir.config_parameter"].get_param("abp_json_secret_file")
        )
        # Create flow instance to manage the OAuth 2.0 Authorization Grant Flow steps.
        flow = InstalledAppFlow.from_client_config(
            CLIENT_SECRETS_FILE, scopes=SCOPES
        )

        # The URI created here must exactly match one of the authorized redirect URIs
        # for the OAuth 2.0 client, which you configured in the API Console. If this
        # value doesn't match an authorized URI, you will get a 'redirect_uri_mismatch'
        # error.
        flow.redirect_uri = (
            request.httprequest.host_url + "oauth2callback_auto_backup_grive"
        )

        authorization_url, state = flow.authorization_url(
            # Enable offline access so that you can refresh an access token without
            # re-prompting the user for permission. Recommended for web server apps.
            access_type="offline",
            # Enable incremental authorization. Recommended as a best practice.
            include_granted_scopes="true",
        )

        # Store the state so the callback can verify the auth server response.
        request.session["auto_backup_grive"] = state

        return redirect(authorization_url)

    @http.route("/oauth2callback_auto_backup_grive", type="http", auth="user")
    def oauth2callback(self, **params):
        if "state" not in params:
            redirect("/")
        CLIENT_SECRETS_FILE = get_credentials_from_string(
            request.env["ir.config_parameter"].get_param("abp_json_secret_file")
        )
        # Specify the state when creating the flow in the callback so that it can
        # verified in the authorization server response.
        state = request.session["auto_backup_grive"]

        flow = InstalledAppFlow.from_client_config(
            CLIENT_SECRETS_FILE, scopes=SCOPES, state=state
        )
        flow.redirect_uri = (
            request.httprequest.host_url + "oauth2callback_auto_backup_grive"
        )

        # Use the authorization server's response to fetch the OAuth 2.0 tokens.
        flow.fetch_token(authorization_response=request.httprequest.url)

        # Store credentials in the session.
        # ACTION ITEM: In a production app, you likely want to save these
        #              credentials in a persistent database instead.
        credentials = flow.credentials
        request.env["ir.config_parameter"].set_param(
            "abp_credentials",
            credentials_to_dict(credentials),
        )
        request.env["ir.config_parameter"].set_param(
            "abp_token", flow.credentials.token
        )
        redirect("/")

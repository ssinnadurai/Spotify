import base64
import urllib.parse as urlparse
import webbrowser
from urllib.parse import parse_qs
from urllib.parse import urlencode

import requests
import requests.sessions


class SpotifyAuth(object):
    # define get/post/delete/put here
    def __init__(self, client_id):
        self.client_id = client_id
        self.endpoint = "https://accounts.spotify.com/authorize"
        self.token_url = "https://accounts.spotify.com/api/token"
        self.access_token = None
        self.token_type = None
        self.expire_in = None
        self.refresh_token = None

    def authorize(self):
        pass

    def encode_credentials(self, client_secret):
        credentials = f"{self.client_id}:{client_secret}"
        encoded_credentials = base64.b64encode(credentials.encode())
        return {
            "Authorization": f"Basic {encoded_credentials.decode()}"
        }


class AuthorizationCodeFlow(SpotifyAuth):

    def __init__(self, client_id, client_secret, redirect_uri=None, state=None, scope='', response_type="code",
                 show_dialog=False):
        super(AuthorizationCodeFlow, self).__init__(client_id)
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.state = state
        self.scope = scope
        self.response_type = response_type
        self.show_dialog = show_dialog

    def authorize(self):
        # check to see if this working right
        '''
        add state, scope and show_dialog
        :return:
        '''
        params = {
            "client_id": self.client_id,
            'response_type': self.response_type,
            'redirect_uri': self.redirect_uri,
            'scope': self.scope
        }

        response = requests.get(self.endpoint, params=params)
        if response.status_code != 200:
            return False
        webbrowser.open_new(response.url)

        return True

    def validate_authorization(self, validation_url):
        validation_code = urlparse.urlparse(validation_url)
        return_param = parse_qs(validation_code.query)
        if "error" in return_param:
            return return_param['error']
        authorization_code = return_param['code']

        response = requests.post(self.token_url, data={
            "grant_type": "authorization_code",
            "code": authorization_code,
            "redirect_uri": self.redirect_uri,
            "client_id": self.client_id,
            "client_secret": self.client_secret
        })
        # print(response.json())
        if response.status_code == 200:
            response = response.json()
            self.access_token = response['access_token']
            self.token_type = response["token_type"]
            self.expire_in = response["expires_in"]
            self.refresh_token = response["refresh_token"]

    def token_renewal(self):
        response = requests.post(self.token_url, data={
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token,
        }, headers=self.encode_credentials(self.client_secret))

        if response.status_code == 200:
            response = response.json()
            self.access_token = response['access_token']
            self.token_type = response['token_type']
            self.expire_in = response['expires_in']
            self.scope = response['scope']
        else:
            return False


class ClientCredentialsFlow(SpotifyAuth):

    def __init__(self, client_id=None, client_secret=None):
        super(ClientCredentialsFlow, self).__init__(client_id)
        self.client_secret = client_secret
        self.scope = None
        self.state = None
        self.headers = {  # check
            "Authorization": f"Bearer {self.access_token}"
        }

    def authorize(self):
        if self.client_id is None or self.client_secret is None:
            raise Exception("You must set client_id and client_secret")

        token_header = self.encode_credentials(self.client_secret)

        response = requests.post(self.token_url, data={
            "grant_type": "client_credentials"
        }, headers=token_header)

        if response.status_code != 200:
            raise Exception("Could not authenticate client.")
        # print(response.json())
        response = response.json()
        self.access_token = response['access_token']
        self.token_type = response['token_type']
        self.scope = response['scope']
        self.expire_in = response['expires_in']
        return True

    def search(self, query={}, search_type="track", operator=None, operator_query=None):
        if query == {}:
            raise Exception("A query is required")
        query = " ".join([f"{k}:{v}" for k, v in query.items()])
        if operator != None and operator_query != None:
            if operator.lower() == "or" or operator.lower() == "not":
                operator = operator.upper()
                if isinstance(operator_query, str):
                    query = f"{query} {operator} {operator_query}"
        query_params = urlencode({"q": query, "type": search_type.lower()})
        return self.spotify_api_call(query_params)

    def spotify_api_call(self, query_params):
        lookup_url = f"{self.endpoint}?{query_params}"
        response = requests.get(lookup_url, headers=self.headers)
        if response.status_code not in range(200, 299):
            return {}
        return response.json()

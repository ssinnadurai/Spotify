import requests
import json
from urllib.parse import urlencode
from authorization import AuthorizationCodeFlow, ClientCredentialsFlow


class Base(object):

    def __init__(self, credential_object):
        if not isinstance(credential_object, (AuthorizationCodeFlow, ClientCredentialsFlow)):
            raise Exception("Invalid credential object")
        self.credentials = credential_object
        self.base_url = "https://api.spotify.com/v1/"

    def header(self):
        # done
        headers = {
            "Authorization": f"{self.credentials.token_type} {self.credentials.access_token}",
        }
        return headers

    def application_header(self):
        # done
        headers = {
            'Authorization': 'Bearer {token}'.format(token=self.credentials.access_token),
            'Content-Type': 'application/json'
        }
        return headers

    def get_current_profile(self):
        # done
        endpoint = "me"
        response = self.retrieve_request(endpoint)
        # check if "response" is an error
        return response

    def get_user_profile(self, user_id):
        # done
        endpoint = f"users/{user_id}"
        response = self.retrieve_request(endpoint)
        # check if response is an error
        return response

    def search(self, query={}, search_type=[], limit=20, operator=None, operator_query=None):
        # done
        if not isinstance(query, dict):
            raise Exception("query is a dict")
        elif query == {}:
            raise Exception("A query is required")
        query = " ".join([f"{k}:{v}" for k, v in query.items()])

        if isinstance(search_type, list):
            search_type = ",".join(search_type)
        elif not isinstance(search_type, str):
            raise Exception("search type is a list of type or str")

        if operator is not None and operator_query is not None:
            if operator.lower() == "or" or operator.lower() == "not":
                operator = operator.upper()
            if isinstance(operator_query, str):
                query = f"{query} {operator} {operator_query}"
        query_params = urlencode({
            "q": query,
            "type": search_type,
            "limit": limit
        })

        return self.retrieve_request("search", query_params)

    def retrieve_request(self, endpoint, request_params=None):  # get
        if request_params is None:
            endpoint = f"{self.base_url}{endpoint}"
        else:
            endpoint = f"{self.base_url}{endpoint}?{request_params}"

        response = requests.get(endpoint, headers=self.header())
        print(response.status_code)
        print(response.url)
        if response.status_code != 200:
            raise Exception("Invalid GET request")  # turn this into a statement

        return response.json()

    def post_request(self, endpoint, data=None, request_params=None):  # post
        if request_params is None:
            endpoint = f"{self.base_url}{endpoint}"
            response = requests.post(endpoint, data=json.dumps(data), headers=self.application_header())
        else:
            endpoint = f"{self.base_url}{endpoint}?{request_params}"
            response = requests.post(endpoint, headers=self.header())
        print(response.url)
        print(response.status_code)
        print(response.json())
        if response.status_code not in range(200, 299):  # check for 201
            raise Exception("Invalid POST request")  # turn this into a statement

        return response.json()

    def put_request(self, endpoint, data=None):
        endpoint = f"{self.base_url}{endpoint}"
        if data is None:
            response = requests.put(endpoint, headers=self.application_header())
        else:
            response = requests.put(endpoint, data=json.dumps(data), headers=self.application_header())

        print(response.status_code)
        print(response.json())

        if response.status_code not in range(200, 299):  # check for 201
            raise Exception("Invalid PUT request")  # turn this into a statement

        return response

    def delete_request(self, endpoint, data):
        endpoint = f"{self.base_url}{endpoint}"

        response = requests.delete(endpoint, data=json.dumps(data), headers=self.header())
        print(response.status_code)
        print(response.json())
        if response.status_code != 200:
            raise Exception("Invalid DELETE request")  # turn this into a statement

        return response.json()

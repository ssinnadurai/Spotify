from urllib.parse import urlencode
import json
import requests

from base import Base


class Playlist(Base):

    def __init__(self, credential_object):
        super().__init__(credential_object)

    def create_playlist(self, playlist_name, description="new playlist", public=False, collaborative=False):
        # done
        """  maybe validate scope require:
          -- playlist-modify-public
          -- playlist-modify-private
        """

        user_id = self.get_current_profile()['id']
        # handle error

        endpoint = f"users/{user_id}/playlists"
        query_params = {
            "name": playlist_name,
            "description": description,
            "collaborative": collaborative,
            "public": public
        }
        response = self.post_request(endpoint, data=query_params)
        # validate response
        print(response.status_code)
        print(response.json())
        return response

    def get_current_user_playlist(self, limit=20, offset=0):
        endpoint = "me/playlists"
        if limit not in range(1, 51):
            return False  # statement

        if offset < 0 or offset > 100000:
            return False  # statement
        response = self.retrieve_request(endpoint)
        # check for response for error
        return response

    def get_user_playlist(self, user_id, limit=20, offset=0):
        endpoint = f"users/{user_id}/playlists"
        if limit not in range(1, 51):
            return False  # statement

        if limit < 0 or limit > 100000:
            return False  # statement
        response = self.retrieve_request(endpoint)
        # check for response for error
        return response

    def get_playlist(self, playlist_id, field=None, market=None, addition_types="track"):
        endpoint = f"playlists/{playlist_id}"

        query_params = {
            "addition_types": addition_types
        }

        if field is not None:
            query_params['fields'] = field

        if market is not None:
            query_params['market'] = market

        query_params = urlencode(query_params)
        response = self.retrieve_request(endpoint, query_params)
        # check response for error
        return response

    def add_to_playlists(self, playlist_id, track_uris=[], position=None):
        # done
        endpoint = f"playlists/{playlist_id}/tracks"
        query_params = {}
        if isinstance(track_uris, str):
            query_params['uris'] = track_uris
            if position is not None:
                query_params['position'] = position
            query_params = urlencode(query_params)
            response = self.post_request(endpoint, request_params=query_params)
        else:
            if len(track_uris) > 100 or len(track_uris) == 0:
                return False
            query_params = {
                "uris": track_uris
            }
            if position is not None:
                query_params['position'] = position
            response = self.post_request(endpoint, data=query_params)

        # validate response and check for error

        return response

    def get_items_from_playlist(self, playlist_id, fields=None, limit=100, offset=0, market=None, addition_types=None):
        # done
        endpoint = f"playlists/{playlist_id}/tracks"

        query_params = {
            "offset": offset
        }

        if fields is not None:
            query_params['fields'] = fields

        if limit in range(1, 101):
            query_params['limit'] = limit

        if market is not None:
            query_params['market'] = market

        if addition_types is not None:
            query_params["addition_types"] = addition_types

        query_params = urlencode(query_params)
        response = self.retrieve_request(endpoint, query_params)
        # validate response and check for error

        return response

    def modify_playlists(self, playlist_id, name, public=False, collaborative=False, description="Updated"):
        # change a playlist details
        # done

        endpoint = f"playlists/{playlist_id}"
        query_params = {
            "name": name,
            "public": public,
            "collaborative": collaborative,
            "description": description
        }

        response = self.put_request(endpoint, query_params)
        # validate response and check for error

        return response

    def get_playlist_cover(self, playlist_id):
        # done
        endpoint = f"playlists/{playlist_id}/tracks"

        response = self.retrieve_request(endpoint)
        # validate response and check for error

        return response

    def remove_tracks_from_playlist(self, playlist_id, uris=[], position=None, snapshot_id=""):
        # done
        endpoint = f"playlists/{playlist_id}/tracks"
        uri_dict = {}
        tracks = []
        position_flag = True

        if len(uris) == 0 or len(uris) > 100:
            return False

        if position is None:
            position_flag = False
        elif not isinstance(position, list):
            return False  # error
        elif isinstance(position, list) and len(position) != len(uris):
            return False

        for i in range(0, len(uris)):
            uri_dict['uri'] = uris[i]
            if position_flag:
                uri_dict['positions'] = position[i]
            tracks.append(uri_dict)

        print(tracks)
        query_params = {
            "tracks": tracks
        }
        print(query_params)

        if snapshot_id != "":
            query_params['snapshot_id'] = snapshot_id

        response = self.delete_request(endpoint, query_params)
        return response

    def reorder_playlist(self):
        endpoint = ""
        pass

    def update_playlist(self, playlist_id, uris=[]):
        endpoint = f"playlists/{playlist_id}/tracks"
        query_params = {}
        if isinstance(uris, str):
            query_params['uris'] = uris
        elif isinstance(uris, list):
            if len(uris) > 100:
                return False

            query_params['uris'] = uris

        response = self.put_request(endpoint, query_params)

        return response

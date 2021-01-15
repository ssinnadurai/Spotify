from base import Base
from urllib.parse import urlencode
from playlist import Playlist


class Player(Base):

    def __init__(self, credential_object):
        super().__init__(credential_object)
        self.player_endpoint = "me/player"

    def get_devices(self):
        # 	Get a User's Available Devices
        # user-read-playback-state
        endpoint = f"{self.player_endpoint}/devices"

        response = self.retrieve_request(endpoint)
        # validate response

        return response

    def get_current_playback(self, market=None, additional_types= None):
        # Get Information About The User's Current Playback
        # user-read-playback-state
        endpoint = "me/player"
        query_params = {}
        if additional_types is not None:
            query_params['additional_types'] = additional_types

        if market is not market:
            query_params['market'] = market

        response = self.retrieve_request(endpoint, urlencode(query_params))
        # validate 'response'

        return response

    def get_recently_played(self, limit=20, after=None, before=None):
        # Get Current User's Recently Played Tracks
        # user-read-recently-played
        endpoint = f"{self.player_endpoint}/recently-played"
        query_params = {}
        if limit not in range(1, 51):
            return False

        if after is None and before is not None:
            return False
        elif after is not None and before is None:
            return False
        elif after is not None and before is not None:
            query_params['after'] = after
            query_params['before'] = before

        response = self.retrieve_request(endpoint, urlencode(query_params))
        # validate 'response'
        return response

    def get_currently_playing(self, market=None, additional_types=None):
        # Get the User's Currently Playing Track
        # user-read-currently-playing user-read-playback-state
        endpoint = f"{self.player_endpoint}/currently-playing"
        query_params = {}
        if additional_types is not None:
            query_params['additional_types'] = additional_types

        if market is not market:
            query_params['market'] = market

        response = self.retrieve_request(endpoint, urlencode(query_params))
        # validate 'response'

        return response
        pass

    def pause(self, device_id=None):
        # Pause a User's Playback
        # user-modify-playback-state
        endpoint = f"{self.player_endpoint}/pause"
        if device_id is not None:
            query_params = {
                "device_id": device_id
            }
            response = self.put_request(endpoint, query_params)
        else:
            response = self.put_request(endpoint)

        # validate 'response'

        return response

    def seek(self, position_ms, device_id=None):
        # 	Seek To Position In Currently Playing Track
        # user-modify-playback-state

        endpoint = f'{self.player_endpoint}/seek'
        query_params = {}

        if position_ms < 0:
            return False
        else:
            query_params['position_ms'] = position_ms

        if device_id is not None:
            query_params['device_id']: device_id

        response = self.put_request(endpoint, query_params)
        #  validate response

        return response

    def set_repeat_mode(self, state, device_id=None):
        # Set Repeat Mode On User’s Playback
        # user-modify-playback-state
        endpoint = f'{self.player_endpoint}/repeat'
        query_params = {}

        if state not in ["track", "context", "off"]:
            return False
        else:
            query_params['state'] = state

        if device_id is not None:
            query_params['device_id']: device_id

        response = self.put_request(endpoint, query_params)

        return response

    def volume(self, volume_percent, device_id=None):
        # Set Volume For User's Playback
        # user-modify-playback-state
        endpoint = f'{self.player_endpoint}/volume'
        query_params = {}

        if volume_percent not in range(0, 101):
            return False
        else:
            query_params['volume_percent'] = volume_percent

        if device_id is not None:
            query_params['device_id']: device_id

        response = self.put_request(endpoint, query_params)

        return response

    def next(self, device_id=None):
        # Skip User’s Playback To Next Track
        # user-modify-playback-state
        endpoint = f'{self.player_endpoint}/next'
        query_params = {}
        if device_id is not None:
            query_params['device_id']: device_id
            response = self.post_request(endpoint, query_params)
        else:
            response = self.post_request(endpoint)

        #  validate response

        return response

    def previous(self, device_id=None):
        # Skip User’s Playback To Previous Track
        # user-modify-playback-state

        endpoint = f'{self.player_endpoint}/previous'
        query_params = {}
        if device_id is not None:
            query_params['device_id']: device_id
            response = self.post_request(endpoint, query_params)
        else:
            response = self.post_request(endpoint)

        return response

    def play(self, uris=None, position_or_uri=None, position_ms=None, device_id=None):
        # Start/Resume a User's Playback
        # user-modify-playback-state
        # need premium
        endpoint = f"{self.player_endpoint}/play"
        query_params = {}
        if uris is not None:
            if isinstance(uris, str):
                query_params['context_uri'] = uris
            elif isinstance(uris, list):
                query_params['uris'] = uris

            if position_or_uri is not None:
                if 'context_uri' in query_params:
                    if 'spotify:album' in query_params['context_uri'] or 'spotify:playlist' in \
                            query_params['context_uri']:

                        if isinstance(position_or_uri, int):
                            if position_or_uri >= 0:
                                query_params['offset']['position'] = position_or_uri
                        else:
                            query_params['offset']['uri'] = position_or_uri
                    else:
                        return False
                elif 'uris' in query_params:
                    if isinstance(position_or_uri, int):
                        if position_or_uri >= 0:
                            query_params['offset']['position'] = position_or_uri
                    else:
                        query_params['offset']['uri'] = position_or_uri

        if position_ms is not None:
            if isinstance(position_ms, int) and position_ms >= 0:
                query_params['position_ms'] = position_ms

        if device_id is not None:
            endpoint = f"{endpoint}?device_id={device_id}"

        if query_params == {}:
            response = self.put_request(endpoint)
        else:
            response = self.put_request(endpoint, query_params)

        #   validate response

        return response

    def shuffle(self, state, device_id=None):
        # Toggle Shuffle For User’s Playback
        # user-modify-playback-state
        endpoint = f'{self.player_endpoint}/shuffle'
        query_params = {
            "state": state
        }

        if device_id is not None:
            query_params['device_id'] = device_id

        query_params = urlencode(query_params)
        endpoint = f'{endpoint}?{query_params}'

        response = self.put_request(endpoint)
        # validate response
        return response

    def player(self, device_id, play=False):
        # 	Transfer a User's Playback
        # user-modify-playback-state
        endpoint = f'me/player'
        query_params = {
            "device_ids": [device_id],
            "play": play
        }

        response = self.put_request(endpoint, query_params)
        # validate response
        return response

    def add_to_queue(self, uri, device_id=None):
        # Add an Item to the User's Playback Queue
        # user-modify-playback-state
        endpoint = f'{self.player_endpoint}/queue'
        query_params = {
            'uri': uri,
        }

        if device_id is not None:
            query_params['device_id'] = device_id

        response = self.post_request(endpoint, urlencode(query_params))
        # validate 'response'

        return response

from base import Base
from urllib.parse import urlencode


class Albums(Base):
    def __init__(self, credential_object):
        super().__init__(credential_object)
        self.album_endpoint = 'albums'

    def get_albums(self, album_ids, market=None):
        endpoint = self.album_endpoint
        query_params = {}

        if len(album_ids) > 20:
            return False

        album_ids = ','.join(album_ids)

        query_params['ids'] = album_ids

        if market is not None:
            query_params['market'] = market

        response = self.retrieve_request(endpoint, urlencode(query_params))

        #     validate 'response'

        return response

    def get_album(self, album_id, market=None):
        endpoint = f'{self.album_endpoint}/{album_id}'
        query_params = {}
        if market is not None:
            query_params['market'] = market
            response = self.retrieve_request(endpoint, urlencode(query_params))
        else:
            response = self.retrieve_request(endpoint)

        # validate response
        return response

    def tracks_from_album(self, album_id, limit=20, offset=0, market=None):
        endpoint = f'{self.album_endpoint}/{album_id}/tracks'

        if limit not in range(1, 51):
            return False

        query_params = {
            "limit": limit,
            "offset": offset
        }
        if market is not None:
            query_params['market'] = market

        response = self.retrieve_request(endpoint, urlencode(query_params))

        return response


class Artists(Base):
    def __init__(self, credential_object):
        super().__init__(credential_object)
        self.artist_endpoint = 'artists'

    def get_artists(self, artist_ids):
        endpoint = self.artist_endpoint
        query_params = {}

        if len(artist_ids) > 50:
            return False

        artist_ids = ','.join(artist_ids)
        query_params['ids'] = artist_ids
        response = self.retrieve_request(endpoint, urlencode(query_params))
        #     validate 'response'
        return response

    def get_artist(self, artist_id):
        endpoint = f'{self.artist_endpoint}/{artist_id}'
        response = self.retrieve_request(endpoint)

        # validate response
        return response

    def get_albums(self, artist_id, include_groups=[], country=None, limit=20, offset=0):
        endpoint = f'{self.artist_endpoint}/{artist_id}/albums'
        query_params = {}

        # include_groups: album, single, appears_on, compilation

        if include_groups != []:
            query_params['include_groups'] = ",".join(include_groups)

        if country is not None:
            query_params['market'] = country

        if limit in range(1, 51):
            query_params['limit'] = limit
        else:
            return False

        if offset >= 0:
            query_params['offset'] = offset
        else:
            return False

        if query_params == {}:
            response = self.retrieve_request(endpoint)
        else:
            response = self.retrieve_request(endpoint, urlencode(query_params))

        # validate response
        return response

    def get_top_tracks(self, artist_id, country):
        endpoint = f'{self.artist_endpoint}/{artist_id}/top-tracks'
        query_params = {
            'market': country
        }
        response = self.retrieve_request(endpoint, urlencode(query_params))

        # validate response
        return response

        pass

    def get_related_artist(self, artist_id):
        endpoint = f'{self.artist_endpoint}/{artist_id}/related-artists'
        response = self.retrieve_request(endpoint)

        # validate response
        return response


class Episodes(Base):

    def __init__(self, credential_object):
        super().__init__(credential_object)
        self.episodes_endpoint = 'episodes'

    def get_episode(self, episode_id, market=None):
        # user-read-playback-position
        endpoint = f'{self.episodes_endpoint}/{episode_id}'
        query_params = {}
        if market is not None:
            query_params['market'] = market
            response = self.retrieve_request(endpoint, urlencode(query_params))
        else:
            response = self.retrieve_request(endpoint)

        # validate response
        return response
        pass

    def get_episodes(self, episode_ids, market=None):
        # user-read-playback-position
        endpoint = self.episodes_endpoint
        query_params = {}

        if len(episode_ids) > 50:
            return False

        episode_ids = ','.join(episode_ids)
        query_params['ids'] = episode_ids
        if market is not None:
            query_params['market'] = market
        response = self.retrieve_request(endpoint, urlencode(query_params))
        #     validate 'response'
        return response


class Shows(Base):
    def __init__(self, credential_object):
        super().__init__(credential_object)
        self.shows_endpoint = 'shows'

    def get_shows(self, show_ids, market=None):
        # user-read-playback-position
        endpoint = self.shows_endpoint
        query_params = {}

        if len(show_ids) > 50:
            return False

        album_ids = ','.join(show_ids)

        query_params['ids'] = album_ids

        if market is not None:
            query_params['market'] = market

        response = self.retrieve_request(endpoint, urlencode(query_params))

        #     validate 'response'

        return response
        pass

    def get_show(self, show_id, market=None):
        # user-read-playback-position
        endpoint = f'{self.shows_endpoint}/{show_id}'
        query_params = {}
        if market is not None:
            query_params['market'] = market
            response = self.retrieve_request(endpoint, urlencode(query_params))
        else:
            response = self.retrieve_request(endpoint)

        # validate response
        return response

    def get_episodes(self, show_id, limit=20, offset=0, market=None):
        # user-read-playback-position
        endpoint = f'{self.shows_endpoint}/{show_id}/episodes'

        if limit not in range(1, 51):
            return False

        query_params = {
            "limit": limit,
            "offset": offset
        }
        if market is not None:
            query_params['market'] = market

        response = self.retrieve_request(endpoint, urlencode(query_params))

        return response


class Tracks(Base):
    def __init__(self, credential_object):
        super().__init__(credential_object)
        self.tracks_endpoint = 'tracks'

    def audio_analysis(self, track_id):
        endpoint = f'audio-analysis/{track_id}'

        response = self.retrieve_request(endpoint)

        return response

    def audio_feature_track(self, track_id):
        endpoint = f'audio-features/{track_id}'
        response = self.retrieve_request(endpoint)
        # validate response
        return response

    # fix this
    def audio_feature_tracks(self, track_ids):
        endpoint = f'audio-features'
        query_params = {}
        if len(track_ids) > 100:
            return False

        track_ids = ','.join(track_ids)
        query_params['ids'] = track_ids
        response = self.retrieve_request(endpoint, urlencode(query_params))
        # validate response

        return response

    def get_tracks(self, track_ids, market=None):
        endpoint = self.tracks_endpoint
        query_params = {}

        if len(track_ids) > 50:
            return False

        track_ids = ','.join(track_ids)
        query_params['ids'] = track_ids

        if market is not None:
            query_params['market'] = market

        response = self.retrieve_request(endpoint, urlencode(query_params))
        # validate 'response'
        return response

    def get_track(self, track_id, market=None):
        endpoint = f'{self.tracks_endpoint}/{track_id}'
        query_params = {}
        if market is not None:
            query_params['market'] = market
            response = self.retrieve_request(endpoint, urlencode(query_params))
        else:
            response = self.retrieve_request(endpoint)

        # validate response
        return response

import json
import uuid

import falcon


_songs = {
    'song-1': {
        'id': 'song-1',
        'name': 'Future world',
        'album': 'album-1'
    },
    'song-2': {
        'id': 'song-2',
        'name': 'Lust for life',
        'album': 'album-2'
    },
    'song-3': {
        'id': 'song-3',
        'name': 'Space eater',
        'album': 'album-2'
    },
    'song-4': {
        'id': 'song-4',
        'name': 'Hunting high and low',
        'album': 'album-3'
    }
}


class Songs:
    """API resource for the collection of songs.
    """

    def on_get(self, req, resp):
        """Retrieve the list of songs.

        :param `falcon.Request` req: HTTP request.
        :param `falcon.Response` resp: HTTP response.
        """

        albums = req.get_param_as_list('album')
        if albums:
            songs = [song for song in _songs.values() if song['album'] in albums]
        else:
            songs = list(_songs.values())

        resp.body = json.dumps(songs)
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        """Create a song.

        :param `falcon.Request` req: HTTP request.
        :param `falcon.Response` resp: HTTP response.
        """

        # Check request's body... some input validation should be done here
        #
        payload = req.stream.read().decode('utf-8')
        if not payload:
            raise falcon.HTTPBadRequest(title='Empty body',
                                        description='Valid JSON document required')
        try:
            song = json.loads(payload)
        except ValueError:
            raise falcon.HTTPBadRequest(title='Invalid body',
                                        description='Valid JSON document required')

        # Update collection with new resource
        #
        song['id'] = uuid.uuid4().hex
        _songs.update({song['id']: song})

        # Return response with location header
        #
        resp.set_header('Location', '%s/%s' % (req.uri, song['id']))
        resp.body = json.dumps(song)
        resp.status = falcon.HTTP_201


class Song:
    """API resource for a song.
    """

    def on_get(self, req, resp, song):
        """Retrieve the requested song.

        :param `falcon.Request` req: HTTP request.
        :param `falcon.Response` resp: HTTP response.
        :param str song: Song id.
        :raises `falcon.HTTPNotFound`: Song not found.
        """

        try:
            song = _songs[song]
        except KeyError:
            raise falcon.HTTPNotFound(title='Not found', description='Song %s not found' % song)

        resp.body = json.dumps(song)
        resp.status = falcon.HTTP_200

    def on_delete(self, req, resp, song):
        """Remove the requested song.

        :param `falcon.Request` req: HTTP request.
        :param `falcon.Response` resp: HTTP response.
        :param str song: Song id.
        :raises `falcon.HTTPNotFound`: Song not found.
        """

        try:
            del _songs[song]
        except KeyError:
            raise falcon.HTTPNotFound(title='Not found', description='Song %s not found' % song)

        resp.status = falcon.HTTP_204

import json
import uuid

import falcon


_albums = {
    'album-1': {
        'id': 'album-1',
        'name': 'The keeper of the seven keys',
        'author': 'Helloween',
        'year': 1987
    },
    'album-2': {
        'id': 'album-2',
        'name': 'Heading for tomorrow',
        'author': 'Gamma Ray',
        'year': 1990
    },
    'album-3': {
        'id': 'album-3',
        'name': 'Infinite',
        'author': 'Stratovarius',
        'year': 2000
    }
}


class Albums:
    """API resource for the collection of albums.
    """

    def on_get(self, req, resp):
        """Retrieve the list of power metal albums.

        :param `falcon.Request` req: HTTP request.
        :param `falcon.Response` resp: HTTP response.
        """

        resp.body = json.dumps(_albums.values())
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        """Create an album.

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
            album = json.loads(payload)
        except ValueError:
            raise falcon.HTTPBadRequest(title='Invalid body',
                                        description='Valid JSON document required')

        # Update collection with new resource
        #
        album.update({'id': uuid.uuid4().hex})
        _albums.update({album['id']: album})

        # Return response with location header
        #
        resp.set_header('Location', '%s/%s' % (req.uri, album['id']))
        resp.body = json.dumps(album)
        resp.status = falcon.HTTP_201


class Album:
    """API resource for an album.
    """

    def on_get(self, req, resp, album):
        """Retrieve the requested album.

        :param `falcon.Request` req: HTTP request.
        :param `falcon.Response` resp: HTTP response.
        :param str album: Album id.
        :raises `falcon.HTTPNotFound`: Album not found.
        """

        try:
            album = _albums[album]
        except KeyError:
            raise falcon.HTTPNotFound(title='Not found', description='Album %s not found' % album)

        resp.body = json.dumps(album)
        resp.status = falcon.HTTP_200

    def on_delete(self, req, resp, album):
        """Remove the requested album.

        :param `falcon.Request` req: HTTP request.
        :param `falcon.Response` resp: HTTP response.
        :param str album: Album id.
        :raises `falcon.HTTPNotFound`: Album not found.
        """

        try:
            del _albums[album]
        except KeyError:
            raise falcon.HTTPNotFound(title='Not found', description='Album %s not found' % album)

        resp.status = falcon.HTTP_204

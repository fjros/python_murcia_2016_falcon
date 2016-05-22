import json

import falcon
from falcon import testing

from music import api


class TestAlbum(testing.TestBase):

    albums_uri = '/v1/albums'

    def before(self):
        self.api = api

    def after(self):
        pass

    def test_retrieve_albums(self):
        body = self.simulate_request(method='GET', path=self.albums_uri, decode='utf-8')

        self.assertEqual(self.srmock.status, falcon.HTTP_200)
        self.assertIn('application/json', self.srmock.headers_dict['Content-Type'])
        self.assertIsNotNone(body)
        albums = json.loads(body)
        self.assertGreater(len(albums), 0)
        for album in albums:
            self.assertIsInstance(album['id'], str)
            self.assertIsInstance(album['name'], str)
            self.assertIsInstance(album['author'], str)
            self.assertIsInstance(album['year'], int)

    def test_create_album(self):
        new_album = {
            'name': 'Ride the lightning',
            'author': 'Metallica',
            'year': 1984
        }
        body = self.simulate_request(method='POST',
                                     path=self.albums_uri,
                                     body=json.dumps(new_album),
                                     decode='utf-8')

        self.assertEqual(self.srmock.status, falcon.HTTP_201)
        self.assertIn('application/json', self.srmock.headers_dict['Content-Type'])
        self.assertRegex(self.srmock.headers_dict['Location'], '^https?://.+/v1/albums/[^/]+$')
        self.assertIsNotNone(body)
        album = json.loads(body)
        self.assertIsInstance(album['id'], str)
        self.assertEqual(album['name'], new_album['name'])
        self.assertEqual(album['author'], new_album['author'])
        self.assertEqual(album['year'], new_album['year'])

    def test_retrieve_album(self):
        album_id = 'album-1'
        body = self.simulate_request(method='GET',
                                     path='%s/%s' % (self.albums_uri, album_id),
                                     decode='utf-8')

        self.assertEqual(self.srmock.status, falcon.HTTP_200)
        self.assertIn('application/json', self.srmock.headers_dict['Content-Type'])
        self.assertIsNotNone(body)
        album = json.loads(body)
        self.assertEqual(album['id'], album_id)
        self.assertEqual(album['name'], 'The keeper of the seven keys')
        self.assertEqual(album['author'], 'Helloween')
        self.assertEqual(album['year'], 1987)

    def test_retrieve_album_not_found(self):
        album_id = 'unknown'
        self.simulate_request(method='GET',
                              path='%s/%s' % (self.albums_uri, album_id),
                              decode='utf-8')

        self.assertEqual(self.srmock.status, falcon.HTTP_404)

    def test_remove_album(self):
        album_id = 'album-3'
        self.simulate_request(method='DELETE',
                              path='%s/%s' % (self.albums_uri, album_id),
                              decode='utf-8')

        self.assertEqual(self.srmock.status, falcon.HTTP_204)

    def test_remove_album_not_found(self):
        album_id = 'unknown'
        self.simulate_request(method='DELETE',
                              path='%s/%s' % (self.albums_uri, album_id),
                              decode='utf-8')

        self.assertEqual(self.srmock.status, falcon.HTTP_404)

import json

import falcon
from falcon import testing

from music import api


class TestSong(testing.TestBase):

    songs_uri = '/v1/songs'

    def before(self):
        self.api = api

    def after(self):
        pass

    def test_retrieve_songs(self):
        body = self.simulate_request(method='GET', path=self.songs_uri, decode='utf-8')

        self.assertEqual(self.srmock.status, falcon.HTTP_200)
        self.assertIn('application/json', self.srmock.headers_dict['Content-Type'])
        self.assertIsNotNone(body)
        songs = json.loads(body)
        self.assertGreater(len(songs), 0)
        for song in songs:
            self.assertIsInstance(song['id'], str)
            self.assertIsInstance(song['name'], str)
            self.assertIsInstance(song['album'], str)

    def test_retrieve_songs_filtered_by_album(self):
        album_id = 'album-1'
        body = self.simulate_request(method='GET',
                                     path=self.songs_uri,
                                     query_string='album=%s' % album_id,
                                     decode='utf-8')

        self.assertEqual(self.srmock.status, falcon.HTTP_200)
        self.assertIn('application/json', self.srmock.headers_dict['Content-Type'])
        self.assertIsNotNone(body)
        songs = json.loads(body)
        self.assertGreater(len(songs), 0)
        for song in songs:
            self.assertEqual(song['album'], album_id)

    def test_retrieve_songs_filtered_by_albums(self):
        album_ids = 'album-1,album-2'
        body = self.simulate_request(method='GET',
                                     path=self.songs_uri,
                                     query_string='album=%s' % album_ids,
                                     decode='utf-8')

        self.assertEqual(self.srmock.status, falcon.HTTP_200)
        self.assertIn('application/json', self.srmock.headers_dict['Content-Type'])
        self.assertIsNotNone(body)
        songs = json.loads(body)
        self.assertGreater(len(songs), 0)
        for song in songs:
            self.assertIn(song['album'], album_ids.split(','))

    def test_create_song(self):
        new_song = {
            'name': 'Halloween',
            'album': 'album-1'
        }
        body = self.simulate_request(method='POST',
                                     path=self.songs_uri,
                                     body=json.dumps(new_song),
                                     decode='utf-8')

        self.assertEqual(self.srmock.status, falcon.HTTP_201)
        self.assertIn('application/json', self.srmock.headers_dict['Content-Type'])
        self.assertRegexpMatches(self.srmock.headers_dict['Location'],
                                 '^https?://.+/v1/songs/[^/]+$')
        self.assertIsNotNone(body)
        song = json.loads(body)
        self.assertIsInstance(song['id'], str)
        self.assertEqual(song['name'], new_song['name'])
        self.assertEqual(song['album'], new_song['album'])

    def test_retrieve_song(self):
        song_id = 'song-1'
        body = self.simulate_request(method='GET',
                                     path='%s/%s' % (self.songs_uri, song_id),
                                     decode='utf-8')

        self.assertEqual(self.srmock.status, falcon.HTTP_200)
        self.assertIn('application/json', self.srmock.headers_dict['Content-Type'])
        self.assertIsNotNone(body)
        song = json.loads(body)
        self.assertEqual(song['id'], song_id)
        self.assertEqual(song['name'], 'Future world')
        self.assertEqual(song['album'], 'album-1')

    def test_retrieve_song_not_found(self):
        song_id = 'unknown'
        self.simulate_request(method='GET',
                              path='%s/%s' % (self.songs_uri, song_id),
                              decode='utf-8')

        self.assertEqual(self.srmock.status, falcon.HTTP_404)

    def test_remove_song(self):
        song_id = 'song-4'
        self.simulate_request(method='DELETE',
                              path='%s/%s' % (self.songs_uri, song_id),
                              decode='utf-8')

        self.assertEqual(self.srmock.status, falcon.HTTP_204)

    def test_remove_song_not_found(self):
        song_id = 'unknown'
        self.simulate_request(method='DELETE',
                              path='%s/%s' % (self.songs_uri, song_id),
                              decode='utf-8')

        self.assertEqual(self.srmock.status, falcon.HTTP_404)

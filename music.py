import falcon

from api.album import Album, Albums
from api.song import Song, Songs


api = falcon.API()
api.add_route('/v1/albums', Albums())
api.add_route('/v1/albums/{album}', Album())
api.add_route('/v1/songs', Songs())
api.add_route('/v1/songs/{song}', Song())

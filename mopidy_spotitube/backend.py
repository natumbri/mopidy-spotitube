import json

import pykka
from cachetools import TTLCache, cached
from mopidy import backend, httpclient
from mopidy.models import Ref

from mopidy_spotitube import Extension, logger
from mopidy_spotitube.data import extract_playlist_id, extract_user_id
from mopidy_spotitube.spotify import Spotify


class SpotiTubeBackend(pykka.ThreadingActor, backend.Backend):
    def __init__(self, config, audio):
        super().__init__()
        self.config = config
        self.library = SpotiTubeLibraryProvider(backend=self)
        self.users = config["spotitube"]["spotify_users"]
        self.uri_schemes = ["spotitube"]
        self.user_agent = "{}/{}".format(Extension.dist_name, Extension.version)

    def on_start(self):
        proxy = httpclient.format_proxy(self.config["proxy"])
        headers = {
            "user-agent": httpclient.format_user_agent(self.user_agent),
            "Cookie": "PREF=hl=en; CONSENT=YES+20210329;",
            "Accept-Language": "en;q=0.8",
        }
        self.library.spotify = Spotify(proxy, headers)


class SpotiTubeLibraryProvider(backend.LibraryProvider):

    """
    Called when root_directory is set to [insert description]
    When enabled makes possible to browse the users listed in
    config["spotitube"]["spotify_users"] and to browse their
    public playlists and the separate tracks those playlists.
    """

    root_directory = Ref.directory(uri="spotitube:browse", name="SpotiTube")

    cache_max_len = 4000
    cache_ttl = 21600

    spotify_cache = TTLCache(maxsize=cache_max_len, ttl=cache_ttl)

    @cached(cache=spotify_cache)
    def browse(self, uri):

        # if we're browsing, return a list of directories
        if uri == "spotitube:browse":
            return [
                Ref.directory(uri="spotitube:user:root", name="Spotify Users"),
                # Ref.directory(
                #     uri="spotitube:playlist:root", name="Spotify Playlists"
                # ),
            ]

        # if we're looking at users, return a list of users
        # extract names and uris, return a list of Refs
        if uri == "spotitube:user:root":
            directoryrefs = []
            for user in self.backend.users:
                user_details = self.spotify.get_spotify_user_details(user)
                directoryrefs.append(
                    Ref.directory(
                        uri=f"spotitube:user:{user}",
                        name=user_details["display_name"],
                    )
                )
            return directoryrefs

        # if we're looking at a spotify user, return a list of playlists
        elif extract_user_id(uri):
            logger.debug(f"browse spotify user {uri}")
            playlistrefs = []
            playlists = self.spotify.get_spotify_user_playlists(
                extract_user_id(uri)
            )
            playlistrefs = [
                Ref.directory(
                    uri=f"spotitube:playlist:{playlist['id']}",
                    name=playlist["name"],
                )
                for playlist in playlists
                if playlist["id"]
            ]
            return playlistrefs

        # if we're looking at a spotify playlist, return a list of tracks
        elif extract_playlist_id(uri):
            logger.debug(f"browse spotify playlist {uri}")
            trackrefs = []
            tracks = self.spotify.get_spotify_playlist_tracks(
                extract_playlist_id(uri)
            )

            trackrefs = [
                Ref.track(
                    uri=f"yt:video:{track['videoId']}",
                    name=track["title"],
                )
                for track in tracks
                if "videoId" in track
            ]
            trackrefs[0] = Ref.track(
                uri=(
                    f"yt:video:{tracks[0]['videoId']}"
                    f":preload:"
                    f"{json.dumps([track for track in tracks if track is not None])}"
                ),
                name=tracks[0]["title"],
            )
            return trackrefs

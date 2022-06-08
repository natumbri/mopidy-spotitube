import json
from concurrent.futures.thread import ThreadPoolExecutor

from bs4 import BeautifulSoup as bs
from mopidy_youtube.comms import Client

from mopidy_spotitube import logger
from mopidy_spotitube.yt_provider import search_and_get_best_match


class Spotify(Client):
    @classmethod
    def get_spotify_headers(cls, endpoint):

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
        }
        # Getting the access token first to send it with the header to the api endpoint
        page = cls.session.get(endpoint, headers=headers)
        soup = bs(page.text, "html.parser")
        logger.debug(f"get_spotify_headers base url: {endpoint}")
        access_token_tag = soup.find("script", {"id": "config"})
        json_obj = json.loads(access_token_tag.contents[0])  # text)
        access_token_text = json_obj["accessToken"]
        headers.update(
            {
                "authorization": f"Bearer {access_token_text}",
                "referer": endpoint,
                "accept": "application/json",
                "app-platform": "WebPlayer",
            }
        )
        return headers

    @classmethod
    def get_spotify_user_details(cls, user):
        endpoint = f"https://api.spotify.com/v1/users/{user}"
        headers = cls.get_spotify_headers(
            f"https://open.spotify.com/user/{user}"
        )
        url_params = {}
        data = cls.session.get(
            endpoint, params=url_params, headers=headers
        ).json()
        return data

    @classmethod
    def get_spotify_user_playlists(cls, user):
        endpoint = f"https://api.spotify.com/v1/users/{user}/playlists"
        headers = cls.get_spotify_headers(
            f"https://open.spotify.com/user/{user}"
        )
        url_params = {}
        data = cls.session.get(
            endpoint, params=url_params, headers=headers
        ).json()
        playlists = data["items"]
        return [
            {"name": playlist["name"], "id": playlist["id"]}
            for playlist in playlists
        ]

    @classmethod
    def get_spotify_playlist_tracks(cls, playlist):
        # get tracks for each playlist and translate to ytm
        endpoint = f"https://api.spotify.com/v1/playlists/{playlist}"
        headers = cls.get_spotify_headers(
            f"https://open.spotify.com/playlist/{playlist}"
        )
        url_paramters = {}
        data = cls.session.get(
            endpoint, params=url_paramters, headers=headers
        ).json()
        items = data["tracks"]["items"]

        tracks = [
            {
                "song_name": item["track"]["name"],
                "song_artists": [
                    artist["name"] for artist in item["track"]["artists"]
                ],
                "song_duration": item["track"]["duration_ms"] // 1000,
                "isrc": item["track"]["external_ids"].get("isrc"),
            }
            for item in items
        ]

        # without multithreading
        # [track.update({"uri": search_and_get_best_match(**track)}) for track in tracks]

        # search_and_get_best_match is slow, so with multithreading
        # but have to use a wrapper to pass a dict
        def search_and_get_best_match_wrapper(track):
            track.update({"id": search_and_get_best_match(**track)})
            return track

        results = []

        with ThreadPoolExecutor() as executor:
            futures = executor.map(search_and_get_best_match_wrapper, tracks)
            [results.append(value) for value in futures if value is not None]

        return results

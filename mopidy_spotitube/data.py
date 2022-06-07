import re

# from urllib.parse import parse_qs, urlparse

uri_playlist_regex = re.compile("^(?:spotitube):playlist:(?P<playlistid>.+)$")
uri_user_regex = re.compile("^(?:spotitube):user:(?P<userid>.+)$")


def format_playlist_uri(id) -> str:
    return f"spotitube:playlist:{id}"


def extract_playlist_id(uri) -> str:
    match = uri_playlist_regex.match(uri)
    if match:
        return match.group("playlistid")
    return ""


def format_user_uri(id) -> str:
    return f"spotitube:user:{id}"


def extract_user_id(uri) -> str:
    match = uri_user_regex.match(uri)
    if match:
        return match.group("userid")
    return ""

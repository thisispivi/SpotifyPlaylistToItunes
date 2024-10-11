import csv
import struct
import urllib.parse, urllib.request
import json


def retrieve_itunes_identifier(title, artist):
    headers = {
        "X-Apple-Store-Front": "143446-10,32 ab:rSwnYxS0 t:music2",
        "X-Apple-Tz": "7200",
    }
    url = (
        "https://itunes.apple.com/WebObjects/MZStore.woa/wa/search?clientApplication=MusicPlayer&term="
        + urllib.parse.quote(title)
    )
    request = urllib.request.Request(url, None, headers)

    try:
        response = urllib.request.urlopen(request)
        data = json.loads(response.read().decode("utf-8"))
        songs = [
            result
            for result in data["storePlatformData"]["lockup"]["results"].values()
            if result["kind"] == "song"
        ]

        for song in songs:
            if song["name"].lower() == title.lower() and (
                song["artistName"].lower() in artist.lower()
                or artist.lower() in song["artistName"].lower()
            ):
                return song["id"]

        for song in songs:
            if song["name"].lower() == title.lower():
                return song["id"]

    except:
        return None


def identify(df):
    itunes_identifiers = []

    for row in df.itertuples():
        title, artist = row.track_name, row.artist_name
        itunes_identifier = retrieve_itunes_identifier(title, artist)

        if itunes_identifier:
            itunes_identifiers.append(itunes_identifier)
            print("{} - {} => {}".format(title, artist, itunes_identifier))
        else:
            itunes_identifiers.append(None)
            print("{} - {} => Not Found".format(title, artist))
    return itunes_identifiers

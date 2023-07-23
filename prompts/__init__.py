SONG_ID_NORMALIZATION = """
Please extract song information from the following JSON payloads. Only respond using JSON with no extra text.

Please respond in JSON format using the following schema for a match:

{ song: string, artist: string, album: string, link: string}

And the following JSON format if there's no match or for other miscellaneous errors:

{ song: null, error: string }
"""
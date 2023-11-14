## The SeasideFM AI + Botsuro API

What is this?

This project was created to unite all of the various AI functions and chat bot elements into one single project.
I previously had multiple projects all duplicating the same calls, the same queries, and the same OpenAI calls so I decided to combine them all into one project.

## Setup
This project assumes you have a Redis database, a MongoDB database, and multiple bot tokens.
I'll eventually update this README into how to get those, but this README is more for hiring managers to read than for public developers :)

- Get the dependencies with poetry: `poetry install`
- Populate your `.env` with the following (filling in your own data)
```shell
DISCOGS_ACCESS_TOKEN=...
OPENAI_TOKEN=...
OPEN_WEATHER_MAP_TOKEN=... # for weather function
SONG_ID_URL=... # This is the other song-id repository
DATABASE_URL=mongodb://localhost:27017
REDIS_URL=redis://localhost:6379
```
- You'll note that this project does not consume a Twitch or Discord key! That's by design. This API is more or less the "core" API and does not handle platform integrations. (See the botsuro project for that)

## Running

I prefer to use Make to run this project, but you can also use poetry directly.

```shell
make serve
```

or 

```shell
poetry run uvicorn main:app --reload
```

## Roadmap
- This API isn't really an "active development" feature anymore now that I have the chat bot "brains" working, but I do plan to add more here in the near future.
- Next steps:
  - Add a "song ID" endpoint that will return the song ID for the current song in Redis.
  - Store all retrieved songs as the Song ID API is fairly slow and does not store the songs in a database.
  - Add a "song history" endpoint that will return the last 10 songs played.
  - Add a "song search" endpoint that will return the last 10 songs played that match a search query.
  - Allow for users to soft delete faves
  - Connect directly with Sanity better for fetching current bot personalities
  - Finally, allow a user to delete all of their stored chat data without reaching out to me (GDPR compliance)
# Abelard Gacha

The application backend is a Flask app deployed by Vercel. Character images and
the stylesheet are served from `public/`.

## Run locally

1. Copy `.env.example` to `.env` and set the MySQL connection values and a
   private `SESSION_SECRET`.
2. Install dependencies with `pip install -r requirements.txt`.
3. Run `python app.py` and open `http://127.0.0.1:5000`.

The MySQL database must contain the existing `users` and `characters` tables.
`users` needs `id`, `username`, `password`, `gems`, `pity4`, `pity5`, and
`pulls` columns; `characters` needs `id`, `name`, `rarity`, and `img` columns.
Run `migrations/001_user_characters.sql` against the database to create the
per-player character storage table. Run `migrations/002_add_characters.sql` to
add the included character images and rarities.

## Pull rates

Six-star characters have an independent 1-in-10,000 chance. They reset 4-star
pity but do not reset 5-star pity. Five-star characters have a 1-in-1,000 base
chance and are guaranteed by the 100th pull without one. A five-star resets
both pity counters. Four-star characters have a 9% base chance and are
guaranteed at least every 10 pulls.

## Deploy to Vercel

Import the repository into Vercel. It detects the Flask application from
`app.py` and installs dependencies from `requirements.txt`. Add these
environment variables to the Vercel project:

- `SESSION_SECRET`: a long, random secret unique to this deployment
- `MYSQL_HOST`, `MYSQL_PORT`, `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_DATABASE`:
  connection details for a MySQL database reachable from Vercel

Vercel does not provide this MySQL database. The database provider must permit
connections from the deployment and the tables described above must already
exist. Legacy `.php` URLs are rewritten by `vercel.json`.

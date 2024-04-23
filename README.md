# The Book Review Platform

The Book Review Platform (BRP) is a collaborative hub for literary enthusiasts.

## Project Description:

BRP is a dynamic online platform designed to foster a vibrant community of book
lovers, where they can share their thoughts, discover new reads, and engage in
meaningful discussions. With a user-friendly interface and seamless integration
of external APIs, BRP offers an immersive experience for bibliophiles.

## Key Features

1. Book Reviews and Ratings: o Users can write and publish detailed reviews for
   their favorite books. Whether it’s a classic novel, a thrilling mystery, or a
   thought-provoking non-fiction work, BRP provides a space to express opinions
   and insights. o Readers can rate books on a scale of 1 to 5 stars, allowing
   others to gauge the overall quality and popularity of a title.
2. Book Details and Recommendations: o Leveraging an external API, BRP fetches
   comprehensive information about books, including author details, publication
   dates, genres, and cover images. o The platform suggests personalized book
   recommendations based on users’ reading history, preferences, and trending
   titles.

## Running the project

```bash
poetry install
poetry run serve
```

## Style

This projects uses [ruff] as linter and formatter.

To run linter execute the following command:

```bash
poetry run lint
```

To apply linter suggestions run

```bash
poetry run format
```

## Typechecking

This project uses [mypy]

To run typechecker execute the following command:

```bash
poetry run typecheck
```

[ruff]: https://docs.astral.sh/ruff/
[mypy]: https://mypy-lang.org/

## Configuration

Configuration is stored in `settings.toml` and `.secrets.toml` files. Each field
can be overriden by the environment variables with the `BOOK_REVIEW` prefix.

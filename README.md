# The Book Review Platform

<!--toc:start-->

- [The Book Review Platform](#the-book-review-platform)
  - [Project Description:](#project-description)
  - [Key Features](#key-features)
  - [Running the project](#running-the-project)
  - [Style](#style)
  - [Typechecking](#typechecking)
  - [Configuration](#configuration)
  - [Configuration options](#configuration-options)
  <!--toc:end-->

The Book Review Platform (BRP) is a collaborative hub for literary enthusiasts.

## Project Description

BRP is a dynamic online platform designed to foster a vibrant community of book
lovers, where they can share their thoughts, discover new reads, and engage in
meaningful discussions. With a user-friendly interface and seamless integration
of external APIs, BRP offers an immersive experience for bibliophiles.

## Key Features

1. Book Reviews and Ratings:
   - Users can write and publish detailed reviews for their favorite books.
     Whether it’s a classic novel, a thrilling mystery, or a thought-provoking
     non-fiction work, BRP provides a space to express opinions and insights.
   - Readers can rate books on a scale of 1 to 5 stars, allowing others to gauge
     the overall quality and popularity of a title.
2. Book Details and Recommendations:
   - Leveraging an external API, BRP fetches comprehensive information about
     books, including author details, publication dates, genres, and cover
     images.
   - The platform suggests personalized book recommendations based on users’
     reading history, preferences, and trending titles.

## Running the project

```bash
poetry install
poetry run serve
```

Docs will be available at `http://http://127.0.0.1:$PORT/docs`

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

You can see the default values and their description
[here](./book_review/config.py)

## Configuration Options

This paragraph describes the various configuration options available for the application in detail.

**Database:**

- **DB (default: "db.sqlite3")** - Path to the SQLite database file used for storing book review data.

**Server:**

- **PORT (default: 5000)** - Port number on which the HTTP server listens for incoming requests.

**Logging:**

- **DEBUG (default: False)** - Enables debug mode for the application, providing more verbose logging information.

**CORS:**

- **CORS_ALLOWED_ORIGINS (default: ["*"])** - List of allowed origins for Cross-Origin Resource Sharing (CORS). By default, all origins are allowed ("*").

**Security:**

- **SECRET_KEY** - Secret key used for signing and verifying JSON Web Tokens (JWT) for authorization. This value is automatically generated on first run and should be kept confidential. It's recommended to set this value securely using an environment variable or a separate secrets file (.secrets.toml).
- **ALGORITHM (default: "HS256")** - Algorithm used for signing and verifying JWTs.

**Authentication:**

- **ACCESS_TOKEN_EXPIRE_MINUTES (default: 60)** - Expiration time for JWT access tokens in minutes. After this time, the token will no longer be valid and users will need to re-authenticate.

**Caching:**

- **CACHE_EXPIRE_MINUTES (default: 60 * 24)** - Time before the Openlibrary client cache expires in minutes. Cached data from Openlibrary will be reused for this duration before fetching fresh information.

**Openlibrary API:**

- **OPENLIBRARY_BASE_URL (default: "[https://openlibrary.org/](https://openlibrary.org/)")** - Base URL for the Openlibrary API.
- **OPENLIBRARY_COVERS_BASE_URL (default: "[https://covers.openlibrary.org/](https://covers.openlibrary.org/)")** - Base URL for fetching book cover images from Openlibrary.

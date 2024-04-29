# Book Review Platform Web Application

Web application is written in Vue, built with Vite, tested with Vitest (unit tests) and Playwright (E2E tests), linted with ESLint.

## Project Setup

Configure environment variables (copy and edit as needed):

```sh
cp .env.example .env
```

Install dependencies

```sh
npm install
```

Compile and hot-reload for development

```sh
npm run dev
```

Compile and minify for production

```sh
npm run build
```

### Testing

Run unit tests with [Vitest](https://vitest.dev/)

```sh
npm run test:unit
```

Run end-to-end tests with [Playwright](https://playwright.dev)

```sh
# Install browsers for the first run
npx playwright install

# When testing on CI, must build the project first
npm run build

# Runs the end-to-end tests
npm run test:e2e
# Runs the tests only on Chromium
npm run test:e2e -- --project=chromium
# Runs the tests of a specific file
npm run test:e2e -- tests/example.spec.ts
# Runs the tests in debug mode
npm run test:e2e -- --debug
```

## Linting

Lint with [ESLint](https://eslint.org/)

```sh
npm run lint
```

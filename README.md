# QA Portfolio

A repeatable local testing project, plus the original live-site learning scripts preserved separately.

## Run the verified suite

```sh
npm ci
npx playwright install chromium
pip install -r requirements.txt
npm run test:unit
npm test
```

`npm run demo` opens the local QA practice store at http://127.0.0.1:4190. The credentials displayed there are deliberately synthetic. No payment, email, or third-party account service is connected.

## What is tested

- Browser: login rejection, session persistence/logout, cart quantities/removal/totals, checkout, stock, duplicate checkout, API authentication/validation, isolated browser sessions, phone layout.
- Unit: integer money totals, atomic invalid operations, isolated store state, browser cleanup on failure, environment data loading and invalid configuration.
- CI runs the same checks against a local server. Test failures fail the process; no retries mask them. Failure traces/screenshots use only synthetic local data.

## Structure

- `demo/`, `scripts/demo-server.cjs`, `scripts/store.cjs` — local practice target and its actual server-side rules.
- `e2e/` — current Playwright suite.
- `tests/unit/`, `scripts/store.test.cjs` — configuration/lifecycle and store regressions.
- `legacy/selenium/` — original Publix, Shopify, Weather and YouTube exercises.
- `legacy/nike/`, `legacy/cypress/`, `legacy/playwright-starter/` — historical samples, not the current verified suite.

## Historical live-site samples

These are **unverified learning exercises**, not proven production automation. Their hardcoded store routes, selectors, third-party login/CAPTCHA assumptions and incomplete assertions still need site-by-site work.

They are not collected by default. To deliberately run one, install the Python requirements, configure its `QA_<PROJECT>_<KEY>` environment values, and explicitly invoke `python -m pytest --live legacy/selenium/<project>/<file>.py`. The YouTube and signup examples can send messages/create or change real accounts; do not run them casually. No live-site actions were performed during remediation.

Blank values in `test_data.example.json` are configuration slots. Private `test_data.json` and `.env` files are ignored. Old passwords/contact/payment fixtures and screenshots were removed from the current tracked tree; **Git history still contains earlier versions. Rotate any real credentials that were previously published.**

## What went wrong in the original work

1. CI ran Playwright's starter website examples rather than the account workflows described by the README.
2. Some tests only checked the domain after many clicks, or returned True/False instead of asserting the promised outcome.
3. Shopify called a fixture function as a browser; product-creation exceptions were swallowed, and repeated helpers checked the wrong product names.
4. Every script duplicated driver/data fixtures. Failed setup could leak a browser because cleanup was not guarded.
5. Credentials, personal data, browser screenshots and entire installed environments were tracked.
6. Absolute XPath selectors, generated IDs, fixed sleeps and specific account/store routes made scripts brittle and account-dependent.
7. A Nike sample called `time.sleep()` without an argument and used a malformed CSS selector.

The current local suite fixes the repeatability and CI foundation. It does not certify that all archived third-party workflows work today.

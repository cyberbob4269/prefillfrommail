# Email2Report unlock page

Public GitHub Pages site for the **Email2Report** (PrefillFromMail) post-checkout unlock flow.

**Live page:** [cyberbob4269.github.io/prefillfrommail](https://cyberbob4269.github.io/prefillfrommail/)

## What this repo is

After Stripe checkout, customers land here with a `session_id` query parameter. The page calls the unlock API configured in `config.js` and displays the license key and Google Sheet copy link. This repository hosts **only** the static unlock page (`index.html`, `config.js`).

## What this repo is not

- No license keys, customer emails, or Stripe session data are stored here.
- No server-side logic, secrets, or license minting — that runs in private infrastructure.

## Buy Email2Report

Shop: [NetWRx Solutions](https://cyberbob4269.github.io/netwrx-solutions-website/)

| Tier | Price |
|------|-------|
| Kit | £149 |
| Guided | £199 |

## Support

If the unlock page cannot retrieve your key, email [scott@netwrxsolutions.com](mailto:scott@netwrxsolutions.com). Your payment is recorded; support can issue your key manually.

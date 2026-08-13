# PrefillFromMail unlock page

Public GitHub Pages site for the PrefillFromMail (Email2Report) post-checkout unlock flow.

## Security

This repository hosts the **unlock page only** (`index.html`, `config.js`). It must **never** contain license keys, customer emails, or Stripe session payloads. Those live in the private Vera license store and are served by the Cloudflare Worker (`pfm-unlock`).

After payment, customers land here with a `session_id` query parameter. The page fetches the license from the Worker API configured in `config.js` (`window.PFM_API_BASES`). If no Worker URL is set, customers are asked to email support for their key.

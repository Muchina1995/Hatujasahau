# Setting up the content manager (one-time)

This connects the `/admin` panel to your GitHub repo so saving an entry
commits it directly. You only need to do this once.

## 1. Upload these files to your repo

Via GitHub's web UI, add:
- `admin/index.html`
- `admin/config.yml`
- `data/cases/corruption/`, `data/cases/killings/`, `data/cases/promises/`,
  `data/cases/news/` (folders can be empty — Decap CMS creates files as you
  add entries)
- `media/uploads/` (where uploaded photos will land)

## 2. Create a free Netlify account and link your repo

1. Go to netlify.com and sign up (free tier, no card required).
2. "Add new site" → "Import an existing project" → connect your GitHub
   account → select the `hatujasahau` repo.
3. Netlify will try to build/deploy it — that's fine, you can ignore or
   even skip this. You're only using Netlify for the login handshake, not
   hosting. Your real site stays on GitHub Pages at hatujasahau.org.

## 3. Turn on Identity

1. In the Netlify dashboard for that site: **Site configuration → Identity → Enable Identity**.
2. Under **Registration preferences**, set to **Invite only** (so random
   people can't sign themselves up to edit your site).
3. Under **Identity → Emails**, you can customize the invite email if you
   want, but defaults are fine.

## 4. Turn on Git Gateway

1. Still under Identity: **Services → Git Gateway → Enable Git Gateway**.
2. This is what lets the CMS commit to GitHub on your behalf without you
   ever handling a GitHub access token yourself.

## 5. Invite yourself as an editor

1. **Identity → Invite users** → enter your own email.
2. You'll get an email with a link to set a password.
3. That's your login for `hatujasahau.org/admin` going forward.

## 6. Use it

Visit `hatujasahau.org/admin`, log in, and you'll see forms for
Corruption, Killings, In 6 Months, and News. Each entry has a **Timeline**
section at the bottom — click "Add timeline" to log a new development,
with its own date, write-up, optional photo, and sources. Entries save as
drafts (Editorial Workflow) so you can review before publishing — publish
when ready from the CMS's own workflow tab.

## Later: adding more editors

Repeat step 5 for anyone else who should be able to add/edit content —
each person gets their own login, so you always know who made which
change (visible in both the CMS and the repo's commit history).

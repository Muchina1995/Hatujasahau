# Hatujasahau

A public record of government promises, corruption cases, and extrajudicial killings in Kenya. Static site, no build step, no dependencies.

## What's in this repo

```
index.html    the entire site (all pages, styling, and behavior in one file)
CNAME         tells GitHub Pages which custom domain to serve
.nojekyll     tells GitHub Pages to skip Jekyll processing
```

Everything — layout, the tracker pages, search/filter, the EN/SW toggle, the contact form — lives in `index.html`. There's no build step: what you push is what gets served.

## 1. Push this to GitHub

If you don't have a repo yet:

1. Create a new repository on GitHub (e.g. `hatujasahau`). Public or private both work with GitHub Pages, but public is required on the free tier for Pages to be free.
2. From this folder, run:
   ```
   git init
   git add .
   git commit -m "Initial site"
   git branch -M main
   git remote add origin https://github.com/YOUR-USERNAME/hatujasahau.git
   git push -u origin main
   ```
   (Or use GitHub Desktop if you'd rather not use the command line — drag this folder in, commit, push.)

## 2. Turn on GitHub Pages

1. In the repo: **Settings → Pages**.
2. Under "Build and deployment," set **Source** to `Deploy from a branch`.
3. Set **Branch** to `main`, folder `/ (root)`.
4. Save. GitHub will give you a URL like `https://YOUR-USERNAME.github.io/hatujasahau` within a minute or two — check that it loads before moving on to the domain.

## 3. Point hatujasahau.org at GitHub Pages

You already own the domain. In your domain registrar's DNS settings, add:

**For the root domain (`hatujasahau.org`)** — four A records, all pointing to GitHub's IPs:
```
A    @    185.199.108.153
A    @    185.199.109.153
A    @    185.199.110.153
A    @    185.199.111.153
```

**For `www.hatujasahau.org`** (optional but recommended) — one CNAME record:
```
CNAME    www    YOUR-USERNAME.github.io
```

DNS changes can take anywhere from a few minutes to 24 hours to propagate.

## 4. Confirm the custom domain in GitHub

1. Back in **Settings → Pages**, under "Custom domain," enter `hatujasahau.org` and save. This is also what writes the `CNAME` file in your repo (it's already included here, so this should just confirm it).
2. Wait for the DNS check to pass (GitHub shows a green checkmark once it can see your A records).
3. Tick **Enforce HTTPS** once it becomes available — it won't be checkable until DNS has fully propagated and GitHub has issued a certificate, which can take a few hours.

## 5. You're live

Once HTTPS is enforced, `https://hatujasahau.org` should serve the site directly.

## Making changes going forward

Every push to `main` redeploys automatically — usually live within a minute or two. There's no separate "publish" step:

```
git add .
git commit -m "describe your change"
git push
```

## Known limitations to plan for next

- **The contact form doesn't send anywhere yet.** GitHub Pages is static-only and can't process form submissions. Before relying on it, wire the form's `action` to a service like [Formspree](https://formspree.io) (free tier, ~5 minute setup) — or switch hosting to Netlify, which has forms built in.
- **All content is hardcoded placeholder data** inside `index.html`. Before publishing real cases, replace the sample entries in the Killings, Corruption, In 6 months, and News sections with verified, sourced reporting.
- **No calculated stats yet.** The numbers in the stat cards (148 cases, 37 promises, etc.) are typed in by hand, not computed from data. See the project notes on moving to a data-file + build-script approach when you're ready for that.

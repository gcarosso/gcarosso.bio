# gcarosso.bio — scaffold

A framework to write into. Every piece of copy is a bracketed placeholder; none of
the text is meant to ship. Plain HTML and one stylesheet — no framework, no build
step, no dependencies, nothing to install.

---

## Preview it

**Double-click `preview.command`.** It serves the folder and opens your browser at
`http://localhost:8000`. Close the Terminal window to stop.

Edit any file, save, refresh the browser. That's the whole loop.

*(First time, macOS may block it: right-click → Open → Open. Or run
`python3 -m http.server` in this folder from Terminal.)*

You can also just double-click `index.html` to open it directly — everything works
except links ending in `/`, which need the server.

---

## Draft mode

Every page has `<body class="draft">`. That turns on:

- a yellow bar across the top
- dashed outlines and a **DRAFT** chip on every placeholder
- yellow `.todo` boxes explaining how each section works

**To see a page as it will actually ship**, delete `class="draft"` from that page's
`<body>` tag. Put it back to keep working. The `.todo` boxes disappear entirely when
draft mode is off, so you can leave them in place until you're done.

When you're finished with a page: replace the placeholder text, remove the `ph`
class from those elements, delete the `.todo` blocks, and drop the `draft` class.

---

## Files

```
site/                     the public repository = exactly what is served at gcarosso.bio
  index.html              home — lede, bio paragraph, slideshow, section cards, contacts
  about.html              About
  cv.html                 CV — generated from the 2026 CV in ../site-sources/cv/ (phone number omitted)
  notes/                  Notes — index.html, _template.html (copy to start a piece), example-post.html (layout demo)
  tools/index.html        Tools — one .item row per tool, Open + Source links (SAROS first)
  travels/index.html      Travels — photo grids; web-sized images go in travels/img/<trip>/
  library/index.html      Library — the bookshelf with hover cards, and other media
  assets/img/             site-wide images: home slideshow frames, SAROS mark, placeholders
  assets/plots/           custom plots (SVG preferred)
  style.css               the entire design system
  preview.command         local preview server
  dashboard-trials/       the SAROS working repo — its own git repo, ignored by this one

../site-sources/          NOT in the repo: raw material, one folder per page
  home/photos/            slideshow originals
  travels/<trip>/         camera originals and video, by trip — resize before anything goes in the repo
  notes/drafts/           essay drafts and the old-site archive
  learning/               notes toward the reading list
  about/, tools/          material for those pages
```

---

## How to do the common things

**Write a new essay**
1. Copy `notes/_template.html` → `notes/your-slug.html`
2. Edit the four tagged lines in `<head>` (title, description, og:title, og:description)
3. Write the body
4. Add an `.entry` row to `notes/index.html`, and optionally to Recent on the homepage

**Add an image**
```html
<figure>
  <img src="../assets/img/your-image.jpg" alt="Describe it for screen readers.">
  <figcaption><b>Figure 1.</b> What the reader should take from it.</figcaption>
</figure>
```
Add `class="figure-wide"` to break out past the text column on desktop — good for
plots and anything with fine detail.

**Add a plot.** Export as **SVG** if your tool allows: it stays sharp at any zoom,
is usually smaller than PNG, and the text in it is selectable and searchable.
matplotlib: `plt.savefig("plot.svg")`. Put it in `assets/plots/`.

**Resize photos before adding them.** Camera files will make the page unusable on
mobile data. From Terminal, in a folder of images:
```bash
sips -Z 1600 *.jpg            # macOS built-in: long edge to 1600px
```
Aim for roughly 300 KB per photo.

**Change the design.** Everything is in `style.css`. The variables at the top drive
the whole site:
```css
--ink:   #000;    /* body text        */
--mute:  #6b6b6b; /* secondary text   */
--rule:  #dcdcdc; /* hairlines        */
--max:   680px;   /* text measure     */
--wide:  1040px;  /* galleries, plots */
```
Dark mode is automatic via `prefers-color-scheme` and needs no toggle.

**The nav is repeated in every page.** That's the cost of having no build step. If
you add a section, update the `<nav>` block in each file — there are nine. Mark the
current page with `aria-current="page"` so it highlights. Order: Home · About · Tools · Notes · Travels · Library · CV.

---

## Notes on the design

- **680px measure**, roughly 70 characters per line, which is where reading speed
  peaks. Wider looks more impressive and reads worse.
- **Same system as your CV and resume** — Helvetica Neue, black, hairline rules,
  en-dash bullets. Consistency across the three is itself a signal.
- **No JavaScript, no web fonts, no analytics.** Pages are a few KB and render
  instantly. This matters more than it sounds when someone opens your link between
  meetings on hotel wifi.

---

## When you're ready to go live

- [ ] Register `gcarosso.bio` (Cloudflare Registrar) and attach it to the Pages project
- [ ] Replace every `[bracketed placeholder]`
- [ ] Remove all `class="draft"` and every `.todo` block
- [ ] Check every factual claim against your own records
- [ ] Real `<title>` and `<meta name="description">` on every page
- [ ] Deploy: the repo is connected to Cloudflare Pages (framework "None", no build command,
      output directory `/`); every `git push` redeploys within about a minute. 
- [ ] Point LinkedIn, ORCID, and Google Scholar at the new domain
- [ ] Add the site to Google Search Console so it indexes promptly

---

## Earlier drafts

The three essays written in an earlier pass are parked in `../site-drafts/` — not
part of the site, not linked from anywhere. Raid them for arguments or ignore them.

---

## Git, in four commands

```bash
git status            # what changed
git add -A            # stage everything
git commit -m "…"     # save a point in history, with a note
git push              # send it to GitHub, which redeploys the site
```

Never commit camera originals, video, `.DS_Store`, or anything from `dashboard-trials/` (it has its own repository). This repository holds only what is published at gcarosso.bio.

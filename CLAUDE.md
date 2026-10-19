# gabrieldevoto.com: instructions for Claude

This folder is the source of Gabriel Devoto's academic website, **https://gabrieldevoto.com**. It is a one-page [Quarto](https://quarto.org) site hosted on GitHub Pages. Gabriel is an economist, not a web developer: explain steps in plain language, do the technical work yourself, and show him the result before anything goes public.

## Ground rules (from Gabriel)

1. **Ask before anything public or hard to undo**: `git push`, `quarto publish`, changing GitHub settings, deleting files. Commit locally freely; push and publish only after he says yes.
2. **Never invent content.** Use only text, links, and facts he gives you. If something is missing (an abstract, a coauthor, a link), ask.
3. **Everything stays under his name.** Commits are authored by `Gabriel Devoto <344975427+gabrieldevoto-1994@users.noreply.github.com>` (his choice: private GitHub address). Do **not** add a `Co-Authored-By: Claude` line or any other attribution. Only ever use the GitHub account **gabrieldevoto-1994**. If `gh` is logged into another account, stop and tell him.
4. **Don't touch DNS or GoDaddy.** If a DNS change is ever needed, give him step-by-step instructions instead.
5. After a change is published, verify it live and report plainly.

`../WEBSITE_BUILD.md` (one folder up, if present) is the **original** build brief. It is historical: the site has since changed (one page instead of three, dark mode, etc.). This file describes the current state and takes precedence.

## Files

| File | Controls |
|---|---|
| `index.qmd` | **All page content**: name, title line under the name, bio, buttons, paper list, link-preview text |
| `_quarto.yml` | Site settings: domain, favicon, navbar, footer disclaimer, theme, which files get published |
| `custom.scss` | Fonts, layout, spacing, **light-mode colors** (variables at the top) |
| `dark.scss` | **Dark-mode colors** (overrides the same variables) |
| `email-tooltip.html` | Small script: shows the email address on hover over the Email button |
| `files/Devoto_CV.pdf` | The CV (button under the name links here) |
| `files/photo.jpg` | Portrait, 800×800 square, shown in a circle |
| `files/favicon.png` | Browser-tab icon: navy square, white serif "GD" |
| `files/share-card.png` | 1200×630 image shown when the link is shared (LinkedIn, Slack…); rebuild with `python tools/make_share_card.py` |
| `CNAME` | Contains `gabrieldevoto.com`. **Must stay**, and must stay listed under `project: resources`, or the domain disconnects on the next publish |
| `tools/check_site.py` | Pre-publish check: screenshots, phone overflow, links (see workflow) |
| `tools/make_share_card.py` | Rebuilds `files/share-card.png` |
| `README.md` | Short human-readable version of these instructions |
| `_site/` | Build output (git-ignored). Never edit by hand |

### Page layout (`index.qmd`)

- Front matter `about:` uses Quarto's **trestles** template with `id: about`: left column = round photo, name (`title`), title line (`subtitle`), link buttons (`about: links:`); right column = the `::: {#about}` block (bio, one sentence per paragraph).
- Below it, `## Working Papers {#research}` and one `###` block per paper (see recipes).
- `description`, `open-graph`, `twitter-card` in the front matter feed search engines and link previews only; the description is hidden on the page by CSS.
- The navbar shows only the name (left) and the "Dark mode" switch (right). Gabriel removed the Research/CV navbar links on purpose because both are on the page.

## Tools and setup

Windows 10, VS Code. Needed: **Quarto** (`C:\Program Files\Quarto\bin`), **GitHub CLI** (`C:\Program Files\GitHub CLI`), git, Python 3 with **Pillow** (share card) and **Playwright** (site check), and Google Chrome.

- In the Bash tool, these may not be on PATH. Start commands with:
  `export PATH="/c/Program Files/Quarto/bin:/c/Program Files/GitHub CLI:$PATH"`
- Check before the first edit of a session: `quarto --version`, `gh --version`, `python -c "import PIL, playwright"`.
- Missing tools: `winget install --id Posit.Quarto -e --source winget` / `winget install --id GitHub.cli -e --source winget` (the `--source winget` flag matters; the msstore source fails here). Python packages: `pip install pillow playwright`. Playwright uses the installed Chrome; without Chrome, run `python -m playwright install chromium` and pass `--bundled` to the check script.
- Check the GitHub login: `gh auth status` must show **gabrieldevoto-1994**, and `gh api user --jq .login` must print `gabrieldevoto-1994`. If not logged in, Gabriel runs `gh auth login` himself (GitHub.com → HTTPS → Yes → browser), then run `gh auth setup-git`.
- Check the commit identity before committing: `git config user.name` = `Gabriel Devoto`, `git config user.email` = `344975427+gabrieldevoto-1994@users.noreply.github.com`. On a fresh clone, set them with `git config` (repo-local, not `--global`).
- **Working on a different computer:** `gh repo clone gabrieldevoto-1994/gabrieldevoto-1994.github.io gabrieldevoto`, then set the identity as above.

## Workflow for any change

0. **Start clean:** `git status`. If there are uncommitted changes you didn't make, ask Gabriel about them before doing anything else; don't sweep them into your commit.
1. **Edit** the files (recipes below).
2. **Render:** `quarto render 2>&1 | grep -iE "warn|error"`. No output means no warnings (the full log is a long settings dump; don't eyeball it).
3. **Check:** `python tools/check_site.py`. It serves `_site/` on a free port by itself, screenshots light and dark mode at 1280px and 375px (saved in `%TEMP%\gabrieldevoto-check\`, never in the project), **fails if anything scrolls sideways or runs off the phone screen**, and checks every link. Exit code 0 = good. Look at the screenshots yourself as well, especially the 375px ones. Don't trust plain `chrome --headless --screenshot` images (they clamp mobile width), and don't judge overflow from screenshots alone: phone emulation zooms out to fit wide content, which is why the script measures `scrollWidth`.
   - **A link fails** (anything but 200): don't publish it. Tell Gabriel which link and ask for a working one. Google Drive papers need "Anyone with the link" sharing. LinkedIn always shows `??` (it blocks bots); that's fine.
4. **Show Gabriel** a live preview. Do NOT use `quarto preview` on this machine: it crashes (`BadResource: Bad resource ID` in its Sass cache) whenever a `.scss` file changes, and it empties `_site/`. Instead run `python -m http.server 4321 --bind 127.0.0.1 --directory _site` as a **background task** (any free port works if 4321 is busy), then `start "" "http://localhost:4321/"`. After further edits: `quarto render`, and tell him to refresh. Iterate until he approves.
5. **Stop the preview server** before rendering for publish, because it locks `_site/` ("being used by another process"). In Claude Code, stop the background task. If it was started elsewhere, PowerShell: `Get-NetTCPConnection -LocalPort 4321 -State Listen | ForEach-Object { Stop-Process -Id $_.OwningProcess }`.
6. **Commit locally:** `git status`, then `git add <the files you changed>`, then `git commit -m "Short description"` (no attribution trailer). Avoid `git add -A` unless `git status` shows only your changes.
7. **Ask**, then publish:
   - `git push origin master`
   - `quarto publish gh-pages --no-prompt --no-browser`
8. **Verify live** after about 1–3 minutes: `python tools/check_site.py --live` passes, the change appears on https://gabrieldevoto.com, `curl -s -o /dev/null -w "%{http_code} %{redirect_url}" https://www.gabrieldevoto.com/` gives 301 to the bare domain, and `gh api "repos/gabrieldevoto-1994/gabrieldevoto-1994.github.io/contents/CNAME?ref=gh-pages" --jq .content | base64 -d` prints `gabrieldevoto.com`. Tell Gabriel that a stale browser copy goes away with Ctrl+F5.

## Recipes

### Add a working paper
Copy a block in `index.qmd` and place it where it belongs in the list (newest/most important first):

```markdown
### [Exact Paper Title](https://link-to-pdf)

<details><summary>Abstract</summary>

Abstract text, verbatim from Gabriel.

</details>
```

Coauthors, if he gives them, go on their own line directly under the `###` line, as plain text: `with Name Surname and Name Surname`. If he wants this, add a small muted style in `custom.scss` (e.g. a `.coauthors` class, font-size ~0.92rem, color `$gd-muted`) rather than bolding or italicizing ad hoc.

Paper PDFs usually live on Gabriel's Google Drive ("Anyone with the link" share URL); journal, SSRN, NBER, or IMF Working Paper pages are fine too. `tools/check_site.py` verifies every link; if one fails, ask him for a working link instead of publishing it.

On phones a long title wraps and the "New draft" tag may sit on its own line under it. That's expected.

### Remove a paper
Delete its whole block, from the `###` line through `</details>`.

### Move or remove the "New draft" tag
It is `<span class="tag">New draft</span>` at the end of a title line (same line, after the link). Cut and paste it to another paper's title line, or delete it. Other labels work the same way (e.g. `<span class="tag">R&R at Journal</span>`), using only wording Gabriel provides.

### Add a new section (e.g. "Work in Progress", "Publications", "Teaching")
Add after the papers in `index.qmd`:

```markdown
## Work in Progress {#work-in-progress}

### Title of project

### [Title of project with a draft](https://link)

with Name Surname
```

- Link the title only if Gabriel gives a link; unlinked titles look the same (navy, bold).
- Coauthors and one-line descriptions go as plain text on the line under the `###`, only if he provides them. An abstract can be added with the same `<details>` block as papers.
- `##` headings automatically get the small uppercase, letter-spaced style and spacing (`section.level2` in `custom.scss`).
- Published papers: same `###` + `<details>` pattern, plus a plain line under the title with the journal and year, e.g. `*Journal of Monetary Economics*, 2027`.

### Change the bio or the title line
- Bio: the `::: {#about}` block. Keep one sentence (or short idea) per paragraph, separated by blank lines.
- Title line under the name: `subtitle:` in the front matter, currently "Economist, International Monetary Fund". On desktop it never wraps (the left column widens to fit; a much longer line squeezes the bio column, so keep it short). On phones it fits on one line with only a few pixels to spare; anything longer wraps into two balanced lines (`text-wrap: balance` in the mobile media query), which is fine. If Gabriel wants it on one line on phones, he'll need a shorter wording, so ask him rather than shrinking the font.
- **The same facts appear in 4 places.** Whenever his job title, employer, or research fields change, update all of them together: the bio, `subtitle`, the three `description` fields in the front matter (`description`, `open-graph`, `twitter-card`; used by Google and link previews), and the text lines in `tools/make_share_card.py` (then run it). Small wording tweaks to the bio alone don't need the others.

### Buttons under the name (CV, Email, LinkedIn)
Edit `about: links:` in `index.qmd`. Each has `icon` ([Bootstrap Icons](https://icons.getbootstrap.com/) name), `text`, `href`. Examples: Google Scholar → icon `mortarboard`, GitHub → icon `github`, IMF profile → icon `bank`. Gabriel wanted no Twitter/X.

Three buttons fit on one row on a phone. A 4th (or more) automatically wraps to a centered second row (tested; it looks fine). Mention this to Gabriel when adding one, so the second row isn't a surprise. Keep labels short ("Google Scholar", not "My Google Scholar profile").

The Email button is `mailto:gdevoto@imf.org` (his work email, which he wants public). On a computer without a default mail app, clicking it does nothing; that's normal, and hovering shows the address.

### Replace the CV
Overwrite `files/Devoto_CV.pdf` (same exact name), render, publish. Gabriel may hand you a file with a different name (e.g. `Gabriel Devoto CV.pdf`): copy it to that path.

### Change the photo
Crop to a square around head and shoulders (the face in the upper-middle; leave some shoulders so the circle doesn't cut the chin), resize to 800×800, save as `files/photo.jpg` (JPEG quality ~85). Then run `python tools/make_share_card.py` to rebuild the link-preview card. The originals are high-resolution headshots in the parent `WEBSITE` folder (`100424_UM_Econ_Headshots_59.jpg` = green leafy background, `_62.jpg` = warm tree/brick background, currently used).

### Footer disclaimer
`page-footer: center:` in `_quarto.yml`. It is the IMF disclaimer; don't remove it without Gabriel asking.

### Colors and fonts
- Light mode: the color variables at the top of `custom.scss` (`$primary: #19325F` is the navy from his CV; `$gd-*` variables are custom). Dark mode: the same variable names in `dark.scss` (near-black `#0c0e13` background, light navy `#a9bfe6` accents). **Every color used in the rules must be a variable**, so dark mode stays consistent: add new variables in both files.
- Font: Source Serif 4 (Google Fonts import at the top of `custom.scss`).
- Design intent: calm, typographic, lots of white space, like top economics job-market pages. No animations, stock images, banners, or decorative icons.

### Add a navbar link back
In `_quarto.yml` replace `navbar: true` with:
```yaml
  navbar:
    toggle-position: right
    right:
      - text: CV
        href: files/Devoto_CV.pdf
```
(The CSS already handles the "Dark" label and menu button on phones.)

### Add a separate page
Create e.g. `teaching.qmd`, **add it to `project: render:`** in `_quarto.yml` (only listed files are built, which keeps `README.md` / `CLAUDE.md` off the website), and add a navbar link to it as above.

## Hosting reference (don't change unless Gabriel asks)

- Repo: https://github.com/gabrieldevoto-1994/gabrieldevoto-1994.github.io. `master` = source, `gh-pages` = built site (written by `quarto publish`). GitHub Pages serves `gh-pages` with custom domain `gabrieldevoto.com` and **Enforce HTTPS** on.
- Domain registrar and DNS: **GoDaddy**. Records: 4 × A `@` → `185.199.108.153`, `.109.153`, `.110.153`, `.111.153`; 4 × AAAA `@` → `2606:50c0:8000::153` … `8003::153`; CNAME `www` → `gabrieldevoto-1994.github.io`; TXT `_github-pages-challenge-gabrieldevoto-1994` (domain verification, keep forever); TXT `google-site-verification=…` (keep). No email (MX) on the domain.
- This network blocks outside DNS resolvers (8.8.8.8, DNS-over-HTTPS). To inspect DNS, query GoDaddy directly: PowerShell `Resolve-DnsName gabrieldevoto.com -Type A -Server ns63.domaincontrol.com`.
- Harmless quirks: git's "LF will be replaced by CRLF" warnings; the CV button's link renders as `/files/Devoto_CV.pdf` (root-absolute, from the about template), which works online and on the local server but not when opening `index.html` straight from disk.

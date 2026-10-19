# gabrieldevoto.com

Source for my academic website, built with [Quarto](https://quarto.org) and hosted on GitHub Pages.

Everything is on one page, `index.qmd`. Run all commands below in Git Bash from this folder.

## Preview and publish

```bash
quarto preview                 # opens a live preview in the browser
quarto publish gh-pages        # puts the site online (takes ~1 minute)
```

Also save the source to GitHub after each change:

```bash
git add . && git commit -m "Describe the change" && git push
```

If `quarto preview` crashes after you edit a `.scss` file (a known Windows issue), stop it with Ctrl+C and start it again.

## Replace the CV

Overwrite `files/Devoto_CV.pdf` with the new file (keep that exact name), then publish.

## Add a new paper

In `index.qmd`, copy one paper block (from `### [` through `</details>`), paste it where it should appear in the list, and change the title, link, and abstract:

```markdown
### [TITLE](PDF_LINK)

<details><summary>Abstract</summary>

ABSTRACT TEXT

</details>
```

## Move the "New draft" tag

Cut `<span class="tag">New draft</span>` from the end of one paper's title line and paste it at the end of another's (same line, after the link). Delete it to remove the tag.

## Change the photo

Replace `files/photo.jpg` with a square image (about 800 × 800 px), then rebuild the link-preview image so shared links show the new photo:

```bash
python tools/make_share_card.py
```

## Where things are

| File | What it controls |
|---|---|
| `index.qmd` | All page text: name, title line, bio, buttons, papers |
| `_quarto.yml` | Site settings: navbar, footer disclaimer, theme |
| `custom.scss` | Fonts, layout, light-mode colors |
| `dark.scss` | Dark-mode colors |
| `files/` | CV, photo, favicon, link-preview image |

# gabrieldevoto.com

Source for my academic website, built with [Quarto](https://quarto.org) and hosted on GitHub Pages.

## The easy way: ask Claude

Open this folder in VS Code with Claude Code and describe the change ("add this paper", "replace my CV", "remove the New draft tag"). `CLAUDE.md` gives Claude everything it needs: how the site works, my rules, and recipes. Claude will show me a preview and ask before publishing.

## Doing it by hand

Everything is on one page, `index.qmd`. Run the commands below in Git Bash from this folder.

### Preview and publish

```bash
quarto render                                                    # build the site into _site/
python -m http.server 4321 --bind 127.0.0.1 --directory _site    # preview at http://localhost:4321/ (Ctrl+C to stop)
```

Optional automatic check (phone layout, dark mode, all links): `python tools/check_site.py`

When it looks right, stop the preview server, then save and publish:

```bash
git add -A && git commit -m "Describe the change" && git push
quarto publish gh-pages
```

The live site updates within a few minutes. Press Ctrl+F5 if your browser shows the old version.

(`quarto preview` crashes on this computer after style edits, so use the two commands above instead.)

### Replace the CV

Overwrite `files/Devoto_CV.pdf` with the new file (keep that exact name), then publish.

### Add a new paper

In `index.qmd`, copy one paper block (from `### [` through `</details>`), paste it where it should appear in the list, and change the title, link, and abstract:

```markdown
### [TITLE](PDF_LINK)

<details><summary>Abstract</summary>

ABSTRACT TEXT

</details>
```

### Move the "New draft" tag

Cut `<span class="tag">New draft</span>` from the end of one paper's title line and paste it at the end of another's (same line, after the link). Delete it to remove the tag.

### Change the photo

Replace `files/photo.jpg` with a square image (about 800 × 800 px), then rebuild the link-preview image so shared links show the new photo:

```bash
python tools/make_share_card.py
```

## Where things are

| File | What it controls |
|---|---|
| `index.qmd` | All page text: name, title line, bio, buttons, papers |
| `_quarto.yml` | Site settings: domain, footer disclaimer, theme |
| `custom.scss` | Fonts, layout, light-mode colors |
| `dark.scss` | Dark-mode colors |
| `files/` | CV, photo, favicon, link-preview image |
| `CNAME` | The domain name. Don't delete |
| `CLAUDE.md` | Instructions for Claude Code |

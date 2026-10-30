# sideprojects

A collection of small side projects, served with GitHub Pages. The root `index.html` shows a list of all projects.

## Layout
- `index.html`: landing page that lists the projects.
- `projects.json`: the list of projects shown on the landing page.
- One folder per project, e.g. `klotski-state-space/` (contains the page and a `PROJECT.md` handoff document).

## Adding a project
1. Create a folder for it with its HTML page (and a `PROJECT.md` if you want to continue it in a new chat).
2. Add an entry to `projects.json`:
   ```json
   { "name": "My Project", "description": "One sentence.", "path": "my-project/page.html", "tags": ["tag"] }
   ```
3. Commit and push; GitHub Pages picks it up.

## Hosting
Repo Settings → Pages → deploy from branch `main`, folder `/ (root)`.

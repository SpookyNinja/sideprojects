# Instructions for AI assistants

This repo holds many small side projects, hosted with GitHub Pages. Read this file before adding or changing anything.

## Repo conventions
- **One folder per project** (kebab-case, e.g. `klotski-state-space/`). All of a project's files live in that folder.
- **The root `index.html` is the landing page** and must stay at the repo root. Give a project's own page a descriptive name (e.g. `klotski.html`) rather than `index.html`, so it is never confused with the landing page.
- **Every project folder contains a `PROJECT.md`**: a handoff document so a new chat can pick up the work without any other context. Use `PROJECT_TEMPLATE.md` as the starting point.
- **Every project is registered in `projects.json`** at the repo root (the landing page reads it). Do not hard-code projects in the root `index.html`.
- **Every project page has a "Home" button fixed at the bottom right** linking back to the landing page (`../index.html` for pages one folder deep). Copy it from `klotski-state-space/klotski.html` (`#home`).
- Projects should be static (plain HTML/CSS/JS, optional CDN libraries) so they work on GitHub Pages without a build step. Use exact library versions in CDN URLs.

## When you are given a new project to upload
1. Create `<project-folder>/` and put every file of the project there.
2. Write `<project-folder>/PROJECT.md` from `PROJECT_TEMPLATE.md`. Fill it with everything a future session needs: what the project is, the user's original brief and later requests, what is implemented, what is not done or untested, known issues, planned ideas, a code map, and development notes. Be concrete; do not leave template placeholders.
3. Add an entry to `projects.json`:
   ```json
   { "name": "Project Name", "description": "One sentence.", "path": "project-folder/page.html", "tags": ["tag"] }
   ```
4. Check that the `path` in `projects.json` points to an existing file.
5. Commit and push (only if the user asked for it).

## When you are asked to continue an existing project
1. Read `<project-folder>/PROJECT.md` first, then the code.
2. After making changes, **update `PROJECT.md`**: move finished items out of "not done / planned", add new features, new known issues, and any decisions the user made (and why).
3. Keep the code map accurate if you add, move or rename major functions or files.

## Style notes
- Match the existing code style of the project you are editing.
- Don't commit large binaries or build output.
- Keep `README.md` (repo overview) and `projects.json` consistent with what is actually in the repo.

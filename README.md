# stash-plugins

Plugin source for [Stash](https://github.com/stashapp/stash). In Stash: Settings → Plugins →
Available Plugins → Add Source, with the URL

```
https://max-dev42.github.io/stash-plugins/index.yml
```

## Plugins

| Plugin | Repository |
|---|---|
| Performer Network | [max-dev42/stash-performer-network](https://github.com/max-dev42/stash-performer-network) |

## How it works

Each plugin lives in its own repository, included here as a git submodule under `plugins/`.
`build_site.py` zips each plugin (the folder holding its manifest `<id>.yml`, either `plugin/` or the
repository root) and writes `index.yml`; the version is the manifest version plus the plugin
repository's commit, the date that commit's date. The `deploy` workflow publishes the result to
GitHub Pages on every push to `main`. Dependabot moves the submodules forward weekly.

Build locally:

```sh
git submodule update --init
pip install pyyaml
TZ=UTC0 python3 build_site.py _site
```

## License

MIT

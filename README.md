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

## Beta source

Pre-releases of the same plugins, for testing before a release:

```
https://max-dev42.github.io/stash-plugins/beta/index.yml
```

The plugins keep their IDs, so use one source at a time: replace the source above with this one
(Settings → Plugins → Available Plugins), and Stash offers the beta versions as updates. To go back,
switch to the stable source again and install the plugin from there.

The beta source is built from the `beta` branch of this repository, whose submodules point at the
`beta` branches of the plugin repositories (tags `vX.Y.Z-beta.N`, published as GitHub pre-releases).
Betas are announced in each plugin's thread.

## How it works

Each plugin lives in its own repository, included here as a git submodule under `plugins/`.
`build_site.py` zips each plugin (the folder holding its manifest `<id>.yml`, either `plugin/` or the
repository root) and writes `index.yml`; the version is the manifest version plus the plugin
repository's commit, the date that commit's date. The `deploy` workflow publishes the result to
GitHub Pages on every push to `main` or `beta`: the stable source from `main` at the root, the beta
source from `beta` under `beta/`. Dependabot moves the submodules of `main` forward weekly.

Build locally:

```sh
git submodule update --init
pip install pyyaml
TZ=UTC0 python3 build_site.py _site
```

The beta source from the `beta` branch, next to it:

```sh
git worktree add --detach ../stash-plugins-beta origin/beta
git -C ../stash-plugins-beta submodule update --init
(cd ../stash-plugins-beta && TZ=UTC0 python3 build_site.py "$OLDPWD/_site/beta")
```

## License

MIT

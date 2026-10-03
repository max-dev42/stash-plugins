#!/usr/bin/env python3
"""Build a Stash plugin source from the plugin submodules in plugins/.

Writes <outdir>/index.yml and one <plugin_id>.zip per plugin. A plugin is the
directory that holds its manifest <plugin_id>.yml: either the submodule root
or its plugin/ subdirectory (repos that also carry tests and a demo).

Modelled on build_site.sh from stashapp/CommunityScripts; differences:
the manifest is parsed as YAML (folded descriptions), the version and date
come from the submodule's own last commit, and the zip is reproducible.
"""
import hashlib
import subprocess
import sys
import zipfile
from pathlib import Path

import yaml

FIXED_TIME = (1980, 1, 1, 0, 0, 0)  # constant zip timestamps -> stable sha256


def git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args], check=True,
                          capture_output=True, text=True).stdout.strip()


def find_manifest(repo):
    for base in (repo / "plugin", repo):
        hits = [p for p in base.glob("*.yml") if yaml.safe_load(p.read_text()).get("name")]
        if len(hits) == 1:
            return hits[0]
    sys.exit(f"{repo}: expected exactly one plugin manifest in plugin/ or the repo root")


def build_zip(src, target):
    files = sorted(p for p in src.rglob("*") if p.is_file())
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as z:
        for f in files:
            info = zipfile.ZipInfo(f.relative_to(src).as_posix(), FIXED_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            z.writestr(info, f.read_bytes())


def main():
    out = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
    out.mkdir(parents=True, exist_ok=True)
    index = []
    for repo in sorted(p for p in Path("plugins").iterdir() if p.is_dir() and (p / ".git").exists()):
        manifest = find_manifest(repo)
        meta = yaml.safe_load(manifest.read_text())
        plugin_id = manifest.stem
        commit = git(repo, "log", "-1", "--format=%h")
        date = git(repo, "log", "-1", "--date=format-local:%Y-%m-%d %H:%M:%S", "--format=%ad")
        zip_path = out / f"{plugin_id}.zip"
        build_zip(manifest.parent, zip_path)
        entry = {
            "id": plugin_id,
            "name": meta["name"],
            "metadata": {"description": " ".join(str(meta.get("description", "")).split())},
            "version": f"{meta.get('version', '0')}-{commit}",
            "date": date,
            "path": zip_path.name,
            "sha256": hashlib.sha256(zip_path.read_bytes()).hexdigest(),
        }
        if meta.get("requires"):
            entry["requires"] = meta["requires"]
        index.append(entry)
        print(f"{plugin_id} {entry['version']}")
    (out / "index.yml").write_text(yaml.safe_dump(index, sort_keys=False, allow_unicode=True))


if __name__ == "__main__":
    main()

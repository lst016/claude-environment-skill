#!/usr/bin/env python3
"""Install this complete local Skill; back up an existing copy before replacement."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
import tempfile

NAME = 'claude-environment-setup'


def install(source: Path, destination: Path) -> dict:
    source = source.resolve()
    if not (source / 'SKILL.md').is_file() or not (source / 'references/install.md').is_file():
        raise ValueError('Incomplete skill source')
    if any(p.is_symlink() for p in source.rglob('*')) or destination.is_symlink():
        raise ValueError('Symlinks are not supported')
    if destination.exists() and not destination.is_dir():
        raise ValueError('Destination must be a directory')
    destination.parent.mkdir(parents=True, exist_ok=True)
    # Stage on the destination filesystem for atomic rename. The running source
    # may itself be the installed destination, so copy before moving it away.
    staging_root = destination.parent.parent / 'skill-install-staging'
    staging_root.mkdir(parents=True, exist_ok=True)
    staged = Path(tempfile.mkdtemp(prefix='claude-skill-', dir=staging_root)) / NAME
    shutil.copytree(source, staged, ignore=shutil.ignore_patterns('__pycache__', '*.pyc', '.DS_Store'))
    backup = None
    if destination.exists():
        stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
        backup = destination.parent.parent / 'skill-backups' / NAME / stamp
        backup.parent.mkdir(parents=True, exist_ok=True)
        destination.rename(backup)
    try:
        staged.rename(destination)
    except Exception:
        if backup and not destination.exists():
            backup.rename(destination)
        raise
    return {'destination': str(destination), 'backup': str(backup) if backup else None}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--target', choices=['codex', 'claude', 'both'], required=True)
    args = parser.parse_args()
    source = Path(__file__).resolve().parents[1]
    names = ('codex', 'claude') if args.target == 'both' else (args.target,)
    # Default user directories; custom CODEX_HOME installations use manual copy.
    results = [install(source, Path.home() / ('.' + name) / 'skills' / NAME) for name in names]
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()

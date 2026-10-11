#!/usr/bin/env python3
"""Read-only checks; no credentials, config writes, or model requests."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess

OVERRIDES = {
    'ANTHROPIC_AUTH_TOKEN', 'ANTHROPIC_BASE_URL',
    'ANTHROPIC_DEFAULT_HAIKU_MODEL', 'ANTHROPIC_DEFAULT_SONNET_MODEL',
    'ANTHROPIC_DEFAULT_OPUS_MODEL', 'ANTHROPIC_MODEL',
    'ANTHROPIC_REASONING_MODEL',
}


def run(args: list[str]) -> subprocess.CompletedProcess[str] | None:
    try:
        return subprocess.run(args, capture_output=True, text=True, timeout=15, check=False)
    except (OSError, subprocess.TimeoutExpired):
        return None


def executable(name: str) -> str | None:
    if name == 'claude':
        native = Path.home() / '.local/bin/claude'
        if native.is_file() and os.access(native, os.X_OK):
            return str(native)
    return shutil.which(name)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--ports', type=int, nargs='+', default=[7897, 7898])
    parser.add_argument('--skip-auth', action='store_true', help='Skip local authentication status')
    args = parser.parse_args()
    if any(p < 1 or p > 65535 for p in args.ports):
        parser.error('ports must be between 1 and 65535')
    report: dict = {'system': platform.system(), 'checks_are_read_only': True, 'tools': {}}
    for name in ('claude', 'codex'):
        cmd = executable(name)
        result = run([cmd, '--version']) if cmd else None
        # Version responses should be short. Never emit arbitrary command errors.
        version = None
        if result and result.returncode == 0:
            import re
            found = re.search(r'\b\d+\.\d+\.\d+\b', result.stdout)
            version = found.group(0) if found else None
        report['tools'][name] = {'available': cmd is not None, 'version': version}
    claude = executable('claude')
    report['claude_prefers_native_install'] = bool(
        claude and Path(claude) == Path.home() / '.local/bin/claude'
    )
    path_claude = shutil.which('claude')
    report['path_points_to_different_claude'] = bool(
        claude and path_claude and Path(claude) != Path(path_claude)
    )
    settings = Path.home() / '.claude/settings.json'
    try:
        data = json.loads(settings.read_text()) if settings.exists() else {}
        if not isinstance(data, dict):
            raise ValueError('settings root must be an object')
        env = data.get('env', {})
        if not isinstance(env, dict):
            raise ValueError('settings env must be an object')
        report['settings'] = {'readable': True, 'provider_override_keys': sorted(OVERRIDES & env.keys())}
    except (OSError, ValueError, TypeError):
        report['settings'] = {'readable': False, 'provider_override_keys': []}
    report['process_provider_override_keys'] = sorted(k for k in OVERRIDES if os.environ.get(k))
    report['auth'] = {'checked': False}
    if claude and not args.skip_auth:
        result = run([claude, 'auth', 'status'])
        if result and result.returncode == 0:
            try:
                state = json.loads(result.stdout)
                if not isinstance(state, dict):
                    raise ValueError('auth result must be an object')
                report['auth'] = {
                    'checked': True,
                    'loggedIn': state.get('loggedIn') is True,
                    # Only known labels are allowed, not arbitrary provider values.
                    'official_subscription_auth': state.get('authMethod') == 'claude.ai',
                    'first_party': state.get('apiProvider') == 'firstParty',
                    'subscription_present': bool(state.get('subscriptionType')),
                }
            except (ValueError, TypeError):
                report['auth'] = {'checked': False, 'reason': 'unparseable_status'}
        else:
            report['auth'] = {'checked': False, 'reason': 'auth_or_keychain_unavailable'}
    lsof = shutil.which('lsof')
    report['ports'] = []
    for port in args.ports:
        result = run([lsof, '-nP', f'-iTCP:{port}', '-sTCP:LISTEN', '-F', 'c']) if lsof else None
        port_checked = bool(result is not None and result.returncode in (0, 1) and not result.stderr.strip())
        commands = [x[1:] for x in result.stdout.splitlines() if x.startswith('c')] if port_checked else []
        report['ports'].append({
            'port': port, 'checked': port_checked,
            'listening': bool(commands) if port_checked else None,
            'proxy_process_detected': any(
                any(label in cmd.lower() for label in ('clash', 'mihomo', 'efan')) for cmd in commands
            ),
        })
    report['scope_note'] = 'Empty results may reflect restricted process visibility; recheck with normal local permissions before changing networking.'
    report['not_verified'] = [
        'actual_proxy_exit', 'browser_account_or_fingerprint', 'iphone_routing',
        'model_request', 'payment_or_renewal', 'failure_blocking_or_reboot',
    ]
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()

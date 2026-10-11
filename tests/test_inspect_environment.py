"""Verify read-only reporting boundaries with synthetic local state."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

SOURCE = Path(__file__).resolve().parents[1] / 'skills/claude-environment-setup/scripts/inspect_environment.py'
spec = importlib.util.spec_from_file_location('inspect_environment', SOURCE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class InspectEnvironmentTests(unittest.TestCase):
    def report(self, runner, settings=None, argv=None):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            if settings is not None:
                p = home / '.claude/settings.json'
                p.parent.mkdir()
                p.write_text(json.dumps(settings))
            before = {str(p.relative_to(home)): p.read_bytes() for p in home.rglob('*') if p.is_file()}
            output = io.StringIO()
            with patch.object(mod.Path, 'home', return_value=home), \
                 patch.object(mod.shutil, 'which', side_effect=lambda name: '/fake/' + name), \
                 patch.object(mod, 'run', side_effect=runner), \
                 patch.object(mod.os, 'environ', {}), \
                 patch('sys.argv', argv or ['inspect_environment.py']), \
                 contextlib.redirect_stdout(output):
                mod.main()
            after = {str(p.relative_to(home)): p.read_bytes() for p in home.rglob('*') if p.is_file()}
            self.assertEqual(before, after, 'inspector must not mutate local files')
            return json.loads(output.getvalue()), output.getvalue()

    @staticmethod
    def success(args):
        if '--version' in args:
            return subprocess.CompletedProcess(args, 0, '2.1.296', '')
        if args[-2:] == ['auth', 'status']:
            state = {'loggedIn': True, 'authMethod': 'claude.ai', 'apiProvider': 'firstParty',
                     'subscriptionType': 'pro', 'email': 'PRIVATE_EMAIL', 'token': 'PRIVATE_TOKEN'}
            return subprocess.CompletedProcess(args, 0, json.dumps(state), '')
        return subprocess.CompletedProcess(args, 0, 'cmihomo\n', '')

    def test_private_values_filtered_and_state_unchanged(self):
        data, text = self.report(self.success, {'env': {'ANTHROPIC_AUTH_TOKEN': 'PRIVATE_CONFIG'}})
        self.assertTrue(data['auth']['loggedIn'])
        self.assertTrue(data['auth']['first_party'])
        self.assertEqual(data['settings']['provider_override_keys'], ['ANTHROPIC_AUTH_TOKEN'])
        for secret in ('PRIVATE_EMAIL', 'PRIVATE_TOKEN', 'PRIVATE_CONFIG'):
            self.assertNotIn(secret, text)

    def test_keychain_failure_is_unknown_not_logged_out(self):
        def runner(args):
            if args[-2:] == ['auth', 'status']:
                return subprocess.CompletedProcess(args, 1, 'PRIVATE_ERROR', 'PRIVATE_ERROR')
            return self.success(args)
        data, text = self.report(runner)
        self.assertFalse(data['auth']['checked'])
        self.assertNotIn('loggedIn', data['auth'])
        self.assertNotIn('PRIVATE_ERROR', text)

    def test_denied_port_check_is_unknown_not_closed(self):
        def runner(args):
            if '-F' in args:
                return subprocess.CompletedProcess(args, 2, '', 'PRIVATE_DENIAL')
            return self.success(args)
        data, text = self.report(runner)
        self.assertTrue(all(not p['checked'] and p['listening'] is None for p in data['ports']))
        self.assertNotIn('PRIVATE_DENIAL', text)

    def test_skip_auth_avoids_auth_command(self):
        calls = []
        def runner(args):
            calls.append(args)
            return self.success(args)
        data, _ = self.report(runner, argv=['inspect_environment.py', '--skip-auth', '--ports', '9999'])
        self.assertFalse(data['auth']['checked'])
        self.assertFalse(any('auth' in args for args in calls))
        self.assertEqual(data['ports'][0]['port'], 9999)

    def test_timeout_returns_no_raw_exception(self):
        with patch.object(mod.subprocess, 'run', side_effect=subprocess.TimeoutExpired('PRIVATE_COMMAND', 15)):
            self.assertIsNone(mod.run(['claude', '--version']))


if __name__ == '__main__':
    unittest.main()

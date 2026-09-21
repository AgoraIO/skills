"""Check the workflow's actual resolver against small suite fixtures."""
import contextlib
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import yaml

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = yaml.safe_load((ROOT / '.github/workflows/codex-eval.yml').read_text())
STEP = next(s for s in WORKFLOW['jobs']['evaluate']['steps'] if s.get('id') == 'resolve')
RESOLVER = STEP['run'].split("python3 - <<'PY'\n", 1)[1].rsplit('\nPY', 1)[0]


class CodexCaseSelectionTest(unittest.TestCase):
    def resolve(self, event, suites='workflow', case_id='', omit_rtc=False):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            cases_root = root / 'targets/agora/cases'
            cases_root.mkdir(parents=True)
            (cases_root.parent / 'target.yaml').write_text(yaml.safe_dump({'default_suites': ['workflow', 'rtc-contract']}))
            for suite, ids in {
                'workflow': ['convoai-e2e-first-success', 'unrelated-workflow'],
                'rtc-contract': ['rtc-web-quickstart-route', 'rtc-web-sdk-question', 'rtc-web-post-baseline', 'rtc-web-audio-only', 'rtc-web-readiness-evidence', 'rtc-native-ios-route'],
            }.items():
                if suite == 'rtc-contract' and omit_rtc:
                    continue
                suite_dir = cases_root / suite
                suite_dir.mkdir()
                paths = []
                for case in ids:
                    path = suite_dir / f'{case}.yaml'
                    path.write_text(yaml.safe_dump({'case_id': case, 'input': {'user_prompt': 'test'}}))
                    paths.append(str(path.relative_to(root)))
                (suite_dir / 'suite.yaml').write_text(yaml.safe_dump({'cases': paths}))
            original_open = open

            def redirect(path, *args, **kwargs):
                if str(path) == '/tmp/codex-eval-cases.json':
                    path = root / 'resolved.json'
                return original_open(path, *args, **kwargs)

            with contextlib.chdir(root), patch.dict(os.environ, {
                'TARGET_ID': 'agora', 'SUITE_IDS': suites, 'CASE_ID': case_id,
                'EVENT_NAME': event, 'GITHUB_OUTPUT': str(root / 'output'),
            }), patch('builtins.open', redirect):
                exec(compile(RESOLVER, 'codex-eval.yml:resolve', 'exec'), {})
            return [case['case_id'] for case in json.loads((root / 'resolved.json').read_text())]

    def test_pr_keeps_convoai_and_adds_exactly_six_rtc_cases(self):
        cases = self.resolve('pull_request')
        self.assertEqual(len(cases), 7)
        self.assertEqual(cases[0], 'convoai-e2e-first-success')
        self.assertTrue(all(case.startswith('rtc-') for case in cases[1:]))
        self.assertIn('rtc-native-ios-route', cases)

    def test_manual_single_case_and_empty_filter(self):
        self.assertEqual(self.resolve('workflow_dispatch', 'rtc-contract', 'rtc-web-audio-only'), ['rtc-web-audio-only'])
        self.assertEqual(len(self.resolve('workflow_dispatch', 'rtc-contract')), 6)
        self.assertEqual(self.resolve('workflow_dispatch', 'workflow', 'convoai-e2e-first-success'), ['convoai-e2e-first-success'])

    def test_manual_ios_case(self):
        self.assertEqual(self.resolve('workflow_dispatch', 'rtc-contract', 'rtc-native-ios-route'), ['rtc-native-ios-route'])

    def test_missing_suite_or_unmatched_case_does_not_silently_pass(self):
        with self.assertRaises(FileNotFoundError):
            self.resolve('pull_request', omit_rtc=True)
        with self.assertRaises(SystemExit):
            self.resolve('workflow_dispatch', 'rtc-contract', 'does-not-exist')


if __name__ == '__main__':
    unittest.main()

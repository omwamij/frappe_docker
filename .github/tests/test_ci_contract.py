"""Offline CI safety contracts; application suites still run in hosted CI."""
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
CONTRACTS={'.github/workflows/build_stable.yml': ['  v14:', '  v15:', '  v16:', "cancel-in-progress: ${{ github.event_name == 'pull_request' }}"], '.github/workflows/docker-build-push.yml': ['workflow_call:', 'timeout-minutes: 60']}
class CIContracts(unittest.TestCase):
 def test_distinct_gates_are_retained(self):
  for filename,requirements in CONTRACTS.items():
   text=(ROOT/filename).read_text(encoding='utf-8')
   for requirement in requirements:
    with self.subTest(file=filename,requirement=requirement):self.assertIn(requirement,text)
if __name__=='__main__':unittest.main()

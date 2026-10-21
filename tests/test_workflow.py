import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "daily-contribution.yml"


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.text = WORKFLOW.read_text(encoding="utf-8")

    def test_uses_the_published_action_and_the_account_email(self):
        self.assertIn("bcanseco/github-contribution-graph-action@v2", self.text)
        self.assertIn("GIT_EMAIL: zhuen1101@hotmail.com", self.text)
        self.assertIn('MIN_COMMITS_PER_DAY: "1"', self.text)
        self.assertIn('MAX_COMMITS_PER_DAY: "5"', self.text)
        self.assertNotIn("you@youremail.com", self.text)

    def test_runs_every_day_and_can_backfill_on_demand(self):
        self.assertIn('cron: "15 1 * * *"', self.text)
        self.assertIn("workflow_dispatch:", self.text)
        self.assertIn('default: "1"', self.text)
        self.assertIn("contents: write", self.text)
        self.assertIn("[skip ci]", self.text)

    def test_old_heartbeat_workflow_is_gone(self):
        self.assertFalse((ROOT / ".github" / "workflows" / "daily-heartbeat.yml").exists())
        self.assertFalse((ROOT / "scripts" / "heartbeat.py").exists())


if __name__ == "__main__":
    unittest.main()

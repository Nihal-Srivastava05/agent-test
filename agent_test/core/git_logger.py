"""
Git-aware logger for AgentTest.

Tracks test results with git commit information for regression analysis.
"""

import json
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    import git

    GIT_AVAILABLE = True
except ImportError:
    GIT_AVAILABLE = False

from ..utils.exceptions import GitError
from .config import Config
from .decorators import TestResults


class GitLogger:
    """Git-aware logger for test results."""

    def __init__(self, config: Config):
        self.config = config
        self.results_dir = Path(config.logging.results_dir)
        self.results_dir.mkdir(parents=True, exist_ok=True)

        # Initialize git repo if available
        self.repo = None
        if GIT_AVAILABLE and config.logging.git_aware:
            try:
                self.repo = git.Repo(search_parent_directories=True)
            except (git.InvalidGitRepositoryError, git.GitCommandError):
                print("Warning: Not in a git repository. Git-aware logging disabled.")

    def log_results(self, results: TestResults) -> None:
        """Log test results with git information."""
        timestamp = datetime.now().isoformat()

        # Get git information
        git_info = self._get_git_info()

        # Prepare log entry
        log_entry = {
            "timestamp": timestamp,
            "git_info": git_info,
            "summary": results.get_summary(),
            "test_results": [
                {
                    "test_name": result.test_name,
                    "passed": result.passed,
                    "score": result.score,
                    "duration": result.duration,
                    "error": result.error,
                    "evaluations": result.evaluations,
                }
                for result in results.test_results
            ],
            "metadata": results.metadata,
        }

        # Save to file
        self._save_log_entry(log_entry)

        # Update index
        self._update_index(log_entry)

    def _get_git_info(self) -> Dict[str, Any]:
        """Get current git information."""
        if not self.repo:
            return {"error": "Git not available"}

        try:
            # Get current commit
            commit = self.repo.head.commit

            # Get branch name
            try:
                branch = self.repo.active_branch.name
            except TypeError:
                # Detached HEAD
                branch = "detached"

            # Get status
            changed_files = [item.a_path for item in self.repo.index.diff(None)]
            untracked_files = self.repo.untracked_files

            # Get recent commits
            recent_commits = []
            for commit_obj in self.repo.iter_commits(max_count=5):
                recent_commits.append(
                    {
                        "hash": commit_obj.hexsha[:8],
                        "message": commit_obj.message.strip(),
                        "author": str(commit_obj.author),
                        "date": commit_obj.committed_datetime.isoformat(),
                    }
                )

            return {
                "commit_hash": commit.hexsha,
                "commit_hash_short": commit.hexsha[:8],
                "branch": branch,
                "commit_message": commit.message.strip(),
                "author": str(commit.author),
                "commit_date": commit.committed_datetime.isoformat(),
                "changed_files": changed_files,
                "untracked_files": untracked_files,
                "is_dirty": self.repo.is_dirty(),
                "recent_commits": recent_commits,
            }

        except Exception as e:
            return {"error": f"Failed to get git info: {str(e)}"}

    def _save_log_entry(self, log_entry: Dict[str, Any]) -> None:
        """Save log entry to file."""
        # Create filename with timestamp and commit hash
        timestamp = datetime.fromisoformat(log_entry["timestamp"])
        commit_hash = log_entry["git_info"].get("commit_hash_short", "unknown")

        filename = f"{timestamp.strftime('%Y%m%d_%H%M%S')}_{commit_hash}.json"
        filepath = self.results_dir / filename

        with open(filepath, "w") as f:
            json.dump(log_entry, f, indent=2, default=str)

    def _update_index(self, log_entry: Dict[str, Any]) -> None:
        """Update the index file with latest results."""
        index_path = self.results_dir / "index.json"

        # Load existing index
        if index_path.exists():
            with open(index_path, "r") as f:
                index = json.load(f)
        else:
            index = {"runs": [], "by_commit": {}, "by_branch": {}}

        # Add new entry
        entry_summary = {
            "timestamp": log_entry["timestamp"],
            "commit_hash": log_entry["git_info"].get("commit_hash"),
            "commit_hash_short": log_entry["git_info"].get("commit_hash_short"),
            "branch": log_entry["git_info"].get("branch"),
            "summary": log_entry["summary"],
            "filename": (
                f"{datetime.fromisoformat(log_entry['timestamp']).strftime('%Y%m%d_%H%M%S')}"
                + f"_{log_entry['git_info'].get('commit_hash_short', 'unknown')}.json"
            ),
        }

        # Add to runs list
        index["runs"].append(entry_summary)

        # Sort by timestamp (most recent first)
        index["runs"].sort(key=lambda x: x["timestamp"], reverse=True)

        # Limit to last 100 runs
        index["runs"] = index["runs"][:100]

        # Index by commit hash
        commit_hash = log_entry["git_info"].get("commit_hash")
        if commit_hash:
            if commit_hash not in index["by_commit"]:
                index["by_commit"][commit_hash] = []
            index["by_commit"][commit_hash].append(entry_summary)

        # Index by branch
        branch = log_entry["git_info"].get("branch")
        if branch:
            if branch not in index["by_branch"]:
                index["by_branch"][branch] = []
            index["by_branch"][branch].append(entry_summary)

        # Save updated index
        with open(index_path, "w") as f:
            json.dump(index, f, indent=2, default=str)

    def get_history(
        self,
        limit: int = 10,
        commit: Optional[str] = None,
        branch: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Get test run history."""
        index_path = self.results_dir / "index.json"

        if not index_path.exists():
            return []

        with open(index_path, "r") as f:
            index = json.load(f)

        runs = index.get("runs", [])

        # Filter by commit if specified
        if commit:
            runs = [
                run
                for run in runs
                if run.get("commit_hash_short") == commit[:8]
                or run.get("commit_hash") == commit
            ]

        # Filter by branch if specified
        if branch:
            runs = [run for run in runs if run.get("branch") == branch]

        # Limit results
        return runs[:limit]

    def compare_results(
        self,
        base: str,
        target: str,
        metric: Optional[str] = None,
        filter_by: Optional[str] = None,
        min_change: float = 0.01,
        include_unchanged: bool = False,
    ) -> Dict[str, Any]:
        """Compare test results between two commits or branches with enhanced filtering."""
        # Get results for base and target
        base_results = self._get_results_for_ref(base)
        target_results = self._get_results_for_ref(target)

        if not base_results:
            raise GitError(f"No test results found for base: {base}")

        if not target_results:
            raise GitError(f"No test results found for target: {target}")

        # Enhanced comparison structure
        comparison = {
            "base": base,
            "target": target,
            "base_timestamp": base_results.get("timestamp"),
            "target_timestamp": target_results.get("timestamp"),
            "base_summary": base_results.get("summary", {}),
            "target_summary": target_results.get("summary", {}),
            "summary_changes": {},
            "improvements": [],
            "regressions": [],
            "new_tests": [],
            "removed_tests": [],
            "unchanged": [],
            "score_changes": [],
            "evaluator_changes": {},
            "metadata": {
                "total_compared": 0,
                "min_change_threshold": min_change,
                "filter_applied": filter_by,
                "metric_focus": metric,
            },
        }

        # Compare overall summaries
        base_summary = base_results.get("summary", {})
        target_summary = target_results.get("summary", {})

        for key in ["total_tests", "passed", "failed", "pass_rate", "average_score"]:
            base_val = base_summary.get(key)
            target_val = target_summary.get(key)
            if base_val is not None and target_val is not None:
                if isinstance(base_val, (int, float)) and isinstance(
                    target_val, (int, float)
                ):
                    change = target_val - base_val
                    comparison["summary_changes"][key] = {
                        "base": base_val,
                        "target": target_val,
                        "change": change,
                        "percent_change": (
                            (change / base_val * 100) if base_val != 0 else 0
                        ),
                    }

        # Get test results from both
        base_tests = {
            test["test_name"]: test for test in base_results.get("test_results", [])
        }
        target_tests = {
            test["test_name"]: test for test in target_results.get("test_results", [])
        }

        # Find new and removed tests
        base_test_names = set(base_tests.keys())
        target_test_names = set(target_tests.keys())

        comparison["new_tests"] = list(target_test_names - base_test_names)
        comparison["removed_tests"] = list(base_test_names - target_test_names)

        # Compare common tests
        common_tests = base_test_names & target_test_names
        comparison["metadata"]["total_compared"] = len(common_tests)

        for test_name in common_tests:
            base_test = base_tests[test_name]
            target_test = target_tests[test_name]

            # Apply test name filter if specified
            if filter_by and filter_by.lower() not in test_name.lower():
                continue

            test_change = {
                "test_name": test_name,
                "base_passed": base_test["passed"],
                "target_passed": target_test["passed"],
                "base_score": base_test.get("score"),
                "target_score": target_test.get("score"),
                "base_duration": base_test.get("duration"),
                "target_duration": target_test.get("duration"),
                "base_evaluations": base_test.get("evaluations", {}),
                "target_evaluations": target_test.get("evaluations", {}),
                "changes": {},
            }

            # Status change analysis
            status_changed = False
            if base_test["passed"] != target_test["passed"]:
                status_changed = True
                status_change = {
                    "type": "status",
                    "from": "PASS" if base_test["passed"] else "FAIL",
                    "to": "PASS" if target_test["passed"] else "FAIL",
                    "improvement": target_test["passed"],
                }
                test_change["changes"]["status"] = status_change

                if target_test["passed"]:
                    comparison["improvements"].append(test_change)
                else:
                    comparison["regressions"].append(test_change)

            # Score change analysis
            score_changed = False
            if (
                base_test.get("score") is not None
                and target_test.get("score") is not None
            ):
                base_score = base_test["score"]
                target_score = target_test["score"]
                score_diff = target_score - base_score

                if abs(score_diff) >= min_change:
                    score_changed = True
                    score_change = {
                        "type": "score",
                        "from": base_score,
                        "to": target_score,
                        "change": score_diff,
                        "percent_change": (
                            (score_diff / base_score * 100) if base_score != 0 else 0
                        ),
                        "improvement": score_diff > 0,
                    }
                    test_change["changes"]["score"] = score_change
                    comparison["score_changes"].append(test_change)

                    if not status_changed:  # Don't double-count status changes
                        if score_diff > 0:
                            comparison["improvements"].append(test_change)
                        else:
                            comparison["regressions"].append(test_change)

            # Duration change analysis
            if (
                base_test.get("duration") is not None
                and target_test.get("duration") is not None
            ):
                duration_diff = target_test["duration"] - base_test["duration"]
                if abs(duration_diff) >= 0.1:  # 100ms threshold
                    duration_change = {
                        "type": "duration",
                        "from": base_test["duration"],
                        "to": target_test["duration"],
                        "change": duration_diff,
                        "improvement": duration_diff < 0,  # Faster is better
                    }
                    test_change["changes"]["duration"] = duration_change

            # Evaluator-specific changes
            self._compare_evaluator_results(
                base_test.get("evaluations", {}),
                target_test.get("evaluations", {}),
                test_change,
                comparison["evaluator_changes"],
                metric,
                min_change,
            )

            # Add to unchanged if no significant changes
            if not score_changed and not status_changed and include_unchanged:
                comparison["unchanged"].append(test_change)

        return comparison

    def _compare_evaluator_results(
        self,
        base_evals: Dict[str, Any],
        target_evals: Dict[str, Any],
        test_change: Dict[str, Any],
        evaluator_changes: Dict[str, Any],
        metric_filter: Optional[str],
        min_change: float,
    ) -> None:
        """Compare individual evaluator results."""
        all_evaluators = set(base_evals.keys()) | set(target_evals.keys())

        for evaluator_name in all_evaluators:
            # Skip if metric filter is specified and doesn't match
            if metric_filter and metric_filter != evaluator_name:
                continue

            base_eval = base_evals.get(evaluator_name, {})
            target_eval = target_evals.get(evaluator_name, {})

            eval_change = {
                "evaluator": evaluator_name,
                "base": base_eval,
                "target": target_eval,
                "changes": {},
            }

            # Compare scores
            base_score = base_eval.get("score")
            target_score = target_eval.get("score")

            if base_score is not None and target_score is not None:
                score_diff = target_score - base_score
                if abs(score_diff) >= min_change:
                    eval_change["changes"]["score"] = {
                        "from": base_score,
                        "to": target_score,
                        "change": score_diff,
                        "improvement": score_diff > 0,
                    }

            # Compare pass/fail
            base_passed = base_eval.get("passed")
            target_passed = target_eval.get("passed")

            if base_passed is not None and target_passed is not None:
                if base_passed != target_passed:
                    eval_change["changes"]["status"] = {
                        "from": "PASS" if base_passed else "FAIL",
                        "to": "PASS" if target_passed else "FAIL",
                        "improvement": target_passed,
                    }

            # Store evaluator changes
            if eval_change["changes"]:
                if evaluator_name not in evaluator_changes:
                    evaluator_changes[evaluator_name] = []
                evaluator_changes[evaluator_name].append(eval_change)

                # Add to test change
                if "evaluators" not in test_change["changes"]:
                    test_change["changes"]["evaluators"] = {}
                test_change["changes"]["evaluators"][evaluator_name] = eval_change[
                    "changes"
                ]

    def _get_results_for_ref(self, ref: str) -> Optional[Dict[str, Any]]:
        """Get test results for a specific git reference (commit or branch)."""
        index_path = self.results_dir / "index.json"

        if not index_path.exists():
            return None

        with open(index_path, "r") as f:
            index = json.load(f)

        # Try to find by commit hash first
        runs = index.get("runs", [])
        for run in runs:
            if (
                run.get("commit_hash_short") == ref[:8]
                or run.get("commit_hash") == ref
                or run.get("branch") == ref
            ):
                # Load full results
                filename = run.get("filename")
                if filename:
                    filepath = self.results_dir / filename
                    if filepath.exists():
                        with open(filepath, "r") as f:
                            return json.load(f)

        return None

    def cleanup_old_results(self, days: int = 30) -> None:
        """Clean up old test result files."""
        cutoff_time = time.time() - (days * 24 * 60 * 60)

        for file_path in self.results_dir.glob("*.json"):
            if file_path.name == "index.json":
                continue

            if file_path.stat().st_mtime < cutoff_time:
                file_path.unlink()

        # Rebuild index after cleanup
        self._rebuild_index()

    def _rebuild_index(self) -> None:
        """Rebuild the index from existing result files."""
        index = {"runs": [], "by_commit": {}, "by_branch": {}}

        for file_path in self.results_dir.glob("*.json"):
            if file_path.name == "index.json":
                continue

            try:
                with open(file_path, "r") as f:
                    log_entry = json.load(f)

                entry_summary = {
                    "timestamp": log_entry["timestamp"],
                    "commit_hash": log_entry["git_info"].get("commit_hash"),
                    "commit_hash_short": log_entry["git_info"].get("commit_hash_short"),
                    "branch": log_entry["git_info"].get("branch"),
                    "summary": log_entry["summary"],
                    "filename": file_path.name,
                }

                index["runs"].append(entry_summary)

            except Exception as e:
                print(f"Warning: Could not process {file_path}: {e}")

        # Sort by timestamp
        index["runs"].sort(key=lambda x: x["timestamp"], reverse=True)

        # Save rebuilt index
        index_path = self.results_dir / "index.json"
        with open(index_path, "w") as f:
            json.dump(index, f, indent=2, default=str)

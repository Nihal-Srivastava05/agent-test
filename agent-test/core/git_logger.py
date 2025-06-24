"""
Git-aware logger for AgentTest.

Tracks test results with git commit information for regression analysis.
"""

import json
import os
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

try:
    import git
    GIT_AVAILABLE = True
except ImportError:
    GIT_AVAILABLE = False

from .config import Config
from .decorators import TestResults
from ..utils.exceptions import GitError


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
                    "evaluations": result.evaluations
                }
                for result in results.test_results
            ],
            "metadata": results.metadata
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
                recent_commits.append({
                    "hash": commit_obj.hexsha[:8],
                    "message": commit_obj.message.strip(),
                    "author": str(commit_obj.author),
                    "date": commit_obj.committed_datetime.isoformat()
                })
            
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
                "recent_commits": recent_commits
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
        
        with open(filepath, 'w') as f:
            json.dump(log_entry, f, indent=2, default=str)
    
    def _update_index(self, log_entry: Dict[str, Any]) -> None:
        """Update the index file with latest results."""
        index_path = self.results_dir / "index.json"
        
        # Load existing index
        if index_path.exists():
            with open(index_path, 'r') as f:
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
            "filename": f"{datetime.fromisoformat(log_entry['timestamp']).strftime('%Y%m%d_%H%M%S')}_{log_entry['git_info'].get('commit_hash_short', 'unknown')}.json"
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
        with open(index_path, 'w') as f:
            json.dump(index, f, indent=2, default=str)
    
    def get_history(
        self, 
        limit: int = 10, 
        commit: Optional[str] = None, 
        branch: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get test run history."""
        index_path = self.results_dir / "index.json"
        
        if not index_path.exists():
            return []
        
        with open(index_path, 'r') as f:
            index = json.load(f)
        
        runs = index.get("runs", [])
        
        # Filter by commit if specified
        if commit:
            runs = [run for run in runs if run.get("commit_hash_short") == commit[:8] or run.get("commit_hash") == commit]
        
        # Filter by branch if specified
        if branch:
            runs = [run for run in runs if run.get("branch") == branch]
        
        # Limit results
        return runs[:limit]
    
    def compare_results(
        self, 
        base: str, 
        target: str, 
        metric: Optional[str] = None
    ) -> Dict[str, Any]:
        """Compare test results between two commits or branches."""
        # Get results for base and target
        base_results = self._get_results_for_ref(base)
        target_results = self._get_results_for_ref(target)
        
        if not base_results:
            raise GitError(f"No test results found for base: {base}")
        
        if not target_results:
            raise GitError(f"No test results found for target: {target}")
        
        # Compare results
        comparison = {
            "base": base,
            "target": target,
            "base_timestamp": base_results.get("timestamp"),
            "target_timestamp": target_results.get("timestamp"),
            "improvements": [],
            "regressions": [],
            "new_tests": [],
            "removed_tests": []
        }
        
        # Get test results from both
        base_tests = {test["test_name"]: test for test in base_results.get("test_results", [])}
        target_tests = {test["test_name"]: test for test in target_results.get("test_results", [])}
        
        # Find new and removed tests
        base_test_names = set(base_tests.keys())
        target_test_names = set(target_tests.keys())
        
        comparison["new_tests"] = list(target_test_names - base_test_names)
        comparison["removed_tests"] = list(base_test_names - target_test_names)
        
        # Compare common tests
        common_tests = base_test_names & target_test_names
        
        for test_name in common_tests:
            base_test = base_tests[test_name]
            target_test = target_tests[test_name]
            
            # Compare pass/fail status
            if base_test["passed"] != target_test["passed"]:
                if target_test["passed"]:
                    comparison["improvements"].append(f"{test_name}: FAIL → PASS")
                else:
                    comparison["regressions"].append(f"{test_name}: PASS → FAIL")
            
            # Compare scores if available
            if base_test.get("score") is not None and target_test.get("score") is not None:
                score_diff = target_test["score"] - base_test["score"]
                if abs(score_diff) > 0.1:  # Significant change
                    if score_diff > 0:
                        comparison["improvements"].append(f"{test_name}: score improved by {score_diff:.2f}")
                    else:
                        comparison["regressions"].append(f"{test_name}: score decreased by {abs(score_diff):.2f}")
        
        return comparison
    
    def _get_results_for_ref(self, ref: str) -> Optional[Dict[str, Any]]:
        """Get test results for a specific git reference (commit or branch)."""
        index_path = self.results_dir / "index.json"
        
        if not index_path.exists():
            return None
        
        with open(index_path, 'r') as f:
            index = json.load(f)
        
        # Try to find by commit hash first
        runs = index.get("runs", [])
        for run in runs:
            if (run.get("commit_hash_short") == ref[:8] or 
                run.get("commit_hash") == ref or
                run.get("branch") == ref):
                
                # Load full results
                filename = run.get("filename")
                if filename:
                    filepath = self.results_dir / filename
                    if filepath.exists():
                        with open(filepath, 'r') as f:
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
                with open(file_path, 'r') as f:
                    log_entry = json.load(f)
                
                entry_summary = {
                    "timestamp": log_entry["timestamp"],
                    "commit_hash": log_entry["git_info"].get("commit_hash"),
                    "commit_hash_short": log_entry["git_info"].get("commit_hash_short"),
                    "branch": log_entry["git_info"].get("branch"),
                    "summary": log_entry["summary"],
                    "filename": file_path.name
                }
                
                index["runs"].append(entry_summary)
                
            except Exception as e:
                print(f"Warning: Could not process {file_path}: {e}")
        
        # Sort by timestamp
        index["runs"].sort(key=lambda x: x["timestamp"], reverse=True)
        
        # Save rebuilt index
        index_path = self.results_dir / "index.json"
        with open(index_path, 'w') as f:
            json.dump(index, f, indent=2, default=str) 
"""
AgentTest Logging System

Provides structured logging similar to pytest with detailed test information,
progress tracking, and failure analysis.
"""

import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from rich.console import Console
from rich.tree import Tree


@dataclass
class LogEntry:
    """Structured log entry for AgentTest."""

    timestamp: float
    level: str
    category: str
    message: str
    details: Dict[str, Any] = None
    test_name: Optional[str] = None

    def __post_init__(self):
        if self.details is None:
            self.details = {}


class AgentTestLogger:
    """Advanced logger for AgentTest with structured output."""

    def __init__(self, verbose: bool = False, quiet: bool = False):
        self.verbose = verbose
        self.quiet = quiet
        self.console = Console()
        self.entries: List[LogEntry] = []
        self.start_time = time.time()

        # Test execution tracking
        self.current_test = None
        self.test_progress = None
        self.total_tests = 0
        self.completed_tests = 0

    def log(
        self,
        level: str,
        category: str,
        message: str,
        details: Dict[str, Any] = None,
        test_name: str = None,
    ):
        """Log a structured entry."""
        entry = LogEntry(
            timestamp=time.time(),
            level=level,
            category=category,
            message=message,
            details=details or {},
            test_name=test_name,
        )
        self.entries.append(entry)

        if not self.quiet:
            self._display_entry(entry)

    def info(self, category: str, message: str, **kwargs):
        """Log info level message."""
        self.log(
            "INFO", category, message, kwargs.get("details"), kwargs.get("test_name")
        )

    def warning(self, category: str, message: str, **kwargs):
        """Log warning level message."""
        self.log(
            "WARNING", category, message, kwargs.get("details"), kwargs.get("test_name")
        )

    def error(self, category: str, message: str, **kwargs):
        """Log error level message."""
        self.log(
            "ERROR", category, message, kwargs.get("details"), kwargs.get("test_name")
        )

    def debug(self, category: str, message: str, **kwargs):
        """Log debug level message (only if verbose)."""
        if self.verbose:
            self.log(
                "DEBUG",
                category,
                message,
                kwargs.get("details"),
                kwargs.get("test_name"),
            )

    def test_started(self, test_name: str, total_tests: int):
        """Log test execution start."""
        self.current_test = test_name
        self.total_tests = total_tests

        if self.verbose:
            self.info("TEST_START", f"Starting test: {test_name}")

    def test_completed(
        self,
        test_name: str,
        passed: bool,
        duration: float,
        score: Optional[float] = None,
        error: str = None,
    ):
        """Log test completion."""
        self.completed_tests += 1

        details = {
            "duration": duration,
            "score": score,
            "error": error,
            "progress": f"{self.completed_tests}/{self.total_tests}",
        }

        if passed:
            self.info(
                "TEST_PASS", f"✅ {test_name}", details=details, test_name=test_name
            )
        else:
            self.error(
                "TEST_FAIL", f"❌ {test_name}", details=details, test_name=test_name
            )

            if error and self.verbose:
                self.error("TEST_ERROR", f"Error details: {error}", test_name=test_name)

    def evaluator_started(self, evaluator_name: str, test_name: str):
        """Log evaluator execution start."""
        if self.verbose:
            self.debug(
                "EVALUATOR",
                f"Running {evaluator_name} for {test_name}",
                test_name=test_name,
            )

    def evaluator_completed(
        self,
        evaluator_name: str,
        test_name: str,
        passed: bool,
        score: Optional[float] = None,
        error: str = None,
    ):
        """Log evaluator completion."""
        details = {"score": score, "error": error}

        if passed:
            if self.verbose:
                self.debug(
                    "EVALUATOR_PASS",
                    f"✅ {evaluator_name}: PASSED",
                    details=details,
                    test_name=test_name,
                )
        else:
            if self.verbose:
                self.debug(
                    "EVALUATOR_FAIL",
                    f"❌ {evaluator_name}: FAILED",
                    details=details,
                    test_name=test_name,
                )

    def discovery_started(self, path: str, pattern: str):
        """Log test discovery start."""
        self.info(
            "DISCOVERY", f"🔍 Discovering tests in {path} with pattern '{pattern}'"
        )

    def discovery_completed(self, test_count: int, files_scanned: int):
        """Log test discovery completion."""
        self.info("DISCOVERY", f"📋 Found {test_count} tests in {files_scanned} files")

    def session_started(self, config_info: Dict[str, Any]):
        """Log test session start."""
        self.info("SESSION", "🧪 Starting AgentTest session")
        if self.verbose and config_info:
            self.debug("CONFIG", "Configuration loaded", details=config_info)

    def session_completed(self, summary: Dict[str, Any]):
        """Log test session completion."""
        total_time = time.time() - self.start_time

        self.info("SESSION", f"🏁 Test session completed in {total_time:.2f}s")

        # Display final summary
        if not self.quiet:
            self._display_final_summary(summary, total_time)

    def _display_entry(self, entry: LogEntry):
        """Display a log entry to console."""
        if entry.level == "DEBUG" and not self.verbose:
            return

        timestamp = time.strftime("%H:%M:%S", time.localtime(entry.timestamp))

        # Color coding by level
        level_colors = {
            "INFO": "blue",
            "WARNING": "yellow",
            "ERROR": "red",
            "DEBUG": "dim",
        }
        color = level_colors.get(entry.level, "white")

        if self.verbose:
            prefix = f"[{timestamp}] [{entry.category}]"
            self.console.print(f"[{color}]{prefix}[/{color}] {entry.message}")

            if entry.details and self.verbose:
                for key, value in entry.details.items():
                    if value is not None:
                        self.console.print(f"  {key}: {value}", style="dim")
        else:
            # Simplified output for non-verbose mode
            if entry.category in ["TEST_PASS", "TEST_FAIL", "SESSION", "DISCOVERY"]:
                self.console.print(f"[{color}]{entry.message}[/{color}]")

    def _display_final_summary(self, summary: Dict[str, Any], total_time: float):
        """Display final test session summary."""
        tree = Tree("📊 Test Session Summary")

        # Basic stats
        stats_branch = tree.add("📈 Statistics")
        stats_branch.add(f"Total Tests: {summary.get('total_tests', 0)}")
        stats_branch.add(f"Passed: {summary.get('passed', 0)} ✅")
        stats_branch.add(f"Failed: {summary.get('failed', 0)} ❌")
        stats_branch.add(f"Pass Rate: {summary.get('pass_rate', 0):.1f}%")
        stats_branch.add(f"Duration: {total_time:.2f}s")

        if summary.get("average_score"):
            stats_branch.add(f"Average Score: {summary['average_score']:.3f}")

        # Performance info
        if self.verbose:
            perf_branch = tree.add("⚡ Performance")
            avg_duration = summary.get("total_duration", 0) / max(
                summary.get("total_tests", 1), 1
            )
            perf_branch.add(f"Average Test Duration: {avg_duration:.3f}s")
            perf_branch.add(f"Total Test Time: {summary.get('total_duration', 0):.2f}s")

            # Log entry stats
            log_stats = self._get_log_statistics()
            logs_branch = tree.add("📝 Log Statistics")
            for category, count in log_stats.items():
                logs_branch.add(f"{category}: {count}")

        self.console.print(tree)

    def _get_log_statistics(self) -> Dict[str, int]:
        """Get statistics about log entries."""
        stats = {}
        for entry in self.entries:
            stats[entry.category] = stats.get(entry.category, 0) + 1
        return stats

    def get_failed_tests(self) -> List[Dict[str, Any]]:
        """Get information about failed tests."""
        failed_tests = []
        for entry in self.entries:
            if entry.category == "TEST_FAIL" and entry.test_name:
                failed_tests.append(
                    {
                        "test_name": entry.test_name,
                        "message": entry.message,
                        "details": entry.details,
                        "timestamp": entry.timestamp,
                    }
                )
        return failed_tests

    def export_logs(self, file_path: str, format: str = "json"):
        """Export logs to file."""
        import json
        from pathlib import Path

        if format == "json":
            data = {
                "session_info": {
                    "start_time": self.start_time,
                    "end_time": time.time(),
                    "total_duration": time.time() - self.start_time,
                    "verbose": self.verbose,
                },
                "entries": [
                    {
                        "timestamp": entry.timestamp,
                        "level": entry.level,
                        "category": entry.category,
                        "message": entry.message,
                        "details": entry.details,
                        "test_name": entry.test_name,
                    }
                    for entry in self.entries
                ],
            }

            Path(file_path).write_text(json.dumps(data, indent=2))
        else:
            raise ValueError(f"Unsupported export format: {format}")


# Global logger instance
_logger: Optional[AgentTestLogger] = None


def get_logger() -> AgentTestLogger:
    """Get the global AgentTest logger."""
    global _logger
    if _logger is None:
        _logger = AgentTestLogger()
    return _logger


def setup_logger(verbose: bool = False, quiet: bool = False) -> AgentTestLogger:
    """Setup the global AgentTest logger."""
    global _logger
    _logger = AgentTestLogger(verbose=verbose, quiet=quiet)
    return _logger


def reset_logger():
    """Reset the global logger."""
    global _logger
    _logger = None

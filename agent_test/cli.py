"""
Command Line Interface for AgentTest.

Provides pytest-like CLI commands for AI agent testing.
"""

from pathlib import Path
from typing import List, Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from .core.config import Config
from .core.git_logger import GitLogger
from .core.init import initialize_project
from .core.logging import setup_logger
from .core.runner import TestRunner
from .generators.test_generator import TestGenerator
from .utils.exceptions import AgentTestError

app = typer.Typer(
    name="agenttest",
    help="A pytest-like testing framework for AI agents and prompts",
    add_completion=False,
)

console = Console()


@app.command()
def init(
    path: Path = typer.Argument(
        Path("."), help="Directory to initialize (defaults to current directory)"
    ),
    template: str = typer.Option(
        "basic",
        "--template",
        "-t",
        help="Template to use: basic, langchain, llamaindex",
    ),
    overwrite: bool = typer.Option(
        False, "--overwrite", help="Overwrite existing configuration"
    ),
) -> None:
    """Initialize a new AgentTest project."""
    try:
        console.print("[bold blue]🧪 Initializing AgentTest project...[/bold blue]")

        success = initialize_project(path, template, overwrite)

        if success:
            console.print(
                "[bold green]✅ AgentTest project initialized successfully![/bold green]"
            )
            console.print(f"📁 Configuration created in: {path / '.agenttest'}")
            console.print("\n🚀 Next steps:")
            console.print("1. Configure your agents in .agenttest/config.yaml")
            console.print("2. Add test cases to tests/")
            console.print("3. Run: agenttest run")
        else:
            console.print("[bold red]❌ Failed to initialize project[/bold red]")
            raise typer.Exit(1)

    except AgentTestError as e:
        console.print(f"[bold red]Error: {e}[/bold red]")
        raise typer.Exit(1)


@app.command()
def run(
    path: Optional[Path] = typer.Option(
        None, "--path", "-p", help="Path to test files or directory"
    ),
    pattern: str = typer.Option("test_*.py", "--pattern", help="Test file pattern"),
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Verbose output with detailed logging"
    ),
    quiet: bool = typer.Option(
        False, "--quiet", "-q", help="Suppress non-essential output"
    ),
    ci: bool = typer.Option(
        False, "--ci", help="CI mode - exit with error code on failures"
    ),
    output: Optional[Path] = typer.Option(
        None, "--output", "-o", help="Output file for results"
    ),
    log_output: Optional[Path] = typer.Option(
        None, "--log-output", help="Export detailed logs to file"
    ),
    tags: Optional[List[str]] = typer.Option(
        None, "--tag", "-t", help="Run tests with specific tags"
    ),
) -> None:
    """Run agent tests."""
    try:
        # Setup logging first
        logger = setup_logger(verbose=verbose, quiet=quiet)

        config = Config.load()
        runner = TestRunner(config)

        if not quiet:
            console.print("[bold blue]🧪 Running AgentTest suite...[/bold blue]")

        # Discover and run tests
        results = runner.run_tests(
            path=path, pattern=pattern, tags=tags, verbose=verbose
        )

        # Display results (enhanced with detailed failure info)
        if not quiet:
            _display_results(results)

        # Export logs if requested
        if log_output:
            logger.export_logs(str(log_output))
            if not quiet:
                console.print(f"📄 Detailed logs saved to: {log_output}")

        # Log to git-aware logger
        git_logger = GitLogger(config)
        git_logger.log_results(results)

        # Save output if specified
        if output:
            results.save_to_file(str(output))
            if not quiet:
                console.print(f"📄 Results saved to: {output}")

        # Exit with error code in CI mode if there are failures
        if ci and results.has_failures():
            if not quiet:
                console.print(
                    "[bold red]❌ Tests failed - exiting with error code[/bold red]"
                )
            raise typer.Exit(1)

        if not quiet:
            console.print("[bold green]✅ Test run completed![/bold green]")

    except AgentTestError as e:
        console.print(f"[bold red]Error: {e}[/bold red]")
        raise typer.Exit(1)


@app.command()
def generate(
    agent: Optional[str] = typer.Option(
        None, "--agent", "-a", help="Agent file or class to generate tests for"
    ),
    output: Optional[Path] = typer.Option(
        None, "--output", "-o", help="Output file for generated tests"
    ),
    count: int = typer.Option(
        5, "--count", "-c", help="Number of test cases to generate"
    ),
    format: str = typer.Option(
        "python", "--format", "-f", help="Output format: python, yaml, json"
    ),
) -> None:
    """Generate test cases automatically using AI."""
    try:
        config = Config.load()
        generator = TestGenerator(config)

        console.print("[bold blue]🤖 Generating test cases...[/bold blue]")

        if not agent:
            # Auto-discover agents
            agents = generator.discover_agents()
            if not agents:
                console.print(
                    "[yellow]⚠️  No agents found. Please specify --agent parameter[/yellow]"
                )
                raise typer.Exit(1)
            agent = agents[0]  # Use first discovered agent

        # Generate tests
        with console.status("Generating tests..."):
            generated_tests = generator.generate_tests(
                agent_path=agent, count=count, format=format
            )

        # Save or display results
        if output:
            output.write_text(generated_tests)
            console.print(f"📄 Generated tests saved to: {output}")
        else:
            console.print("[bold green]Generated Tests:[/bold green]")
            console.print(generated_tests)

        console.print(f"[bold green]✅ Generated {count} test cases![/bold green]")

    except AgentTestError as e:
        console.print(f"[bold red]Error: {e}[/bold red]")
        raise typer.Exit(1)


@app.command()
def log(
    limit: int = typer.Option(
        10, "--limit", "-l", help="Number of recent runs to show"
    ),
    commit: Optional[str] = typer.Option(
        None, "--commit", "-c", help="Show results for specific commit"
    ),
    branch: Optional[str] = typer.Option(
        None, "--branch", "-b", help="Show results for specific branch"
    ),
) -> None:
    """Show test run history with git information."""
    try:
        config = Config.load()
        git_logger = GitLogger(config)

        console.print("[bold blue]📊 Test Run History[/bold blue]")

        history = git_logger.get_history(limit=limit, commit=commit, branch=branch)

        if not history:
            console.print("[yellow]No test history found[/yellow]")
            return

        _display_history(history)

    except AgentTestError as e:
        console.print(f"[bold red]Error: {e}[/bold red]")
        raise typer.Exit(1)


@app.command()
def compare(
    base: str = typer.Argument(help="Base commit/branch to compare from"),
    target: Optional[str] = typer.Argument(
        None, help="Target commit/branch to compare to (defaults to HEAD)"
    ),
    metric: Optional[str] = typer.Option(
        None,
        "--metric",
        "-m",
        help="Focus on specific evaluator/metric (similarity, contains, regex, etc.)",
    ),
    filter_by: Optional[str] = typer.Option(
        None, "--filter", "-f", help="Filter tests by name pattern"
    ),
    min_change: float = typer.Option(
        0.01,
        "--min-change",
        "-c",
        help="Minimum change threshold for scores (default: 0.01)",
    ),
    include_unchanged: bool = typer.Option(
        False,
        "--include-unchanged",
        "-u",
        help="Include tests with no significant changes",
    ),
    detailed: bool = typer.Option(
        False, "--detailed", "-d", help="Show detailed evaluator-level changes"
    ),
    export: Optional[str] = typer.Option(
        None, "--export", "-e", help="Export comparison to JSON file"
    ),
) -> None:
    """Compare test results between commits/branches with advanced filtering."""
    try:
        config = Config.load()
        git_logger = GitLogger(config)

        target = target or "HEAD"

        console.print(f"[bold blue]📊 Comparing {base} → {target}[/bold blue]")

        comparison = git_logger.compare_results(
            base,
            target,
            metric=metric,
            filter_by=filter_by,
            min_change=min_change,
            include_unchanged=include_unchanged,
        )

        _display_comparison(comparison, detailed=detailed)

        # Export if requested
        if export:
            import json

            with open(export, "w") as f:
                json.dump(comparison, f, indent=2, default=str)
            console.print(f"[green]Comparison exported to {export}[/green]")

    except AgentTestError as e:
        console.print(f"[bold red]Error: {e}[/bold red]")
        raise typer.Exit(1)


@app.command()
def dashboard(
    port: int = typer.Option(8080, "--port", "-p", help="Port to run dashboard on"),
    host: str = typer.Option("localhost", "--host", help="Host to bind dashboard to"),
) -> None:
    """Launch the AgentTest dashboard (future feature)."""
    console.print("[yellow]🚧 Dashboard feature coming soon![/yellow]")
    console.print("For now, use 'agenttest log' and 'agenttest compare' commands")


def _display_results(results) -> None:
    """Display test results in a formatted table with detailed error information."""
    table = Table(title="Test Results")
    table.add_column("Test", style="cyan")
    table.add_column("Status", style="bold")
    table.add_column("Score", style="magenta")
    table.add_column("Duration", style="green")

    failed_tests = []

    for result in results.test_results:
        status = "✅ PASS" if result.passed else "❌ FAIL"
        score = f"{result.score:.2f}" if result.score is not None else "N/A"
        duration = f"{result.duration:.2f}s"

        table.add_row(result.test_name, status, score, duration)

        # Collect failed tests for detailed reporting
        if not result.passed:
            failed_tests.append(result)

    console.print(table)

    # Display detailed failure information
    if failed_tests:
        console.print("\n[bold red]💥 FAILURE DETAILS[/bold red]")
        console.print("=" * 60)

        for i, result in enumerate(failed_tests, 1):
            console.print(f"\n[bold red]{i}. {result.test_name}[/bold red]")
            console.print("─" * 40)

            # Display error message if present
            if result.error:
                console.print(f"[red]❌ Error:[/red] {result.error}")

            # Display evaluation details
            if result.evaluations:
                console.print("[yellow]📊 Evaluation Results:[/yellow]")
                for evaluator_name, evaluation in result.evaluations.items():
                    if isinstance(evaluation, dict):
                        if evaluation.get("error"):
                            console.print(
                                f"  • [red]{evaluator_name}:[/red] {evaluation['error']}"
                            )
                        else:
                            console.print(f"  • [cyan]{evaluator_name}:[/cyan]")
                            if (
                                "score" in evaluation
                                and evaluation["score"] is not None
                            ):
                                console.print(f"    Score: {evaluation['score']:.3f}")
                            if (
                                "threshold" in evaluation
                                and evaluation["threshold"] is not None
                            ):
                                console.print(
                                    f"    Threshold: {evaluation['threshold']}"
                                )
                            if "passed" in evaluation:
                                console.print(
                                    f"    Passed: {'✅' if evaluation['passed'] else '❌'}"
                                )

                            # Display specific failure reasons
                            if "details" in evaluation and evaluation["details"]:
                                details = evaluation["details"]
                                if "reason" in details:
                                    console.print(f"    Reason: {details['reason']}")
                                if "actual" in details and "expected" in details:
                                    console.print(
                                        f"    Expected: [green]{details['expected']}[/green]"
                                    )
                                    console.print(
                                        f"    Actual:   [red]{details['actual']}[/red]"
                                    )
                                if "similarity" in details:
                                    console.print(
                                        f"    Similarity: {details['similarity']:.3f}"
                                    )
                                if "pattern" in details:
                                    console.print(f"    Pattern: {details['pattern']}")
                                if "matches" in details:
                                    console.print(f"    Matches: {details['matches']}")

            # Display additional test details
            if result.details:
                console.print("[yellow]🔍 Test Details:[/yellow]")
                for key, value in result.details.items():
                    if key not in ["evaluations"]:  # Skip redundant info
                        if isinstance(value, (str, int, float, bool)):
                            console.print(f"  • {key}: {value}")
                        elif isinstance(value, dict):
                            console.print(f"  • {key}:")
                            for sub_key, sub_value in value.items():
                                console.print(f"    - {sub_key}: {sub_value}")

    # Summary
    total = len(results.test_results)
    passed = sum(1 for r in results.test_results if r.passed)
    failed = total - passed

    summary_text = f"Total: {total} | Passed: {passed} | Failed: {failed}"
    if failed > 0:
        summary_text += "\n\n[bold red]💡 Tip:[/bold red] Check the failure details above for specific issues."
        summary_text += "\n[bold blue]🔧 Common fixes:[/bold blue]"
        summary_text += "\n  • Verify API keys are set (GOOGLE_API_KEY, OPENAI_API_KEY)"
        summary_text += "\n  • Check test input/expected output formats"
        summary_text += "\n  • Review evaluation criteria and thresholds"

    summary = Panel(summary_text, title="Summary", title_align="left")
    console.print(summary)


def _display_history(history: List[dict]) -> None:
    """Display test history in a formatted table."""
    table = Table(title="Test History")
    table.add_column("Timestamp", style="cyan")
    table.add_column("Commit", style="yellow")
    table.add_column("Branch", style="green")
    table.add_column("Tests", style="magenta")
    table.add_column("Pass Rate", style="bold")

    for entry in history:
        timestamp = entry["timestamp"]
        commit = entry["commit_hash"][:8]
        branch = entry["branch"]
        test_count = entry["summary"]["total_tests"]
        pass_rate = f"{entry['summary']['pass_rate']:.1f}%"

        table.add_row(timestamp, commit, branch, str(test_count), pass_rate)

    console.print(table)


def _display_comparison(comparison: dict, detailed: bool = False) -> None:
    """Display enhanced comparison results."""
    from rich.tree import Tree

    # Header with metadata
    metadata = comparison.get("metadata", {})
    console.print(
        f"[bold]Base:[/bold] {comparison['base']} ({comparison.get('base_timestamp', 'Unknown time')})"
    )
    console.print(
        f"[bold]Target:[/bold] {comparison['target']} ({comparison.get('target_timestamp', 'Unknown time')})"
    )

    if metadata.get("filter_applied"):
        console.print(f"[dim]Filter: {metadata['filter_applied']}[/dim]")
    if metadata.get("metric_focus"):
        console.print(f"[dim]Metric focus: {metadata['metric_focus']}[/dim]")
    console.print()

    # Summary changes
    summary_changes = comparison.get("summary_changes", {})
    if summary_changes:
        console.print("[bold]📊 Overall Summary Changes:[/bold]")
        summary_table = Table(show_header=True, header_style="bold blue")
        summary_table.add_column("Metric")
        summary_table.add_column("Base", justify="right")
        summary_table.add_column("Target", justify="right")
        summary_table.add_column("Change", justify="right")
        summary_table.add_column("% Change", justify="right")

        for metric, change_data in summary_changes.items():
            change_val = change_data["change"]
            percent_change = change_data["percent_change"]

            # Color coding for changes
            if change_val > 0:
                change_str = f"[green]+{change_val:.3f}[/green]"
                percent_str = f"[green]+{percent_change:.1f}%[/green]"
            elif change_val < 0:
                change_str = f"[red]{change_val:.3f}[/red]"
                percent_str = f"[red]{percent_change:.1f}%[/red]"
            else:
                change_str = "0.000"
                percent_str = "0.0%"

            summary_table.add_row(
                metric.replace("_", " ").title(),
                str(change_data["base"]),
                str(change_data["target"]),
                change_str,
                percent_str,
            )

        console.print(summary_table)
        console.print()

    # Test changes overview
    total_improvements = len(comparison.get("improvements", []))
    total_regressions = len(comparison.get("regressions", []))
    total_new = len(comparison.get("new_tests", []))
    total_removed = len(comparison.get("removed_tests", []))
    total_unchanged = len(comparison.get("unchanged", []))

    overview_tree = Tree("🔍 Test Changes Overview")
    if total_improvements > 0:
        overview_tree.add(f"[green]📈 Improvements: {total_improvements}[/green]")
    if total_regressions > 0:
        overview_tree.add(f"[red]📉 Regressions: {total_regressions}[/red]")
    if total_new > 0:
        overview_tree.add(f"[blue]🆕 New Tests: {total_new}[/blue]")
    if total_removed > 0:
        overview_tree.add(f"[yellow]🗑️ Removed Tests: {total_removed}[/yellow]")
    if total_unchanged > 0:
        overview_tree.add(f"[dim]😐 Unchanged: {total_unchanged}[/dim]")

    console.print(overview_tree)
    console.print()

    # Detailed improvements
    if comparison.get("improvements"):
        console.print("[bold green]📈 Improvements:[/bold green]")
        for improvement in comparison["improvements"]:
            _display_test_change(improvement, "improvement", detailed)
        console.print()

    # Detailed regressions
    if comparison.get("regressions"):
        console.print("[bold red]📉 Regressions:[/bold red]")
        for regression in comparison["regressions"]:
            _display_test_change(regression, "regression", detailed)
        console.print()

    # New tests
    if comparison.get("new_tests"):
        console.print("[bold blue]🆕 New Tests:[/bold blue]")
        for test in comparison["new_tests"]:
            console.print(f"  • [blue]{test}[/blue]")
        console.print()

    # Removed tests
    if comparison.get("removed_tests"):
        console.print("[bold yellow]🗑️ Removed Tests:[/bold yellow]")
        for test in comparison["removed_tests"]:
            console.print(f"  • [yellow]{test}[/yellow]")
        console.print()

    # Score changes (if not already shown in improvements/regressions)
    score_changes = comparison.get("score_changes", [])
    significant_score_changes = [
        change
        for change in score_changes
        if change not in comparison.get("improvements", [])
        and change not in comparison.get("regressions", [])
    ]

    if significant_score_changes:
        console.print("[bold]📊 Score Changes:[/bold]")
        for change in significant_score_changes:
            _display_test_change(change, "score_change", detailed)
        console.print()

    # Evaluator-specific changes (detailed mode)
    if detailed and comparison.get("evaluator_changes"):
        console.print("[bold]🔍 Evaluator-Specific Changes:[/bold]")
        for evaluator, changes in comparison["evaluator_changes"].items():
            console.print(f"  [bold]{evaluator}:[/bold]")
            for change in changes:
                test_name = change.get("test_name", "Unknown")
                changes_detail = change.get("changes", {})

                for change_type, change_data in changes_detail.items():
                    if change_type == "score":
                        score_change = change_data["change"]
                        color = "green" if score_change > 0 else "red"
                        console.print(
                            f"    • {test_name}: [{color}]{change_data['from']:.3f} → {change_data['to']:.3f} ({score_change:+.3f})[/{color}]"
                        )
                    elif change_type == "status":
                        color = "green" if change_data["improvement"] else "red"
                        console.print(
                            f"    • {test_name}: [{color}]{change_data['from']} → {change_data['to']}[/{color}]"
                        )
        console.print()

    # Unchanged tests (if requested)
    if comparison.get("unchanged"):
        console.print(
            f"[dim]😐 Unchanged Tests ({len(comparison['unchanged'])}):[/dim]"
        )
        for unchanged in comparison["unchanged"][:5]:  # Show only first 5
            console.print(f"  • [dim]{unchanged['test_name']}[/dim]")
        if len(comparison["unchanged"]) > 5:
            console.print(
                f"  • [dim]... and {len(comparison['unchanged']) - 5} more[/dim]"
            )
        console.print()


def _display_test_change(
    change: dict, change_type: str, detailed: bool = False
) -> None:
    """Display individual test change with details."""
    test_name = change["test_name"]
    changes = change.get("changes", {})

    # Main change description
    main_change = ""
    color = "white"

    if "status" in changes:
        status_change = changes["status"]
        color = "green" if status_change["improvement"] else "red"
        main_change = f"{status_change['from']} → {status_change['to']}"

    if "score" in changes:
        score_change = changes["score"]
        score_color = "green" if score_change["improvement"] else "red"
        score_text = f"score: {score_change['from']:.3f} → {score_change['to']:.3f} ({score_change['change']:+.3f})"

        if main_change:
            main_change += f", {score_text}"
        else:
            main_change = score_text
            color = score_color

    console.print(f"  • [{color}]{test_name}[/{color}]: {main_change}")

    # Additional details if requested
    if detailed:
        if "duration" in changes:
            duration_change = changes["duration"]
            duration_color = "green" if duration_change["improvement"] else "yellow"
            console.print(
                f"Duration: [{duration_color}]{duration_change['from']:.3f}s "
                + f"→ {duration_change['to']:.3f}s ({duration_change['change']:+.3f}s)[/{duration_color}]"
            )

        if "evaluators" in changes:
            console.print("    Evaluator changes:")
            for evaluator, eval_changes in changes["evaluators"].items():
                for change_type, change_data in eval_changes.items():
                    if change_type == "score":
                        eval_color = "green" if change_data["improvement"] else "red"
                        console.print(
                            f"      {evaluator}: [{eval_color}]{change_data['from']:.3f} → {change_data['to']:.3f}[/{eval_color}]"
                        )
                    elif change_type == "status":
                        eval_color = "green" if change_data["improvement"] else "red"
                        console.print(
                            f"      {evaluator}: [{eval_color}]{change_data['from']} → {change_data['to']}[/{eval_color}]"
                        )


if __name__ == "__main__":
    app()

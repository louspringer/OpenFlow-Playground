#!/usr/bin/env python3
"""
GitHub DSL - Simple interface for GitHub operations
"""

import json
import logging
import subprocess
import sys
from pathlib import Path
from typing import Any

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout), logging.FileHandler("gh_dsl.log")],
)
logger = logging.getLogger(__name__)


class GitHubDSL:
    def __init__(self):
        self.base_dir = Path.cwd()
        logger.info(f"GitHub DSL initialized in {self.base_dir}")

    def run_gh(self, *args) -> dict[str, Any]:
        """Run gh command and return structured result"""
        logger.info(f"Running gh command: {' '.join(args)}")

        try:
            result = subprocess.run(
                ["gh"] + list(args),
                capture_output=True,
                text=True,
                cwd=self.base_dir,
            )

            logger.info(f"Command completed with return code: {result.returncode}")
            if result.stdout:
                logger.info(f"STDOUT: {result.stdout.strip()}")
            if result.stderr:
                logger.warning(f"STDERR: {result.stderr.strip()}")

            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
            }
        except Exception as e:
            logger.error(f"Exception running gh command: {e}")
            return {
                "success": False,
                "error": str(e),
                "stdout": "",
                "stderr": str(e),
                "returncode": 1,
            }

    def create_pr_from_config(self, config_file: str) -> dict[str, Any]:
        """Create a PR using config file"""
        logger.info(f"Creating PR from config: {config_file}")

        try:
            with open(config_file) as f:
                config = json.load(f)
            logger.info(f"Loaded config: {config}")
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
            return {
                "success": False,
                "error": f"Failed to load config: {e}",
                "stdout": "",
                "stderr": str(e),
                "returncode": 1,
            }

        # Build args from config
        args = ["pr", "create"]

        if "title" in config:
            args.extend(["--title", config["title"]])

        if "body_file" in config:
            args.extend(["--body-file", config["body_file"]])

        if "base" in config:
            args.extend(["--base", config["base"]])

        if "head" in config:
            args.extend(["--head", config["head"]])

        if "labels" in config and config["labels"]:
            for label in config["labels"]:
                args.extend(["--label", label])

        if "assignees" in config and config["assignees"]:
            for assignee in config["assignees"]:
                args.extend(["--assignee", assignee])

        if "reviewers" in config and config["reviewers"]:
            for reviewer in config["reviewers"]:
                args.extend(["--reviewer", reviewer])

        if config.get("draft", False):
            args.append("--draft")

        logger.info(f"Built gh args: {args}")
        return self.run_gh(*args)

    def create_pr(
        self,
        title: str,
        body_file: str,
        base: str = "develop",
        head: str = None,
    ) -> dict[str, Any]:
        """Create a PR with title and body from file"""
        logger.info(f"Creating PR: {title} -> {base}")

        if head is None:
            result = self.run_gh("branch", "--show-current")
            if not result["success"]:
                return result
            head = result["stdout"].strip()
            logger.info(f"Using current branch as head: {head}")

        args = [
            "pr",
            "create",
            "--title",
            title,
            "--body-file",
            body_file,
            "--base",
            base,
            "--head",
            head,
        ]

        return self.run_gh(*args)

    def list_prs(self) -> dict[str, Any]:
        """List all PRs"""
        logger.info("Listing PRs")
        return self.run_gh("pr", "list")

    def get_pr_status(self, pr_number: int) -> dict[str, Any]:
        """Get PR status"""
        logger.info(f"Getting PR status for #{pr_number}")
        return self.run_gh("pr", "view", str(pr_number))

    def merge_pr(self, pr_number: int, merge_method: str = "merge") -> dict[str, Any]:
        """Merge a PR"""
        logger.info(f"Merging PR #{pr_number} with method: {merge_method}")
        return self.run_gh("pr", "merge", str(pr_number), "--" + merge_method)

    def check_conflicts(
        self,
        base: str = "develop",
        head: str = None,
    ) -> dict[str, Any]:
        """Check for merge conflicts"""
        logger.info(f"Checking conflicts: {head} -> {base}")

        if head is None:
            result = self.run_gh("branch", "--show-current")
            if not result["success"]:
                return result
            head = result["stdout"].strip()
            logger.info(f"Using current branch as head: {head}")

        return self.run_gh("pr", "check", head, "--base", base)

    def push_and_create_pr(self, config_file: str) -> dict[str, Any]:
        """Push current branch and create PR"""
        logger.info(f"Pushing branch and creating PR with config: {config_file}")

        # First push
        logger.info("Step 1: Pushing branch")
        push_result = self.run_gh("repo", "sync")
        if not push_result["success"]:
            logger.error("Failed to push branch")
            return push_result

        logger.info("Step 2: Creating PR")
        # Then create PR
        return self.create_pr_from_config(config_file)


def main():
    """Main DSL interface"""
    logger.info("GitHub DSL starting")
    dsl = GitHubDSL()

    if len(sys.argv) < 2:
        print("Usage: python gh_dsl.py <command> [args...]")
        print("Commands:")
        print("  create-pr <title> <body_file> [base] [head]")
        print("  create-pr-config <config_file>")
        print("  push-and-create-pr <config_file>")
        print("  list-prs")
        print("  check-conflicts [base] [head]")
        return

    command = sys.argv[1]
    logger.info(f"Executing command: {command}")

    if command == "create-pr":
        if len(sys.argv) < 4:
            print("Usage: create-pr <title> <body_file> [base] [head]")
            return

        title = sys.argv[2]
        body_file = sys.argv[3]
        base = sys.argv[4] if len(sys.argv) > 4 else "develop"
        head = sys.argv[5] if len(sys.argv) > 5 else None

        result = dsl.create_pr(title, body_file, base, head)
        if result["success"]:
            print("✅ PR created successfully!")
            print(result["stdout"])
        else:
            print("❌ Failed to create PR:")
            print(result["stderr"])

    elif command == "create-pr-config":
        if len(sys.argv) < 3:
            print("Usage: create-pr-config <config_file>")
            return

        config_file = sys.argv[2]
        result = dsl.create_pr_from_config(config_file)
        if result["success"]:
            print("✅ PR created successfully!")
            print(result["stdout"])
        else:
            print("❌ Failed to create PR:")
            print(result["stderr"])

    elif command == "push-and-create-pr":
        if len(sys.argv) < 3:
            print("Usage: push-and-create-pr <config_file>")
            return

        config_file = sys.argv[2]
        result = dsl.push_and_create_pr(config_file)
        if result["success"]:
            print("✅ Branch pushed and PR created successfully!")
            print(result["stdout"])
        else:
            print("❌ Failed to push and create PR:")
            print(result["stderr"])

    elif command == "list-prs":
        result = dsl.list_prs()
        if result["success"]:
            print(result["stdout"])
        else:
            print("❌ Failed to list PRs:")
            print(result["stderr"])

    elif command == "check-conflicts":
        base = sys.argv[2] if len(sys.argv) > 2 else "develop"
        head = sys.argv[3] if len(sys.argv) > 3 else None

        result = dsl.check_conflicts(base, head)
        if result["success"]:
            print("✅ No conflicts detected")
            print(result["stdout"])
        else:
            print("⚠️ Conflicts or issues detected:")
            print(result["stderr"])

    else:
        print(f"Unknown command: {command}")

    logger.info("GitHub DSL completed")


if __name__ == "__main__":
    main()

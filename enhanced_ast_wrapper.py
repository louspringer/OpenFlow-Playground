#!/usr/bin/env python3
"""
Enhanced AST Parser Wrapper - Fixes import path issues
"""

import sys
from pathlib import Path


def setup_enhanced_ast_paths():
    """Setup proper import paths for enhanced AST parser"""
    # Add scripts directory to Python path
    scripts_dir = Path(__file__).parent / "scripts"
    if scripts_dir.exists() and str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))
        print(f"✅ Added {scripts_dir} to Python path")

    # Add current directory to Python path
    current_dir = Path(__file__).parent
    if str(current_dir) not in sys.path:
        sys.path.insert(0, str(current_dir))
        print(f"✅ Added {current_dir} to Python path")


def get_enhanced_ast_linter():
    """Get the enhanced AST linter with proper imports"""
    setup_enhanced_ast_paths()

    try:
        from scripts.ast_enhanced_linter import ASTEnhancedLinter

        print("✅ Enhanced AST parser imported successfully!")
        return ASTEnhancedLinter
    except ImportError as e:
        print(f"❌ Failed to import enhanced AST parser: {e}")
        print("🔍 Trying alternative import paths...")

        try:
            # Try direct import
            from ast_enhanced_linter import ASTEnhancedLinter

            print("✅ Enhanced AST parser imported via direct path!")
            return ASTEnhancedLinter
        except ImportError as e2:
            print(f"❌ Alternative import also failed: {e2}")
            return None


if __name__ == "__main__":
    # Test the enhanced AST parser
    print("🧪 Testing Enhanced AST Parser Import")
    print("=" * 50)

    linter_class = get_enhanced_ast_linter()

    if linter_class:
        print("\n✅ Enhanced AST parser is working!")
        print("🚀 You can now use it in your reverse engineering script")

        # Test creating an instance
        try:
            linter = linter_class(".")
            print(f"✅ Created linter instance: {type(linter).__name__}")

            # Test basic functionality
            print(f"   📁 Workspace: {linter.workspace_path}")
            print(f"   🎯 File patterns: {list(linter.file_patterns.keys())}")

        except Exception as e:
            print(f"❌ Failed to create linter instance: {e}")
    else:
        print("\n❌ Enhanced AST parser is not working")
        print("🔧 Check the import paths and dependencies")

#!/usr/bin/env python3
"""
Tests for AST Analysis Domain

RM Compliance: Test the language-agnostic AST parsing capabilities
"""

import pytest
from pathlib import Path
from src.ast_analysis.api.ast_api import ASTAnalysisAPI


class TestASTAnalysis:
    """Test AST analysis capabilities"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.api = ASTAnalysisAPI()
        self.test_file = Path("src/ssh_key_management/ssh_key_manager.py")
    
    def test_api_initialization(self):
        """Test API initialization"""
        assert self.api is not None
        assert hasattr(self.api, 'analyze_file')
        assert hasattr(self.api, 'get_health_status')
    
    def test_supported_languages(self):
        """Test supported languages detection"""
        languages = self.api.get_supported_languages()
        assert "python" in languages
        assert "markdown" in languages
        assert "javascript" in languages
    
    def test_can_parse_python_file(self):
        """Test Python file parsing capability"""
        assert self.api.can_parse_file(str(self.test_file))
    
    def test_can_parse_markdown_file(self):
        """Test Markdown file parsing capability"""
        md_file = "README.md"
        assert self.api.can_parse_file(md_file)
    
    def test_can_parse_javascript_file(self):
        """Test JavaScript file parsing capability"""
        js_file = "test.js"
        assert self.api.can_parse_file(js_file)
    
    def test_cannot_parse_unknown_file(self):
        """Test unknown file type handling"""
        unknown_file = "test.xyz"
        assert not self.api.can_parse_file(unknown_file)
    
    def test_python_file_analysis(self):
        """Test Python file analysis"""
        if self.test_file.exists():
            result = self.api.analyze_python_file(str(self.test_file))
            assert result["success"] is True
            assert result["language"] == "python"
            assert "artifacts" in result
            assert "artifact_counts" in result
    
    def test_health_status(self):
        """Test health status monitoring"""
        health = self.api.get_health_status()
        assert "status" in health
        assert "supported_languages" in health
        assert isinstance(health["supported_languages"], list)
    
    def test_self_correction(self):
        """Test self-correction capabilities"""
        # Initially should be healthy
        assert self.api.self_correct() is True

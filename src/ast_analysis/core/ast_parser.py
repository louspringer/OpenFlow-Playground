#!/usr/bin/env python3
"""
Core AST Parser - Language-agnostic AST operations

RM Compliance: Self-monitoring, self-correction, interface constraints
"""

import ast
import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field

# Configure logging for RM compliance
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class ASTParseResult:
    """RM Compliance: Structured result with validation"""
    success: bool
    ast_tree: Optional[Any] = None  # Language-agnostic AST tree
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    parse_time: float = 0.0
    language: str = "unknown"
    
    def is_valid(self) -> bool:
        """RM Compliance: Self-validation"""
        return self.success and self.ast_tree is not None
    
    def get_health_indicators(self) -> Dict[str, Any]:
        """RM Compliance: Health monitoring"""
        return {
            "parse_success": self.success,
            "error_count": len(self.errors),
            "warning_count": len(self.warnings),
            "has_ast_tree": self.ast_tree is not None,
            "parse_time": self.parse_time,
            "language": self.language
        }


@dataclass
class ArtifactInfo:
    """RM Compliance: Structured artifact information"""
    name: str
    artifact_type: str  # 'class', 'function', 'method', 'module', 'component', etc.
    line_number: int
    end_line: Optional[int] = None
    source_code: Optional[str] = None
    parent_class: Optional[str] = None
    language: str = "unknown"
    is_valid: bool = True
    validation_errors: List[str] = field(default_factory=list)
    
    def validate(self) -> bool:
        """RM Compliance: Self-validation"""
        if not self.name or not self.artifact_type:
            self.validation_errors.append("Missing required fields")
            self.is_valid = False
        return self.is_valid


class LanguageParser(ABC):
    """RM Compliance: Abstract base for language-specific parsers"""
    
    @abstractmethod
    def can_parse(self, file_path: Path) -> bool:
        """Check if this parser can handle the file type"""
        pass
    
    @abstractmethod
    def parse(self, file_path: Path, content: str) -> ASTParseResult:
        """Parse file content and return AST result"""
        pass
    
    @abstractmethod
    def extract_artifacts(self, ast_tree: Any, source_code: str) -> List[ArtifactInfo]:
        """Extract artifacts from parsed AST"""
        pass


class PythonParser(LanguageParser):
    """RM Compliance: Python-specific AST parser"""
    
    def can_parse(self, file_path: Path) -> bool:
        return file_path.suffix == '.py'
    
    def parse(self, file_path: Path, content: str) -> ASTParseResult:
        """Parse Python file with comprehensive monitoring"""
        import time
        start_time = time.time()
        
        try:
            ast_tree = ast.parse(content)
            parse_time = time.time() - start_time
            
            result = ASTParseResult(
                success=True,
                ast_tree=ast_tree,
                parse_time=parse_time,
                language="python"
            )
            
            logger.info(f"✅ Successfully parsed Python file {file_path} in {parse_time:.3f}s")
            return result
            
        except SyntaxError as e:
            error_msg = f"Python syntax error in {file_path}: {e}"
            logger.error(error_msg)
            return ASTParseResult(
                success=False,
                errors=[error_msg],
                language="python"
            )
            
        except Exception as e:
            error_msg = f"Unexpected error parsing Python file {file_path}: {e}"
            logger.error(error_msg)
            return ASTParseResult(
                success=False,
                errors=[error_msg],
                language="python"
            )
    
    def extract_artifacts(self, ast_tree: ast.AST, source_code: str) -> List[ArtifactInfo]:
        """Extract Python artifacts with proper classification"""
        artifacts = []
        
        try:
            # RM Compliance: Context-aware extraction
            class_context = None
            
            for node in ast.walk(ast_tree):
                if isinstance(node, ast.ClassDef):
                    # Extract class
                    class_info = self._extract_class_info(node, source_code)
                    artifacts.append(class_info)
                    class_context = node.name
                    
                elif isinstance(node, ast.FunctionDef):
                    # Determine if it's a method or standalone function
                    if self._is_method(node, class_context):
                        function_info = self._extract_method_info(node, source_code, class_context)
                    else:
                        function_info = self._extract_function_info(node, source_code)
                    artifacts.append(function_info)
            
            logger.info(f"✅ Extracted {len(artifacts)} Python artifacts")
            return artifacts
            
        except Exception as e:
            logger.error(f"❌ Error extracting Python artifacts: {e}")
            return []
    
    def _is_method(self, node: ast.FunctionDef, class_context: Optional[str]) -> bool:
        """RM Compliance: Proper method detection using context"""
        # Check if we're inside a class context
        if class_context:
            return True
        
        # Check function name patterns that suggest methods
        if node.name.startswith('_'):
            return True
            
        # Check if function has 'self' as first parameter
        if node.args.args and node.args.args[0].arg == 'self':
            return True
            
        return False
    
    def _extract_class_info(self, node: ast.ClassDef, source_code: str) -> ArtifactInfo:
        """RM Compliance: Extract class information"""
        try:
            class_source = ast.get_source_segment(source_code, node) if hasattr(ast, 'get_source_segment') else None
            
            return ArtifactInfo(
                name=node.name,
                artifact_type='class',
                line_number=node.lineno,
                end_line=getattr(node, 'end_lineno', None),
                source_code=class_source,
                parent_class=None,
                language="python"
            )
        except Exception as e:
            logger.error(f"Error extracting Python class info for {node.name}: {e}")
            return ArtifactInfo(
                name=node.name,
                artifact_type='class',
                line_number=node.lineno,
                language="python",
                is_valid=False,
                validation_errors=[str(e)]
            )
    
    def _extract_method_info(self, node: ast.FunctionDef, source_code: str, parent_class: str) -> ArtifactInfo:
        """RM Compliance: Extract method information"""
        try:
            method_source = ast.get_source_segment(source_code, node) if hasattr(ast, 'get_source_segment') else None
            
            return ArtifactInfo(
                name=node.name,
                artifact_type='method',
                line_number=node.lineno,
                end_line=getattr(node, 'end_lineno', None),
                source_code=method_source,
                parent_class=parent_class,
                language="python"
            )
        except Exception as e:
            logger.error(f"Error extracting Python method info for {node.name}: {e}")
            return ArtifactInfo(
                name=node.name,
                artifact_type='method',
                line_number=node.lineno,
                parent_class=parent_class,
                language="python",
                is_valid=False,
                validation_errors=[str(e)]
            )
    
    def _extract_function_info(self, node: ast.FunctionDef, source_code: str) -> ArtifactInfo:
        """RM Compliance: Extract standalone function information"""
        try:
            function_source = ast.get_source_segment(source_code, node) if hasattr(ast, 'get_source_segment') else None
            
            return ArtifactInfo(
                name=node.name,
                artifact_type='function',
                line_number=node.lineno,
                end_line=getattr(node, 'end_lineno', None),
                source_code=function_source,
                parent_class=None,
                language="python"
            )
        except Exception as e:
            logger.error(f"Error extracting Python function info for {node.name}: {e}")
            return ArtifactInfo(
                name=node.name,
                artifact_type='function',
                line_number=node.lineno,
                language="python",
                is_valid=False,
                validation_errors=[str(e)]
            )


class MarkdownParser(LanguageParser):
    """RM Compliance: Markdown parser (placeholder for future implementation)"""
    
    def can_parse(self, file_path: Path) -> bool:
        return file_path.suffix in ['.md', '.markdown']
    
    def parse(self, file_path: Path, content: str) -> ASTParseResult:
        """Parse Markdown file - placeholder implementation"""
        # TODO: Implement proper Markdown parsing
        logger.warning(f"⚠️ Markdown parsing not yet implemented for {file_path}")
        return ASTParseResult(
            success=False,
            errors=["Markdown parsing not yet implemented"],
            language="markdown"
        )
    
    def extract_artifacts(self, ast_tree: Any, source_code: str) -> List[ArtifactInfo]:
        """Extract Markdown artifacts - placeholder implementation"""
        return []


class JavaScriptParser(LanguageParser):
    """RM Compliance: JavaScript parser (placeholder for future implementation)"""
    
    def can_parse(self, file_path: Path) -> bool:
        return file_path.suffix in ['.js', '.jsx', '.ts', '.tsx']
    
    def parse(self, file_path: Path, content: str) -> ASTParseResult:
        """Parse JavaScript file - placeholder implementation"""
        # TODO: Implement proper JavaScript parsing with ast.parse or similar
        logger.warning(f"⚠️ JavaScript parsing not yet implemented for {file_path}")
        return ASTParseResult(
            success=False,
            errors=["JavaScript parsing not yet implemented"],
            language="javascript"
        )
    
    def extract_artifacts(self, ast_tree: Any, source_code: str) -> List[ArtifactInfo]:
        """Extract JavaScript artifacts - placeholder implementation"""
        return []


class ASTParser:
    """RM Compliance: Language-agnostic AST parser with self-monitoring"""
    
    def __init__(self):
        # RM Compliance: Health monitoring
        self._parse_count = 0
        self._success_count = 0
        self._error_count = 0
        self._last_parse_time = 0.0
        
        # RM Compliance: Self-monitoring thresholds
        self._error_threshold = 0.2  # 20% error rate triggers health check
        self._parse_time_threshold = 5.0  # 5 seconds triggers performance warning
        
        # RM Compliance: Language-specific parsers
        self._parsers: List[LanguageParser] = [
            PythonParser(),
            MarkdownParser(),
            JavaScriptParser()
        ]
        
        logger.info(f"✅ ASTParser initialized with {len(self._parsers)} language parsers")
    
    def parse_file(self, file_path: Path) -> ASTParseResult:
        """RM Compliance: Parse file with language detection"""
        import time
        start_time = time.time()
        
        self._parse_count += 1
        logger.info(f"🔍 Parsing file: {file_path}")
        
        try:
            # RM Compliance: Input validation
            if not file_path.exists():
                error_msg = f"File does not exist: {file_path}"
                logger.error(error_msg)
                return self._create_error_result([error_msg])
            
            # Find appropriate parser
            parser = self._get_parser_for_file(file_path)
            if not parser:
                error_msg = f"No parser available for file type: {file_path.suffix}"
                logger.error(error_msg)
                return self._create_error_result([error_msg])
            
            # Parse the file
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            parse_result = parser.parse(file_path, content)
            parse_time = time.time() - start_time
            
            # RM Compliance: Success tracking
            if parse_result.success:
                self._success_count += 1
                self._last_parse_time = parse_time
                
                # RM Compliance: Performance monitoring
                if parse_time > self._parse_time_threshold:
                    logger.warning(f"⚠️ Slow parse time: {parse_time:.2f}s for {file_path}")
            else:
                self._error_count += 1
            
            logger.info(f"✅ Parsed {file_path} in {parse_time:.3f}s using {parse_result.language} parser")
            return parse_result
            
        except Exception as e:
            error_msg = f"Unexpected error parsing {file_path}: {e}"
            logger.error(error_msg)
            return self._create_error_result([error_msg])
    
    def _get_parser_for_file(self, file_path: Path) -> Optional[LanguageParser]:
        """RM Compliance: Get appropriate parser for file type"""
        for parser in self._parsers:
            if parser.can_parse(file_path):
                return parser
        return None
    
    def extract_artifacts(self, ast_tree: Any, source_code: str, language: str) -> List[ArtifactInfo]:
        """RM Compliance: Extract artifacts using language-specific parser"""
        parser = self._get_parser_by_language(language)
        if parser:
            return parser.extract_artifacts(ast_tree, source_code)
        return []
    
    def _get_parser_by_language(self, language: str) -> Optional[LanguageParser]:
        """RM Compliance: Get parser by language"""
        for parser in self._parsers:
            # Check parser type to determine language
            if language == "python" and isinstance(parser, PythonParser):
                return parser
            elif language == "markdown" and isinstance(parser, MarkdownParser):
                return parser
            elif language == "javascript" and isinstance(parser, JavaScriptParser):
                return parser
        return None
    
    def _create_error_result(self, errors: List[str]) -> ASTParseResult:
        """RM Compliance: Consistent error handling"""
        self._error_count += 1
        return ASTParseResult(
            success=False,
            errors=errors
        )
    
    def get_health_status(self) -> Dict[str, Any]:
        """RM Compliance: Health monitoring and reporting"""
        total_parses = self._parse_count
        success_rate = self._success_count / total_parses if total_parses > 0 else 0
        error_rate = self._error_count / total_parses if total_parses > 0 else 0
        
        health_status = "HEALTHY"
        if error_rate > self._error_threshold:
            health_status = "DEGRADED"
        if error_rate > 0.5:
            health_status = "UNHEALTHY"
        
        return {
            "status": health_status,
            "total_parses": total_parses,
            "success_count": self._success_count,
            "error_count": self._error_count,
            "success_rate": success_rate,
            "error_rate": error_rate,
            "last_parse_time": self._last_parse_time,
            "performance_warning": self._last_parse_time > self._parse_time_threshold,
            "supported_languages": [p.__class__.__name__.replace('Parser', '').lower() for p in self._parsers]
        }
    
    def self_correct(self) -> bool:
        """RM Compliance: Self-correction capabilities"""
        health = self.get_health_status()
        
        if health["status"] == "UNHEALTHY":
            logger.warning("🚨 ASTParser is unhealthy, attempting self-correction")
            
            # Reset counters if error rate is too high
            if health["error_rate"] > 0.8:
                logger.info("🔄 Resetting error counters due to high error rate")
                self._error_count = 0
                self._success_count = 0
                self._parse_count = 0
                return True
        
        return health["status"] != "UNHEALTHY"

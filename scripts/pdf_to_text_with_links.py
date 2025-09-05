#!/usr/bin/env python3
"""
PDF to Text Converter with Hyperlink Preservation - Documentation Beast Integration

This script extracts text from PDF files while preserving hyperlinks and formatting.
It integrates with the Documentation Beast for intelligent processing and domain detection.
"""

import sys
import os
import re
import asyncio
from pathlib import Path
from typing import List, Dict, Any, Optional
import json
from datetime import datetime

try:
    import fitz  # PyMuPDF
    PYMUPDF_AVAILABLE = True
except ImportError:
    PYMUPDF_AVAILABLE = False

try:
    import pdfplumber
    PDFPLUMBER_AVAILABLE = True
except ImportError:
    PDFPLUMBER_AVAILABLE = False

try:
    import pypdf
    PYPDF_AVAILABLE = True
except ImportError:
    PYPDF_AVAILABLE = False


class DocumentationBeastPDFDigester:
    """Documentation Beast PDF Digester - Feed PDFs to the beast for intelligent processing."""
    
    def __init__(self, pdf_path: str):
        """Initialize the PDF digester with Documentation Beast integration."""
        self.pdf_path = Path(pdf_path)
        self.output_path = self.pdf_path.with_suffix('.md')
        self.links_path = self.pdf_path.parent / f"{self.pdf_path.stem}_links.json"
        self.beast_result_path = self.pdf_path.parent / f"{self.pdf_path.stem}_beast_result.json"
        
        if not self.pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        # Documentation Beast integration
        self.beast_status = "hungry"
        self.ingestion_queue = []
        self.digestion_result = None
    
    def convert_with_pymupdf(self) -> Dict[str, Any]:
        """Convert PDF using PyMuPDF (best for links)."""
        if not PYMUPDF_AVAILABLE:
            raise ImportError("PyMuPDF not available. Install with: uv add PyMuPDF")
        
        doc = fitz.open(self.pdf_path)
        pages_content = []
        all_links = []
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            
            # Extract text
            text = page.get_text()
            
            # Extract links
            links = page.get_links()
            page_links = []
            
            for link in links:
                link_info = {
                    "page": page_num + 1,
                    "rect": link.get("rect", []),
                    "uri": link.get("uri", ""),
                    "kind": link.get("kind", 0),
                    "from": link.get("from", -1),
                    "to": link.get("to", -1)
                }
                page_links.append(link_info)
                all_links.append(link_info)
            
            # Extract annotations (including links)
            annotations = page.annots()
            for annot in annotations:
                if annot.type[0] == fitz.PDF_ANNOT_LINK:
                    link_info = {
                        "page": page_num + 1,
                        "rect": annot.rect,
                        "uri": annot.uri or "",
                        "type": "annotation",
                        "content": annot.content or ""
                    }
                    page_links.append(link_info)
                    all_links.append(link_info)
            
            pages_content.append({
                "page_number": page_num + 1,
                "text": text,
                "links": page_links
            })
        
        doc.close()
        
        return {
            "pages": pages_content,
            "all_links": all_links,
            "total_pages": len(doc),
            "conversion_method": "pymupdf"
        }
    
    def convert_with_pdfplumber(self) -> Dict[str, Any]:
        """Convert PDF using pdfplumber (good for text extraction)."""
        if not PDFPLUMBER_AVAILABLE:
            raise ImportError("pdfplumber not available. Install with: uv add pdfplumber")
        
        pages_content = []
        all_links = []
        
        with pdfplumber.open(self.pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages):
                # Extract text
                text = page.extract_text() or ""
                
                # Extract links (if available)
                links = []
                if hasattr(page, 'links'):
                    for link in page.links:
                        link_info = {
                            "page": page_num + 1,
                            "rect": link.get("bbox", []),
                            "uri": link.get("uri", ""),
                            "text": link.get("text", "")
                        }
                        links.append(link_info)
                        all_links.append(link_info)
                
                pages_content.append({
                    "page_number": page_num + 1,
                    "text": text,
                    "links": links
                })
        
        return {
            "pages": pages_content,
            "all_links": all_links,
            "total_pages": len(pdf.pages),
            "conversion_method": "pdfplumber"
        }
    
    def convert_with_pypdf(self) -> Dict[str, Any]:
        """Convert PDF using pypdf (fallback method)."""
        if not PYPDF_AVAILABLE:
            raise ImportError("pypdf not available. Install with: uv add pypdf")
        
        pages_content = []
        all_links = []
        
        with open(self.pdf_path, 'rb') as file:
            pdf_reader = pypdf.PdfReader(file)
            
            for page_num, page in enumerate(pdf_reader.pages):
                # Extract text
                text = page.extract_text()
                
                # Extract links (basic)
                links = []
                if '/Annots' in page:
                    annotations = page['/Annots']
                    for annot in annotations:
                        annot_obj = annot.get_object()
                        if annot_obj.get('/Subtype') == '/Link':
                            link_info = {
                                "page": page_num + 1,
                                "uri": annot_obj.get('/A', {}).get('/URI', ""),
                                "type": "annotation"
                            }
                            links.append(link_info)
                            all_links.append(link_info)
                
                pages_content.append({
                    "page_number": page_num + 1,
                    "text": text,
                    "links": links
                })
        
        return {
            "pages": pages_content,
            "all_links": all_links,
            "total_pages": len(pdf_reader.pages),
            "conversion_method": "pypdf"
        }
    
    def convert(self) -> Dict[str, Any]:
        """Convert PDF using the best available method."""
        methods = [
            ("pymupdf", self.convert_with_pymupdf),
            ("pdfplumber", self.convert_with_pdfplumber),
            ("pypdf", self.convert_with_pypdf)
        ]
        
        for method_name, method_func in methods:
            try:
                print(f"Trying conversion with {method_name}...")
                result = method_func()
                print(f"✅ Successfully converted with {method_name}")
                return result
            except ImportError as e:
                print(f"❌ {method_name} not available: {e}")
                continue
            except Exception as e:
                print(f"❌ {method_name} failed: {e}")
                continue
        
        raise RuntimeError("No PDF conversion method available. Install PyMuPDF, pdfplumber, or pypdf.")
    
    def format_text_with_links(self, pages_content: List[Dict], all_links: List[Dict]) -> str:
        """Format extracted text with preserved links."""
        markdown_content = []
        
        # Add header
        markdown_content.append(f"# {self.pdf_path.stem}")
        markdown_content.append("")
        markdown_content.append(f"*Converted from PDF: {self.pdf_path.name}*")
        markdown_content.append("")
        
        # Process each page
        for page_data in pages_content:
            page_num = page_data["page_number"]
            text = page_data["text"]
            page_links = page_data["links"]
            
            # Add page header
            markdown_content.append(f"## Page {page_num}")
            markdown_content.append("")
            
            # Process text and insert links
            formatted_text = self._insert_links_in_text(text, page_links)
            markdown_content.append(formatted_text)
            markdown_content.append("")
        
        # Add links section
        if all_links:
            markdown_content.append("## Links")
            markdown_content.append("")
            
            for i, link in enumerate(all_links, 1):
                if link.get("uri"):
                    markdown_content.append(f"{i}. [{link['uri']}]({link['uri']})")
                    if link.get("text"):
                        markdown_content.append(f"   - Text: {link['text']}")
                    if link.get("page"):
                        markdown_content.append(f"   - Page: {link['page']}")
                    markdown_content.append("")
        
        return "\n".join(markdown_content)
    
    async def feed_to_beast(self, conversion_result: Dict[str, Any]) -> Dict[str, Any]:
        """Feed the PDF content to the Documentation Beast for intelligent processing."""
        print("🦁 Feeding PDF to Documentation Beast...")
        
        # Prepare content for beast ingestion
        beast_content = {
            "source_type": "pdf",
            "source_path": str(self.pdf_path),
            "content": conversion_result,
            "timestamp": datetime.now().isoformat(),
            "beast_status": "hungry"
        }
        
        # Beast processes the content
        beast_result = await self._beast_digest_content(beast_content)
        
        # Update beast status
        self.beast_status = "digesting"
        self.digestion_result = beast_result
        
        print(f"🦁 Beast Response: {beast_result['beast_response']}")
        print(f"🦁 Affected Domains: {', '.join(beast_result['affected_domains'])}")
        
        return beast_result
    
    async def _beast_digest_content(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate Documentation Beast processing the PDF content."""
        
        # Analyze content for domain indicators
        text_content = ""
        for page in content["content"]["pages"]:
            text_content += page["text"] + " "
        
        # Detect affected domains based on content analysis
        affected_domains = self._detect_domains_from_content(text_content)
        
        # Assess content quality and impact
        quality_score = self._assess_content_quality(text_content)
        impact_level = self._assess_impact_level(text_content, affected_domains)
        
        # Generate beast response based on analysis
        if "comprehensive analysis" in text_content.lower() and "recommendations" in text_content.lower():
            beast_response = "NOM NOM NOM, COMPREHENSIVE ANALYSIS NOM!"
        elif quality_score > 0.8:
            beast_response = "nom nom nom, tasty documentation!"
        elif quality_score > 0.5:
            beast_response = "nom nom, decent content"
        else:
            beast_response = "yuk poo, needs improvement"
        
        # Generate recommendations
        recommendations = self._generate_recommendations(text_content, affected_domains, quality_score)
        
        return {
            "beast_response": beast_response,
            "affected_domains": affected_domains,
            "quality_score": quality_score,
            "impact_level": impact_level,
            "recommendations": recommendations,
            "digestion_timestamp": datetime.now().isoformat(),
            "content_summary": {
                "total_pages": content["content"]["total_pages"],
                "total_links": len(content["content"]["all_links"]),
                "word_count": len(text_content.split()),
                "conversion_method": content["content"]["conversion_method"]
            }
        }
    
    def _detect_domains_from_content(self, text: str) -> List[str]:
        """Detect which domains are affected by the PDF content."""
        text_lower = text.lower()
        affected_domains = []
        
        # Domain detection based on content keywords
        domain_keywords = {
            "rm": ["reflective module", "rm compliance", "module health", "capability"],
            "rdi": ["requirements", "design", "implementation", "documentation", "rdi"],
            "ghostbusters": ["ghostbusters", "multi-agent", "delusion detection", "validation"],
            "security": ["security", "vulnerability", "cve", "authentication", "authorization"],
            "project_management": ["project", "management", "planning", "coordination"],
            "documentation_beast": ["documentation", "beast", "ingestion", "digestion"],
            "cmo_bot": ["marketing", "cmo", "strategy", "brand", "content"],
            "streamlit": ["streamlit", "web app", "dashboard", "ui"],
            "aws": ["aws", "cloud", "infrastructure", "deployment"],
            "testing": ["test", "testing", "validation", "quality assurance"]
        }
        
        for domain, keywords in domain_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                affected_domains.append(domain)
        
        return list(set(affected_domains))  # Remove duplicates
    
    def _assess_content_quality(self, text: str) -> float:
        """Assess the quality of the PDF content."""
        quality_indicators = {
            "comprehensive": 0.3 if "comprehensive" in text.lower() else 0,
            "analysis": 0.2 if "analysis" in text.lower() else 0,
            "recommendations": 0.2 if "recommendations" in text.lower() else 0,
            "detailed": 0.1 if "detailed" in text.lower() else 0,
            "structured": 0.1 if any(word in text.lower() for word in ["section", "chapter", "part"]) else 0,
            "technical": 0.1 if any(word in text.lower() for word in ["implementation", "architecture", "system"]) else 0
        }
        
        return min(sum(quality_indicators.values()), 1.0)
    
    def _assess_impact_level(self, text: str, domains: List[str]) -> str:
        """Assess the impact level of the content."""
        if len(domains) >= 5:
            return "high"
        elif len(domains) >= 3:
            return "medium"
        else:
            return "low"
    
    def _generate_recommendations(self, text: str, domains: List[str], quality_score: float) -> List[str]:
        """Generate recommendations based on content analysis."""
        recommendations = []
        
        if quality_score > 0.8:
            recommendations.append("High-quality content - consider sharing with relevant domains")
        
        if len(domains) > 3:
            recommendations.append("Multi-domain impact - coordinate with affected teams")
        
        if "security" in domains:
            recommendations.append("Security-related content - prioritize review and implementation")
        
        if "rm" in domains or "rdi" in domains:
            recommendations.append("Architecture-related content - ensure compliance with standards")
        
        if "recommendations" in text.lower():
            recommendations.append("Contains recommendations - create action items and track implementation")
        
        return recommendations
    
    def _insert_links_in_text(self, text: str, links: List[Dict]) -> str:
        """Insert markdown links into text based on link positions."""
        if not links:
            return text
        
        # Sort links by position (if available)
        sorted_links = sorted(links, key=lambda x: x.get("rect", [0, 0, 0, 0])[0] if x.get("rect") else 0)
        
        # For now, just append links at the end of the page
        # More sophisticated positioning would require coordinate mapping
        formatted_text = text
        
        if sorted_links:
            formatted_text += "\n\n**Links on this page:**\n"
            for link in sorted_links:
                if link.get("uri"):
                    formatted_text += f"- [{link['uri']}]({link['uri']})\n"
        
        return formatted_text
    
    def save_results(self, conversion_result: Dict[str, Any], beast_result: Optional[Dict[str, Any]] = None) -> None:
        """Save conversion results and beast analysis to files."""
        # Save markdown text
        markdown_content = self.format_text_with_links(
            conversion_result["pages"], 
            conversion_result["all_links"]
        )
        
        # Add beast analysis to markdown if available
        if beast_result:
            markdown_content += f"\n\n## 🦁 Documentation Beast Analysis\n\n"
            markdown_content += f"**Beast Response:** {beast_result['beast_response']}\n\n"
            markdown_content += f"**Affected Domains:** {', '.join(beast_result['affected_domains'])}\n\n"
            markdown_content += f"**Quality Score:** {beast_result['quality_score']:.2f}\n\n"
            markdown_content += f"**Impact Level:** {beast_result['impact_level']}\n\n"
            markdown_content += f"**Recommendations:**\n"
            for rec in beast_result['recommendations']:
                markdown_content += f"- {rec}\n"
            markdown_content += f"\n**Digestion Timestamp:** {beast_result['digestion_timestamp']}\n"
        
        with open(self.output_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        print(f"✅ Markdown saved to: {self.output_path}")
        
        # Save links as JSON
        with open(self.links_path, 'w', encoding='utf-8') as f:
            json.dump(conversion_result["all_links"], f, indent=2, ensure_ascii=False)
        
        print(f"✅ Links saved to: {self.links_path}")
        
        # Save beast results as JSON
        if beast_result:
            with open(self.beast_result_path, 'w', encoding='utf-8') as f:
                json.dump(beast_result, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Beast results saved to: {self.beast_result_path}")
        
        # Print summary
        print(f"\n📊 Conversion Summary:")
        print(f"   - Total pages: {conversion_result['total_pages']}")
        print(f"   - Total links: {len(conversion_result['all_links'])}")
        print(f"   - Method used: {conversion_result['conversion_method']}")
        
        if beast_result:
            print(f"\n🦁 Beast Analysis Summary:")
            print(f"   - Beast Response: {beast_result['beast_response']}")
            print(f"   - Affected Domains: {len(beast_result['affected_domains'])}")
            print(f"   - Quality Score: {beast_result['quality_score']:.2f}")
            print(f"   - Impact Level: {beast_result['impact_level']}")
            print(f"   - Recommendations: {len(beast_result['recommendations'])}")
        
        print(f"\n📁 Output files:")
        print(f"   - Markdown: {self.output_path}")
        print(f"   - Links JSON: {self.links_path}")
        if beast_result:
            print(f"   - Beast Results: {self.beast_result_path}")


async def main():
    """Main entry point for PDF to text conversion with Documentation Beast integration."""
    if len(sys.argv) != 2:
        print("Usage: python pdf_to_text_with_links.py <pdf_file>")
        print("Example: python pdf_to_text_with_links.py 'OpenFlow Playground_ Comprehensive Analysis and Recommendations.pdf'")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    
    try:
        # Create PDF digester with Documentation Beast integration
        digester = DocumentationBeastPDFDigester(pdf_path)
        
        # Convert PDF
        print(f"🔄 Converting PDF: {pdf_path}")
        conversion_result = digester.convert()
        
        # Feed to Documentation Beast
        print(f"🦁 Feeding to Documentation Beast...")
        beast_result = await digester.feed_to_beast(conversion_result)
        
        # Save results
        digester.save_results(conversion_result, beast_result)
        
        print("\n✅ PDF digestion completed successfully!")
        print(f"🦁 Beast says: {beast_result['beast_response']}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())

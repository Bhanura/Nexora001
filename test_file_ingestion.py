"""
Test PDF and DOCX ingestion. 
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from rich.console import Console
from nexora001.processors.pdf_processor import process_pdf
from nexora001.processors. docx_processor import process_docx

console = Console()


def test_pdf():
    """Test PDF processing."""
    console.print("\n[bold cyan]Testing PDF Ingestion[/bold cyan]\n")
    
    # You'll need to provide a test PDF
    pdf_path = "test_document.pdf"  # Replace with actual PDF
    
    if not Path(pdf_path).exists():
        console.print("[yellow]No test PDF found.  Skipping.. .[/yellow]\n")
        return
    
    try:
        result = process_pdf(pdf_path)
        
        console.print(f"[green]✓ PDF processed successfully![/green]")
        console.print(f"  Title: {result['title']}")
        console.print(f"  Pages: {result['pages']}")
        console.print(f"  Chunks: {result['chunks_created']}\n")
        
    except Exception as e:
        console.print(f"[red]✗ Failed: {e}[/red]\n")


def test_docx():
    """Test DOCX processing."""
    console.print("\n[bold cyan]Testing DOCX Ingestion[/bold cyan]\n")
    
    # You'll need to provide a test DOCX
    docx_path = "test_document.docx"  # Replace with actual DOCX
    
    if not Path(docx_path).exists():
        console.print("[yellow]No test DOCX found. Skipping.. .[/yellow]\n")
        return
    
    try:
        result = process_docx(docx_path)
        
        console.print(f"[green]✓ DOCX processed successfully![/green]")
        console.print(f"  Title: {result['title']}")
        console.print(f"  Paragraphs: {result['paragraphs']}")
        console.print(f"  Chunks: {result['chunks_created']}\n")
        
    except Exception as e:
        console.print(f"[red]✗ Failed: {e}[/red]\n")


if __name__ == "__main__":
    test_pdf()
    test_docx()
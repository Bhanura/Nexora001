"""
Test the RAG system with sample queries.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

from nexora001.rag.pipeline import create_rag_pipeline

console = Console()


def test_rag():
    """Test RAG with sample questions."""
    console.print(Panel(
        "[bold blue]Testing RAG System[/bold blue]",
        title="🤖 RAG Test"
    ))
    
    # Create pipeline
    console.print("\n[cyan]Initializing RAG pipeline...[/cyan]")
    
    try:
        rag = create_rag_pipeline(
            embedding_provider="sentence_transformers",
            model_name="gemini-2.5-flash",
            top_k=5,
            min_similarity=0.3
        )
        
        console.print("[green]✓ Pipeline ready[/green]\n")
        
    except Exception as e:
        console.print(f"[red]✗ Failed to initialize: {e}[/red]")
        return
    
    # Test questions
    questions = [
        "What is Python?",
        "How do I contribute to Python?",
        "What is the pull request lifecycle?",
        "How do I setup Python for development?"
    ]
    
    for i, question in enumerate(questions, 1):
        console.print(f"[bold cyan]Question {i}:[/bold cyan] {question}\n")
        
        try:
            # Ask question
            result = rag.ask(question, use_history=False)
            
            answer = result['answer']
            sources = result['sources']
            found_docs = result['found_documents']
            
            # Display answer
            console.print(Panel(
                Markdown(answer),
                title=f"🤖 Answer ({found_docs} sources)",
                border_style="green"
            ))
            
            # Display sources
            if sources:
                console.print("\n[bold]Sources:[/bold]")
                for source in sources:
                    console.print(
                        f"  [{source['number']}] {source['title']} "
                        f"(score: {source['score']:.2f})"
                    )
                    console.print(f"      {source['url']}")
            
            console.print("\n" + "─" * 80 + "\n")
            
        except Exception as e:
            console.print(f"[red]✗ Error: {e}[/red]\n")
    
    console.print("[bold green]✓ RAG test completed![/bold green]\n")


if __name__ == "__main__":
    test_rag()
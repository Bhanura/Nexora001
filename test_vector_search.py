"""
Test vector search functionality.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from rich.console import Console
from rich. table import Table

from nexora001. storage.mongodb import get_storage
from nexora001.processors. embeddings import get_embedding_generator

console = Console()


def test_search(query: str):
    """Test vector search with a query."""
    console.print(f"\n[bold cyan]🔍 Query:[/bold cyan] {query}\n")
    
    try:
        # Generate query embedding
        console.print("[dim]Generating query embedding...[/dim]")
        generator = get_embedding_generator("sentence_transformers")
        query_embedding = generator.generate_embedding(query)
        
        # Search
        console.print("[dim]Searching vector database...[/dim]\n")
        with get_storage() as storage:
            results = storage.vector_search(query_embedding, limit=5, min_score=0.3)
            
            if not results:
                console.print("[yellow]No results found.[/yellow]\n")
                return
            
            console.print(f"[green]Found {len(results)} results:[/green]\n")
            
            # Display results
            for i, result in enumerate(results, 1):
                score = result.get('similarity_score', 0)
                content = result.get('content', '')[:200]
                metadata = result.get('metadata', {})
                title = metadata.get('title', 'Unknown')
                url = metadata.get('source_url', 'Unknown')
                
                console.print(f"[bold cyan]{i}.  {title}[/bold cyan]")
                console.print(f"   Score: [green]{score:.4f}[/green]")
                console.print(f"   URL: [blue]{url}[/blue]")
                console.print(f"   Content: {content}...")
                console.print()
        
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    # Test queries
    queries = [
        "What is python? ",
        "Tell me about programming languages",
        "How we can start?"
    ]
    
    for query in queries:
        test_search(query)
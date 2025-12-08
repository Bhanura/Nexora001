"""
Test script for text processing, chunking, and embeddings.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from nexora001.processors.chunker import TextChunker
from nexora001.processors.embeddings import EmbeddingGenerator, EmbeddingProvider

console = Console()


def test_chunking():
    """Test text chunking."""
    console.print(Panel(
        "[bold blue]Testing Text Chunking[/bold blue]",
        title="🔪 Chunking Test"
    ))
    
    # Sample text
    sample_text = """
    Machine learning is a subset of artificial intelligence that enables computers to learn 
    from data without being explicitly programmed. It uses algorithms to identify patterns 
    and make decisions. 
    
    There are three main types of machine learning: supervised learning, unsupervised learning, 
    and reinforcement learning.  Supervised learning uses labeled data to train models.  
    Unsupervised learning finds patterns in unlabeled data. 
    
    Deep learning is a specialized form of machine learning that uses neural networks with 
    multiple layers. It has revolutionized fields like computer vision and natural language 
    processing.  Applications include image recognition, speech recognition, and language translation.
    """
    
    console.print(f"\n[cyan]Original text:[/cyan] {len(sample_text)} characters\n")
    
    # Create chunker
    chunker = TextChunker(chunk_size=200, chunk_overlap=30)
    
    # Chunk the text
    chunks = chunker.chunk_text(sample_text, metadata={"test": True})
    
    console.print(f"[green]✓ Created {len(chunks)} chunks[/green]\n")
    
    # Display chunks
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("#", style="dim", width=3)
    table. add_column("Text", style="white", width=70)
    table.add_column("Length", justify="right", width=8)
    
    for chunk in chunks:
        table.add_row(
            str(chunk['chunk_index'] + 1),
            chunk['text'][:67] + "..." if len(chunk['text']) > 67 else chunk['text'],
            str(chunk['char_count'])
        )
    
    console.print(table)
    console.print()


def test_embeddings():
    """Test embedding generation."""
    console.print(Panel(
        "[bold blue]Testing Embedding Generation[/bold blue]",
        title="🧠 Embedding Test"
    ))
    
    try:
        # Initialize generator
        console.print("\n[cyan]Initializing embedding generator...[/cyan]")
        generator = EmbeddingGenerator(provider=EmbeddingProvider. SENTENCE_TRANSFORMERS)
        
        console.print(f"[green]✓ Generator ready[/green]")
        console.print(f"  Dimension: {generator.get_dimension()}")
        console.print(f"  Provider: {generator.provider. value}\n")
        
        # Test single embedding
        test_text = "Machine learning is a fascinating field of study."
        console.print(f"[cyan]Generating embedding for:[/cyan] \"{test_text}\"\n")
        
        embedding = generator.generate_embedding(test_text)
        
        console.print(f"[green]✓ Embedding generated[/green]")
        console.print(f"  Length: {len(embedding)}")
        console.print(f"  First 10 values: {[round(v, 4) for v in embedding[:10]]}\n")
        
        # Test batch embeddings
        test_texts = [
            "Python is a programming language.",
            "JavaScript is used for web development.",
            "Machine learning uses data to train models."
        ]
        
        console.print(f"[cyan]Generating batch embeddings for {len(test_texts)} texts.. .[/cyan]\n")
        
        embeddings = generator.generate_embeddings(test_texts)
        
        console.print(f"[green]✓ Batch embeddings generated[/green]")
        console.print(f"  Count: {len(embeddings)}")
        console.print(f"  Each dimension: {len(embeddings[0])}\n")
        
        return True
        
    except Exception as e:
        console.print(f"[red]✗ Embedding test failed: {e}[/red]\n")
        return False


def test_similarity():
    """Test vector similarity."""
    console.print(Panel(
        "[bold blue]Testing Vector Similarity[/bold blue]",
        title="🔍 Similarity Test"
    ))
    
    try:
        generator = EmbeddingGenerator(provider=EmbeddingProvider. SENTENCE_TRANSFORMERS)
        
        # Test texts
        texts = [
            "I love programming in Python",
            "Python is great for machine learning",
            "The weather is nice today",
            "JavaScript is a web language"
        ]
        
        console.print("\n[cyan]Test sentences:[/cyan]")
        for i, text in enumerate(texts, 1):
            console.print(f"  {i}. {text}")
        console.print()
        
        # Generate embeddings
        embeddings = generator.generate_embeddings(texts)
        
        # Calculate similarities
        from nexora001.storage. mongodb import MongoDBStorage
        
        query_embedding = embeddings[0]  # "I love programming in Python"
        
        console.print("[cyan]Similarities to sentence 1:[/cyan]\n")
        
        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("#", width=3)
        table.add_column("Sentence", width=50)
        table.add_column("Similarity", justify="right", width=12)
        
        for i, (text, emb) in enumerate(zip(texts, embeddings), 1):
            similarity = MongoDBStorage._cosine_similarity(query_embedding, emb)
            
            # Color code by similarity
            if similarity > 0.8:
                sim_style = "green"
            elif similarity > 0.5:
                sim_style = "yellow"
            else:
                sim_style = "red"
            
            table.add_row(
                str(i),
                text,
                f"[{sim_style}]{similarity:.4f}[/{sim_style}]"
            )
        
        console.print(table)
        console.print()
        
        return True
        
    except Exception as e:
        console.print(f"[red]✗ Similarity test failed: {e}[/red]\n")
        return False


def main():
    """Run all tests."""
    console.print("\n")
    
    # Test chunking
    test_chunking()
    
    # Test embeddings
    embeddings_ok = test_embeddings()
    
    # Test similarity (only if embeddings work)
    if embeddings_ok:
        test_similarity()
    
    console.print("[bold green]✓ All tests completed![/bold green]\n")


if __name__ == "__main__":
    main()
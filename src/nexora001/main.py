"""
Nexora001 - Main Console Application Entry Point

This is the interactive console interface for the Nexora001 system.
"""

import sys
from pathlib import Path
from rich.console import Console
from rich. panel import Panel
from rich.prompt import Prompt, Confirm
from rich.markdown import Markdown
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from nexora001. config import settings, print_config_status
from nexora001.storage.mongodb import get_storage
from nexora001. crawler.manager import crawl_website
from nexora001.rag.pipeline import create_rag_pipeline

console = Console()

# Global RAG pipeline (initialized on first use)
_rag_pipeline = None

def print_banner():
    """Display the application banner."""
    banner = """
    ███╗   ██╗███████╗██╗  ██╗ ██████╗ ██████╗  █████╗     ██████╗  ██████╗ ██╗
    ████╗  ██║██╔════╝╚██╗██╔╝██╔═══██╗██╔══██╗██╔══██╗   ██╔═████╗██╔═████╗███║
    ██╔██╗ ██║█████╗   ╚███╔╝ ██║   ██║██████╔╝███████║   ██║██╔██║██║██╔██║╚██║
    ██║╚██╗██║██╔══╝   ██╔██╗ ██║   ██║██╔══██╗██╔══██║   ████╔╝██║████╔╝██║ ██║
    ██║ ╚████║███████╗██╔╝ ██╗╚██████╔╝██║  ██║██║  ██║   ╚██████╔╝╚██████╔╝ ██║
    ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝    ╚═════╝  ╚═════╝  ╚═╝
                                                                             
           AI-Powered Knowledge Base Chatbot with RAG
    """
    console.print(Panel(banner, style="bold blue"))


def print_help():
    """Display available commands."""
    help_text = """
## Available Commands

| Command | Description |
|---------|-------------|
| `crawl <url>` | Crawl a website and index its content |
| `ingest <file>` | Ingest a PDF or document file |
| `ask <question>` | Ask a question about indexed content |
| `history` | Show conversation history |
| `clear-history` | Clear conversation history |
| `list` | List all indexed documents |
| `stats` | Show database statistics |
| `delete <url>` | Delete documents from a specific URL |
| `status` | View system and database status |
| `config` | View current configuration |
| `clear` | Clear the console screen |
| `help` | Show this help message |
| `exit` | Exit the application |

## Examples

    """
    console.print(Markdown(help_text))

def main():
    """Main application entry point."""
    print_banner()
    
    console.print("[bold green]Welcome to Nexora001![/bold green]")
    console.print("Type 'help' for available commands, 'exit' to quit.\n")
    
    # Check configuration on startup
    if not settings.is_configured:
        console.print("[yellow]⚠️  Warning: Some configuration is missing![/yellow]")
        console.print("Run 'config' to see current settings.\n")
    else:
        # Show quick tips
        console.print("[dim]💡 Quick tips:[/dim]")
        console.print("[dim]  • Use 'crawl <url>' to index a website[/dim]")
        console.print("[dim]  • Use 'ask <question>' to query your knowledge base[/dim]")
        console.print("[dim]  • Use 'status' to see what's indexed[/dim]\n")

def get_rag_pipeline():
    """Get or create RAG pipeline."""
    global _rag_pipeline
    
    if _rag_pipeline is None:
        console.print("[dim]Initializing AI system.. .[/dim]")
        try:
            _rag_pipeline = create_rag_pipeline(
                embedding_provider="sentence_transformers",
                model_name="gemini-2.5-flash",
                top_k=5,
                min_similarity=0.3
            )
            console.print("[dim]✓ AI ready[/dim]\n")
        except Exception as e:
            console.print(f"[red]Failed to initialize AI: {e}[/red]\n")
            return None
    
    return _rag_pipeline


def handle_crawl(args: str) -> bool:
    """Handle the crawl command."""
    if not args:
        console.print("[red]Error: Please provide a URL to crawl[/red]")
        console.print("Example: crawl https://example.com")
        console.print("         crawl https://python.org --depth 2")
        return True
    
    # Parse arguments
    parts = args.split()
    url = parts[0]
    
    # Parse options
    max_depth = 2
    follow_links = True
    
    for i, part in enumerate(parts[1:]):
        if part in ['--depth', '-d'] and i + 1 < len(parts[1:]):
            try:
                max_depth = int(parts[i + 2])
            except (ValueError, IndexError):
                pass
        elif part in ['--no-follow', '-n']:
            follow_links = False
    
    # Validate URL
    if not url.startswith(('http://', 'https://')):
        console.print("[red]Error: URL must start with http:// or https://[/red]")
        return True
    
    # Confirm crawl
    console.print(f"\n[cyan]Crawl Configuration:[/cyan]")
    console.print(f"  URL: {url}")
    console.print(f"  Max depth: {max_depth}")
    console. print(f"  Follow links: {follow_links}")
    
    if not Confirm.ask("\nStart crawling? ", default=True):
        console.print("[yellow]Crawl cancelled[/yellow]")
        return True
    
    # Start crawling
    console.print(f"\n[cyan]🕷️  Starting crawler...[/cyan]\n")
    
    try:
        result = crawl_website(url, max_depth=max_depth, follow_links=follow_links)
        console.print(f"\n[green]✅ Crawl completed successfully![/green]")
        
    except KeyboardInterrupt:
        console. print(f"\n[yellow]⚠️  Crawl interrupted by user[/yellow]")
    except Exception as e:
        console.print(f"\n[red]❌ Crawl failed: {e}[/red]")
        if settings.debug:
            console.print_exception()
    
    return True


def handle_list() -> bool:
    """Handle the list command."""
    console.print("\n[cyan]📄 Indexed Documents[/cyan]")
    console.print("─" * 80)
    
    try:
        with get_storage() as storage:
            documents = storage.get_all_documents(limit=20)
            
            if not documents:
                console.print("[yellow]No documents found.  Use 'crawl' to add content.[/yellow]\n")
                return True
            
            table = Table(show_header=True, header_style="bold cyan")
            table.add_column("#", style="dim", width=4)
            table.add_column("Title", style="cyan", width=40)
            table.add_column("URL", style="blue", width=50)
            table.add_column("Type", width=8)
            table.add_column("Length", justify="right", width=10)
            
            for i, doc in enumerate(documents, 1):
                metadata = doc.get('metadata', {})
                title = metadata.get('title', 'Untitled')[:38]
                url = metadata.get('source_url', 'Unknown')[:48]
                source_type = metadata.get('source_type', 'unknown')
                content_len = len(doc.get('content', ''))
                
                table.add_row(
                    str(i),
                    title,
                    url,
                    source_type,
                    f"{content_len:,}"
                )
            
            console.print(table)
            console.print(f"\n[dim]Showing {len(documents)} documents[/dim]\n")
            
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]\n")
    
    return True


def handle_stats() -> bool:
    """Handle the stats command."""
    console. print("\n[cyan]📊 Database Statistics[/cyan]")
    console.print("─" * 40)
    
    try:
        with get_storage() as storage:
            total_docs = storage.count_documents()
            web_docs = storage.count_documents("web")
            pdf_docs = storage.count_documents("pdf")
            
            stats_table = Table(show_header=False)
            stats_table.add_column("Metric", style="cyan")
            stats_table.add_column("Value", style="green", justify="right")
            
            stats_table.add_row("Total Documents", str(total_docs))
            stats_table. add_row("Web Pages", str(web_docs))
            stats_table.add_row("PDF Documents", str(pdf_docs))
            stats_table.add_row("Database", storage.database_name)
            
            console.print(stats_table)
            console.print()
            
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]\n")
    
    return True


def handle_delete(args: str) -> bool:
    """Handle the delete command."""
    if not args:
        console.print("[red]Error: Please provide a URL to delete[/red]")
        console.print("Example: delete https://example.com")
        return True
    
    url = args.strip()
    
    # Confirm deletion
    if not Confirm. ask(f"\n[yellow]Delete all documents from {url}?[/yellow]", default=False):
        console.print("[yellow]Deletion cancelled[/yellow]")
        return True
    
    try:
        with get_storage() as storage:
            deleted_count = storage.delete_by_url(url)
            
            if deleted_count > 0:
                console.print(f"[green]✅ Deleted {deleted_count} document(s)[/green]\n")
            else:
                console.print(f"[yellow]No documents found for URL: {url}[/yellow]\n")
                
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]\n")
    
    return True


def handle_command(command: str) -> bool:
    """
    Process a user command.
    
    Returns:
        bool: True to continue, False to exit
    """
    command = command.strip()
    
    if not command:
        return True
    
    parts = command.split(maxsplit=1)
    cmd = parts[0].lower()
    args = parts[1] if len(parts) > 1 else ""
    
    if cmd == "exit" or cmd == "quit":
        console.print("\n[yellow]Goodbye!  👋[/yellow]\n")
        return False
    
    elif cmd == "help":
        print_help()
    
    elif cmd == "config":
        print_config_status()
    
    elif cmd == "clear":
        console.clear()
        print_banner()
    
    elif cmd == "status":
        console.print("\n[cyan]System Status[/cyan]")
        console.print("─" * 40)
        
        if settings.is_configured:
            console.print("✅ Configuration: Complete")
            
            try:
                with get_storage() as storage:
                    doc_count = storage.count_documents()
                    console.print(f"📊 Indexed Documents: {doc_count}")
                    console.print(f"🔗 Database: Connected ({storage.database_name})")
            except Exception as e:
                console.print(f"🔗 Database: [red]Error - {e}[/red]")
        else:
            console. print("❌ Configuration: Incomplete")
            console.print("   Run 'config' to see what's missing")
        console.print()
    
    elif cmd == "crawl":
        return handle_crawl(args)
    
    elif cmd == "list":
        return handle_list()
    
    elif cmd == "stats":
        return handle_stats()
    
    elif cmd == "delete":
        return handle_delete(args)
    
    elif cmd == "ingest":
        if not args:
            console.print("[red]Error: Please provide a file path[/red]")
            console.print("Example: ingest document.pdf")
        else:
            console.print(f"\n[cyan]📄 Ingesting: {args}[/cyan]")
            console.print("[yellow]⚠️  Ingestion not yet implemented - Coming in next step![/yellow]\n")
    
    elif cmd == "ask":
        if not args:
            console.print("[red]Error: Please provide a question[/red]")
            console.print("Example: ask What is machine learning?")
        else:
            console.print(f"\n[cyan]🤔 Question:[/cyan] {args}\n")
            
            # Get RAG pipeline
            rag = get_rag_pipeline()
            if not rag:
                return True
            
            try:
                # Ask question
                with console.status("[bold cyan]Thinking.. .", spinner="dots"):
                    result = rag.ask(args, use_history=True)
       
                answer = result['answer']
                sources = result['sources']
                found_docs = result['found_documents']
                
                # Display answer
                from rich.markdown import Markdown
                console.print(Panel(
                    Markdown(answer),
                    title=f"🤖 Answer (from {found_docs} sources)",
                    border_style="green"
                ))
                
                # Display sources
                if sources:
                    console.print("\n[bold]📚 Sources:[/bold]")
                    for source in sources:
                        console.print(
                            f"  [{source['number']}] {source['title']} "
                            f"(relevance: {source['score']:.0%})"
                        )
                        console.print(f"      [blue]{source['url']}[/blue]")
                
                console.print()
                
            except Exception as e:
                console.print(f"[red]Error: {e}[/red]\n")
                if settings.debug:
                    console.print_exception()

    elif cmd == "history":
        """Show conversation history."""
        rag = get_rag_pipeline()
        if not rag:
            return True
        
        history = rag.get_history()
        
        if not history:
            console.print("[yellow]No conversation history yet.[/yellow]\n")
            return True
        
        console.print("\n[cyan]📜 Conversation History[/cyan]")
        console.print("─" * 60)
        
        for i, msg in enumerate(history, 1):
            role = msg['role']
            content = msg['content'][:100] + "..." if len(msg['content']) > 100 else msg['content']
            
            if role == "user":
                console.print(f"\n[bold cyan]You:[/bold cyan] {content}")
            else:
                console. print(f"[bold green]AI:[/bold green] {content}")
        
        console.print()
    
    elif cmd == "clear-history":
        """Clear conversation history."""
        rag = get_rag_pipeline()
        if not rag:
            return True
        
        rag.clear_history()
        console.print("[green]✓ Conversation history cleared[/green]\n")

    else:
        console.print(f"[red]Unknown command: {cmd}[/red]")
        console.print("Type 'help' for available commands.")
    
    return True


def main():
    """Main application entry point."""
    print_banner()
    
    console.print("[bold green]Welcome to Nexora001![/bold green]")
    console.print("Type 'help' for available commands, 'exit' to quit.\n")
    
    # Check configuration on startup
    if not settings.is_configured:
        console.print("[yellow]⚠️  Warning: Some configuration is missing![/yellow]")
        console.print("Run 'config' to see current settings.\n")
    
    # Main command loop
    running = True
    while running:
        try:
            command = Prompt.ask("[bold cyan]nexora001[/bold cyan]")
            running = handle_command(command)
        except KeyboardInterrupt:
            console.print("\n[yellow]Use 'exit' to quit[/yellow]")
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            if settings.debug:
                console.print_exception()


if __name__ == "__main__":
    main()
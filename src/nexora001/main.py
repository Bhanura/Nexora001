"""
Nexora001 - Main Console Application Entry Point

This is the interactive console interface for the Nexora001 system. 
"""

import sys
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.markdown import Markdown

from nexora001. config import settings, print_config_status

console = Console()


def print_banner():
    """Display the application banner."""
    banner = """
    ███╗   ██╗███████╗██╗  ██╗ ██████╗ ██████╗  █████╗  ██████╗  ██████╗ ██╗
    ████╗  ██║██╔════╝╚██╗██╔╝██╔═══██╗██╔══██╗██╔══██╗██╔═████╗██╔═████╗███║
    ██╔██╗ ██║█████╗   ╚███╔╝ ██║   ██║██████╔╝███████║██║██╔██║██║██╔██║╚██║
    ██║╚██╗██║██╔══╝   ██╔██╗ ██║   ██║██╔══██╗██╔══██║████╔╝██║████╔╝██║ ██║
    ██║ ╚████║███████╗██╔╝ ██╗╚██████╔╝██║  ██║██║  ██║╚██████╔╝╚██████╔╝ ██║
    ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚═╝
                                                                             
           AI-Powered Knowledge Base Chatbot with RAG
    """
    console. print(Panel(banner, style="bold blue"))


def print_help():
    """Display available commands."""
    help_text = """
## Available Commands

| Command | Description |
|---------|-------------|
| `crawl <url>` | Crawl a website and index its content |
| `ingest <file>` | Ingest a PDF or document file |
| `ask <question>` | Ask a question about indexed content |
| `status` | View system and database status |
| `config` | View current configuration |
| `clear` | Clear the console screen |
| `help` | Show this help message |
| `exit` | Exit the application |

## Examples

    """
    console. print(Markdown(help_text))


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
    cmd = parts[0]. lower()
    args = parts[1] if len(parts) > 1 else ""
    
    if cmd == "exit" or cmd == "quit":
        console. print("\n[yellow]Goodbye!  👋[/yellow]\n")
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
        console. print("─" * 40)
        
        if settings.is_configured:
            console. print("✅ Configuration: Complete")
            # TODO: Add database connection check
            # TODO: Add indexed documents count
            console.print("📊 Indexed Documents: [yellow]Not yet implemented[/yellow]")
            console.print("🔗 Database: [yellow]Not yet connected[/yellow]")
        else:
            console.print("❌ Configuration: Incomplete")
            console.print("   Run 'config' to see what's missing")
        console.print()
    
    elif cmd == "crawl":
        if not args:
            console.print("[red]Error: Please provide a URL to crawl[/red]")
            console.print("Example: crawl https://example. com")
        else:
            console.print(f"\n[cyan]🕷️  Crawling: {args}[/cyan]")
            console.print("[yellow]⚠️  Crawling not yet implemented - Coming in next step![/yellow]\n")
    
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
            console.print(f"\n[cyan]🤔 Question: {args}[/cyan]")
            console.print("[yellow]⚠️  RAG query not yet implemented - Coming in next step![/yellow]\n")
    
    else:
        console. print(f"[red]Unknown command: {cmd}[/red]")
        console. print("Type 'help' for available commands.")
    
    return True


def main():
    """Main application entry point."""
    print_banner()
    
    console.print("[bold green]Welcome to Nexora001![/bold green]")
    console.print("Type 'help' for available commands, 'exit' to quit.\n")
    
    # Check configuration on startup
    if not settings.is_configured:
        console.print("[yellow]⚠️  Warning: Some configuration is missing![/yellow]")
        console. print("Run 'config' to see current settings.\n")
    
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
"""
Nexora002 - Main Console Application Entry Point

This is the interactive console interface for the Nexora002 system.
"""

import sys
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.markdown import Markdown
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
import hashlib

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from nexora001.config import settings, print_config_status
from nexora001.storage.mongodb import get_storage
from nexora001.crawler.manager import crawl_website
from nexora001.rag.pipeline import create_rag_pipeline

console = Console()

# --- SESSION STATE ---
# This simulates the "Logged In" user
CURRENT_USER = None
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
                                                                             
           AI-Powered Knowledge Base Chatbot with RAG -- Multi-Tenant SaaS Edition
    """
    console.print(Panel(banner, style="bold Purple"))


def get_rag_pipeline():
    """Get or create RAG pipeline."""
    global _rag_pipeline
    if _rag_pipeline is None:
        console.print("[dim]Initializing AI Engine...[/dim]")
        try:
            # Note: We don't pass client_id here anymore, we pass it during 'ask'
            _rag_pipeline = create_rag_pipeline(
                embedding_provider="sentence_transformers",
                model_name="gemini-2.5-flash"
            )
        except Exception as e:
            console.print(f"[red]AI Init Failed: {e}[/red]")
            return None
    return _rag_pipeline

# ==========================================
# AUTH COMMANDS
# ==========================================

def handle_register():
    console.print("\n[cyan]📝 Create New Client Account[/cyan]")
    email = Prompt.ask("Email")
    password = Prompt.ask("Password", password=True)
    name = Prompt.ask("Company/Name")
    
    # Simple hash for demo (Use bcrypt in production!)
    pass_hash = hashlib.sha256(password.encode()).hexdigest()
    
    try:
        with get_storage() as storage:
            user_id = storage.create_user(email, pass_hash, name=name)
            console.print(f"[green]✅ Account created! ID: {user_id}[/green]")
            console.print("Please login now.")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

def handle_login():
    global CURRENT_USER
    console.print("\n[cyan]🔐 Login[/cyan]")
    email = Prompt.ask("Email")
    password = Prompt.ask("Password", password=True)
    pass_hash = hashlib.sha256(password.encode()).hexdigest()
    
    with get_storage() as storage:
        # Find user
        user = storage.users.find_one({"email": email, "password_hash": pass_hash})
        
        if user:
            CURRENT_USER = user
            CURRENT_USER["_id"] = str(user["_id"]) # Convert ObjectId to string
            console.print(f"\n[green]👋 Welcome back, {user.get('name')}![/green]")
            console.print(f"[dim]Client ID: {CURRENT_USER['_id']}[/dim]\n")
        else:
            console.print("[red]❌ Invalid credentials[/red]\n")

def handle_whoami():
    if CURRENT_USER:
        console.print(Panel(
            f"User: {CURRENT_USER['name']}\nEmail: {CURRENT_USER['email']}\nRole: {CURRENT_USER['role']}\nID: {CURRENT_USER['_id']}",
            title="👤 Current Session",
            border_style="green"
        ))
    else:
        console.print("[yellow]🕵️  You are currently: GUEST (Not logged in)[/yellow]")

# ==========================================
# CORE COMMANDS (UPDATED)
# ==========================================

def handle_list():
    if not CURRENT_USER:
        console.print("[red]⛔ Access Denied: Please 'login' first.[/red]")
        return True

    console.print(f"\n[cyan]📄 Documents for {CURRENT_USER['name']}[/cyan]")
    console.print("─" * 80)
    
    try:
        with get_storage() as storage:
            # Fetch ONLY this client's documents
            # Note: We use .find() directly here for simplicity
            cursor = storage.documents.find(
                {"client_id": CURRENT_USER['_id']},
                {"metadata": 1, "content": 1}
            ).limit(20)
            
            documents = list(cursor)
            
            if not documents:
                console.print("[yellow]No documents found. Use 'crawl' to add content.[/yellow]\n")
                return True
            
            table = Table(show_header=True, header_style="bold cyan")
            table.add_column("#", style="dim", width=4)
            table.add_column("Title", style="cyan", width=40)
            table.add_column("URL", style="blue", width=50)
            table.add_column("Size", justify="right", width=10)
            
            for i, doc in enumerate(documents, 1):
                meta = doc.get('metadata', {})
                content_len = len(doc.get('content', ''))
                
                table.add_row(
                    str(i),
                    meta.get('title', 'Untitled')[:38],
                    meta.get('source_url', 'Unknown')[:48],
                    f"{content_len:,} ch"
                )
            
            console.print(table)
            console.print(f"\n[dim]Showing {len(documents)} documents[/dim]\n")
            
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]\n")
    return True

def handle_crawl(args: str):
    if not CURRENT_USER:
        console.print("[red]⛔ Access Denied: Please 'login' first.[/red]")
        return True

    if not args:
        console.print("[red]Usage: crawl <url> [--depth N] [--playwright][/red]")
        return True

    # Parse arguments
    parts = args.split()
    url = parts[0]
    
    # Parse --depth flag
    max_depth = 2  # Default
    if '--depth' in parts:
        try:
            depth_idx = parts.index('--depth')
            if depth_idx + 1 < len(parts):
                max_depth = int(parts[depth_idx + 1])
        except (ValueError, IndexError):
            console.print("[yellow]⚠️  Invalid depth, using default: 2[/yellow]")
    
    # Parse --playwright flag
    use_playwright = '--playwright' in parts
    
    # PASS CLIENT_ID TO CRAWLER
    try:
        mode = "Playwright (JS)" if use_playwright else "Standard"
        console.print(f"\n[cyan]🕷️  Crawling for client: {CURRENT_USER['name']} (depth: {max_depth}, mode: {mode})...[/cyan]")
        crawl_website(
            url=url,
            client_id=CURRENT_USER['_id'],
            max_depth=max_depth,
            follow_links=True,
            use_playwright=use_playwright
        )
        console.print("[green]✅ Crawl complete and data isolated.[/green]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
    return True

def handle_ask(args: str):
    if not CURRENT_USER:
        console.print("[red]⛔ Access Denied: Please 'login' first.[/red]")
        return True
    
    if not args:
        console.print("[red]Usage: ask <question>[/red]")
        return True

    rag = get_rag_pipeline()
    if not rag: return True

    console_session_id = f"session-session-{CURRENT_USER['_id']}"

    console.print(f"\n[cyan]🤔 Searching knowledge base for {CURRENT_USER['name']}...[/cyan]")
    
    try:
        # PASS CLIENT_ID TO RAG
        result = rag.ask(
            query=args, 
            client_id=CURRENT_USER['_id'],
            session_id=console_session_id,
            use_history=True
        )
        
        console.print(Panel(Markdown(result['answer']), title="🤖 Nexora AI"))
        
        if result.get('sources'):
            console.print("\n[dim]📚 Sources (Authenticated Access Only):[/dim]")
            for src in result['sources']:
                console.print(f" - {src['url']} ({src['score']:.0%})")
                
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
    return True

def handle_apikey():
    """Generate API Key for the current user."""
    if not CURRENT_USER:
        console.print("[red]⛔ Please login first.[/red]")
        return True

    if CURRENT_USER['role'] != 'client_admin':
        console.print("[red]⛔ Only Client Admins can generate keys.[/red]")
        return True

    try:
        with get_storage() as storage:
            key = storage.generate_api_key(client_id=CURRENT_USER['_id'])
            console.print("\n[green]🔑 API Key Generated:[/green]")
            console.print(Panel(key, style="bold yellow"))
            console.print("[dim]Use this in your frontend widget integration.[/dim]\n")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
    return True

# ==========================================
# MAIN LOOP
# ==========================================

def print_help():
    help_text = """
## Authentication
| Command | Description |
|---------|-------------|
| `register` | Create a new Client Admin account |
| `login` | Log in to an account |
| `whoami` | Show current user |
| `apikey` | Generate widget key (Client Admin only) |

## Knowledge Base
| Command | Description |
|---------|-------------|
| `crawl <url>` | Crawl website (Saved to YOUR account) |
| `ask <msg>` | Ask question (Searches YOUR data only) |
| `list` | List your documents |
| `exit` | Quit |
    """
    console.print(Markdown(help_text))

def handle_command(command: str) -> bool:
    command = command.strip()
    if not command: return True
    
    parts = command.split(maxsplit=1)
    cmd = parts[0].lower()
    args = parts[1] if len(parts) > 1 else ""

    if cmd == "exit": return False
    elif cmd == "help": print_help()
    elif cmd == "clear": console.clear(); print_banner()
    
    # Auth Commands
    elif cmd == "register": handle_register()
    elif cmd == "login": handle_login()
    elif cmd == "whoami": handle_whoami()
    elif cmd == "apikey": handle_apikey()
    
    # Core Commands
    elif cmd == "crawl": handle_crawl(args)
    elif cmd == "ask": handle_ask(args)
    elif cmd == "list": handle_list()
    # Add handlers for list/delete similarly...
    
    else:
        console.print(f"[red]Unknown command. Try 'help'.[/red]")
    
    return True

def main():
    print_banner()
    console.print("[yellow]⚠️  System Mode: Multi-Tenant SaaS Simulation[/yellow]")
    console.print("Please `register` or `login` to begin.\n")
    
    running = True
    while running:
        try:
            # Change prompt color based on login status
            prompt_str = f"[bold green]{CURRENT_USER['name']}[/bold green]" if CURRENT_USER else "[bold red]Guest[/bold red]"
            command = Prompt.ask(f"{prompt_str}@nexora")
            running = handle_command(command)
        except KeyboardInterrupt:
            console.print("\n[yellow]Goodbye![/yellow]")
            break
        except Exception as e:
            console.print(f"[red]System Error: {e}[/red]")

if __name__ == "__main__":
    main()
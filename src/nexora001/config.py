"""
Configuration management for Nexora001. 
Loads settings from environment variables with validation.
"""

import os
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field, field_validator
from dotenv import load_dotenv

# Load . env file from project root
PROJECT_ROOT = Path(__file__).parent. parent.parent
ENV_FILE = PROJECT_ROOT / ".env"

load_dotenv(ENV_FILE)


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # MongoDB Configuration
    mongodb_uri: str = Field(
        default="",
        description="MongoDB Atlas connection string"
    )
    mongodb_database: str = Field(
        default="nexora001",
        description="MongoDB database name"
    )
    
    # Google AI Configuration
    google_api_key: str = Field(
        default="",
        description="Google Gemini API key"
    )
    
    # Application Configuration
    debug: bool = Field(default=True)
    log_level: str = Field(default="INFO")
    environment: str = Field(default="development")
    
    # Crawling Configuration
    crawl_delay: float = Field(default=1.0)
    max_crawl_depth: int = Field(default=2)
    user_agent: str = Field(default="Nexora001-Bot/1.0")
    respect_robots_txt: bool = Field(default=True)
    
    # API Configuration
    api_host: str = Field(default="0.0. 0.0")
    api_port: int = Field(default=8000)
    
    @field_validator("mongodb_uri", "google_api_key")
    @classmethod
    def check_not_empty(cls, v: str, info) -> str:
        """Warn if critical configs are empty."""
        if not v or v.startswith("your_") or "<" in v:
            print(f"⚠️  Warning: {info.field_name} is not configured!")
        return v
    
    @property
    def is_configured(self) -> bool:
        """Check if all required settings are configured."""
        return (
            bool(self.mongodb_uri) and 
            not self.mongodb_uri.startswith("mongodb+srv://<") and
            bool(self.google_api_key) and 
            not self.google_api_key.startswith("your_")
        )
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings()


def print_config_status():
    """Print configuration status for debugging."""
    from rich.console import Console
    from rich.table import Table
    
    console = Console()
    
    table = Table(title="Nexora001 Configuration Status")
    table. add_column("Setting", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Value", style="yellow")
    
    # MongoDB
    mongo_status = "✅ Configured" if settings. mongodb_uri and "<" not in settings. mongodb_uri else "❌ Not Set"
    mongo_value = settings.mongodb_uri[:30] + "..." if len(settings.mongodb_uri) > 30 else settings. mongodb_uri
    table.add_row("MongoDB URI", mongo_status, mongo_value if "✅" in mongo_status else "Not configured")
    
    table.add_row("MongoDB Database", "✅ Set", settings.mongodb_database)
    
    # Google API
    google_status = "✅ Configured" if settings.google_api_key and not settings.google_api_key.startswith("your_") else "❌ Not Set"
    table.add_row("Google API Key", google_status, "***hidden***" if "✅" in google_status else "Not configured")
    
    # Other settings
    table. add_row("Environment", "✅ Set", settings.environment)
    table. add_row("Debug Mode", "✅ Set", str(settings.debug))
    table.add_row("Log Level", "✅ Set", settings.log_level)
    
    console.print(table)
    
    if not settings.is_configured:
        console.print("\n[bold red]⚠️  Some required settings are missing![/bold red]")
        console.print("Please update your .env file with valid values.\n")
    else:
        console.print("\n[bold green]✅ All required settings configured![/bold green]\n")


if __name__ == "__main__":
    print_config_status()
"""
Command-line interface for OpenAI App.
"""
import asyncio
import sys
import click

from ..services import app_service
from ..config.settings import settings


@click.group()
@click.version_option(version="0.1.0", prog_name="OpenAI App")
def cli():
    """OpenAI App - Professional AI Assistant."""
    pass


@cli.command()
@click.argument('query', nargs=-1)
@click.option('--type', 'query_type', 
              type=click.Choice(['auto', 'weather', 'general']), 
              default='auto',
              help='Type of query to run')
def ask(query, query_type):
    """Ask a question to the AI assistant."""
    if not query:
        click.echo("❌ Please provide a question!")
        return
    
    query_text = " ".join(query)
    
    async def run_query():
        try:
            response = await app_service.run_single_query(query_text, query_type)
            click.echo(f"\n🤖 {response}")
        except Exception as e:
            click.echo(f"❌ Error: {str(e)}")
    
    asyncio.run(run_query())


@cli.command()
def chat():
    """Start an interactive chat session."""
    async def run_chat():
        await app_service.run_interactive_session()
    
    asyncio.run(run_chat())


@cli.command()
def info():
    """Show application information."""
    app_info = app_service.get_app_info()
    
    click.echo("📱 OpenAI App Information:")
    click.echo(f"• Version: {app_info['version']}")
    click.echo(f"• Environment: {app_info['environment']}")
    click.echo(f"• Model: {app_info['model']}")
    click.echo(f"• Debug Mode: {app_info['debug']}")
    click.echo(f"• Initialized: {app_info['initialized']}")
    
    if app_info['stats']['total_conversations'] > 0:
        stats = app_info['stats']
        click.echo(f"\n📊 Usage Statistics:")
        click.echo(f"• Total conversations: {stats['total_conversations']}")
        click.echo(f"• Weather queries: {stats['weather_queries']}")
        click.echo(f"• General queries: {stats['general_queries']}")


@cli.command()
def config():
    """Show current configuration."""
    click.echo("⚙️  Current Configuration:")
    click.echo(f"• Gemini Model: {settings.gemini_model}")
    click.echo(f"• Log Level: {settings.log_level}")
    click.echo(f"• Environment: {settings.environment}")
    click.echo(f"• Debug Mode: {settings.debug}")
    click.echo(f"• Tracing: {'Enabled' if settings.tracing_enabled else 'Disabled'}")
    click.echo(f"• API Key: {'Configured' if settings.gemini_api_key else 'Not configured'}")


@cli.command()
@click.argument('city')
def weather(city):
    """Get weather information for a city."""
    async def get_weather():
        try:
            query = f"What's the weather like in {city}?"
            response = await app_service.run_single_query(query, "weather")
            click.echo(f"\n🌤️  {response}")
        except Exception as e:
            click.echo(f"❌ Error: {str(e)}")
    
    asyncio.run(get_weather())


def main():
    """Main CLI entry point."""
    cli()


if __name__ == "__main__":
    main()

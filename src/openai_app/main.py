"""
Main application entry point.
Professional OpenAI App using modern architecture.
"""
import asyncio
import sys
from typing import Optional

from .services import app_service
from .config.logging import get_logger

logger = get_logger(__name__)


async def main_async():
    """Main async function."""
    try:
        # Check for help flag
        if "--help" in sys.argv or "-h" in sys.argv:
            print("""
🤖 OpenAI App - Professional AI Assistant

Usage:
  openai-app [OPTIONS] [QUERY]

Arguments:
  QUERY                     Ask a question to the AI assistant

Options:
  -v, --verbose            Show detailed logging information
  -q, --quiet              Show minimal output
  -h, --help               Show this help message

Examples:
  openai-app "What's the weather in London?"
  openai-app --verbose "Tell me about AI"
  openai-app                              (Interactive mode)

For more advanced features, use the CLI commands:
  python -m src.openai_app.cli.commands --help
            """)
            return
        
        # Check for verbose flag
        verbose = "--verbose" in sys.argv or "-v" in sys.argv
        quiet = "--quiet" in sys.argv or "-q" in sys.argv
        
        # Remove flags from arguments
        args = [arg for arg in sys.argv[1:] if arg not in ["--verbose", "-v", "--quiet", "-q"]]
        
        # Check if we have query arguments
        if args:
            # Join all arguments as a single query
            query = " ".join(args)
            
            # Run single query mode with appropriate quiet mode
            # Default is quiet unless verbose is specified
            use_quiet_mode = not verbose
            
            response = await app_service.run_single_query(query, quiet_mode=use_quiet_mode)
            print(response)
        else:
            # Run interactive mode (always quiet for better UX)
            await app_service.run_interactive_session()
            
    except KeyboardInterrupt:
        if verbose:
            logger.info("Application interrupted by user")
        print("\n👋 Goodbye!")
    except Exception as e:
        if verbose:
            logger.error("Application error", error=str(e))
        print(f"❌ Error: {str(e)}")
        sys.exit(1)


def start():
    """
    Application entry point for the script command.
    This function is called when you run: uv run openai-app
    """
    asyncio.run(main_async())


def main():
    """
    Alternative entry point.
    This function is called when you run the module directly.
    """
    start()


if __name__ == "__main__":
    main()

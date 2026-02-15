"""
Invoice Reminder Agent - Main Entry Point
"""
import asyncio
import os
from rich.console import Console
from rich.panel import Panel
from dotenv import load_dotenv

from voice_handler import VoiceHandler
from agent import InvoiceAgent
from utils.logger import setup_logger
from utils.config import Config

load_dotenv()
console = Console()
logger = setup_logger()

async def main():
    console.print(Panel.fit(
        "[bold cyan]🎙️ Invoice Reminder Agent[/bold cyan]\n"
        "[dim]Voice-enabled AR automation[/dim]\n\n"
        "Commands:\n"
        "  • 'Check overdue invoices'\n"
        "  • 'Send reminder to [company name]'\n"
        "  • 'Exit' to quit",
        title="Welcome",
        border_style="cyan"
    ))
    
    try:
        config = Config()
        voice = VoiceHandler(config)
        agent = InvoiceAgent(config)
        logger.info("Agent initialized")
        console.print("✅ [green]Ready![/green]\n")
    except Exception as e:
        console.print(f"❌ [red]Error: {e}[/red]")
        return
    
    while True:
        try:
            console.print("\n[yellow]🎤 Listening...[/yellow]")
            user_input = await voice.listen()
            
            if not user_input:
                continue
            
            console.print(f"[bold]👤 You:[/bold] {user_input}")
            
            if any(word in user_input.lower() for word in ['exit', 'quit', 'bye']):
                farewell = "Goodbye!"
                console.print(f"[bold]🤖 Agent:[/bold] {farewell}")
                await voice.speak(farewell)
                break
            
            response = await agent.process(user_input)
            console.print(f"[bold]🤖 Agent:[/bold] {response}")
            await voice.speak(response)
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            console.print(f"[red]❌ {e}[/red]")

if __name__ == "__main__":
    asyncio.run(main())

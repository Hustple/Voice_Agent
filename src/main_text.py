"""Text-only version"""
import asyncio
from agent import InvoiceAgent
from utils.config import Config
from utils.logger import setup_logger
from rich.console import Console


console = Console()
logger = setup_logger()

async def main():
    console.print("[cyan]🤖 Invoice Agent (Text Mode)[/cyan]\n")
    config = Config()
    agent = InvoiceAgent(config)
    console.print("Commands: 'check invoices', 'send reminder to [company]', 'exit'\n")
    
    while True:
        user_input = console.input("[yellow]You:[/yellow] ")
        if user_input.lower() in ['exit', 'quit']:
            console.print("[cyan]Goodbye![/cyan]")
            break
        response = await agent.process(user_input)
        console.print(f"[green]Agent:[/green] {response}\n")

if __name__ == "__main__":
    asyncio.run(main())

import typer
from rich.console import Console
from modules.domain_recon import get_whois, get_dns
from modules.ip_recon import get_ip_info
from modules.breach_check import check_breach, check_password
from modules.username_recon import search_username
from modules.report import generate_report

app = typer.Typer()
console = Console()

@app.command()
def domain(target: str):
    """Run domain recon on a target"""
    console.print(f"\n[bold cyan]🔍 Running Domain Recon on: {target}[/bold cyan]\n")
    get_whois(target)
    get_dns(target)

@app.command()
def ip(target: str):
    """Run IP intelligence on a target"""
    console.print(f"\n[bold magenta]🌐 Running IP Intel on: {target}[/bold magenta]\n")
    get_ip_info(target)

@app.command()
def breach(email: str):
    """Check if an email has been in a data breach"""
    console.print(f"\n[bold red]🔓 Checking breaches for: {email}[/bold red]\n")
    check_breach(email)

@app.command()
def password(pwd: str):
    """Check if a password has been leaked"""
    console.print(f"\n[bold yellow]🔑 Checking password safety...[/bold yellow]\n")
    check_password(pwd)

@app.command()
def username(target: str):
    """Search username across platforms"""
    search_username(target)

@app.command()
def report(target: str):
    """Generate a PDF report for a domain"""
    console.print(f"\n[bold green]📄 Generating report for: {target}[/bold green]\n")
    generate_report(target)

if __name__ == "__main__":
    app()
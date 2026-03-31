import subprocess
from rich.console import Console

console = Console()

def search_username(username):
    console.print(f"\n[bold cyan]🔍 Searching username '{username}' across platforms...[/bold cyan]\n")
    try:
        result = subprocess.run(
            ["sherlock", username, "--print-found"],
            capture_output=True,
            text=True
        )
        lines = result.stdout.splitlines()
        found = [l for l in lines if "[+]" in l]
        not_found = [l for l in lines if "[-]" in l]

        console.print(f"[bold green]✅ Found on {len(found)} platforms:[/bold green]")
        for line in found:
            console.print(f"  [green]{line.strip()}[/green]")

        console.print(f"\n[bold red]❌ Not found on {len(not_found)} platforms[/bold red]")

    except FileNotFoundError:
        console.print("[red]Sherlock not found. Make sure it's installed in venv.[/red]")
    except Exception as e:
        console.print(f"[red]Username search failed: {e}[/red]")
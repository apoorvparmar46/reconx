import requests
import hashlib
from rich.console import Console
from rich.table import Table

console = Console()

def check_breach(email):
    try:
        # Using HIBP API (Have I Been Pwned)
        headers = {"hibp-api-key": "free", "user-agent": "reconx-tool"}
        url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}?truncateResponse=false"
        response = requests.get(url, headers=headers)

        if response.status_code == 404:
            console.print(f"\n[bold green]✅ Good news! {email} was NOT found in any known breaches.[/bold green]\n")
            return

        if response.status_code == 401:
            console.print("[yellow]⚠ HIBP API requires a paid key for email lookup. Using password check instead.[/yellow]")
            return

        breaches = response.json()
        table = Table(title=f"💀 Breach Report — {email}", style="red")
        table.add_column("Site", style="bold yellow")
        table.add_column("Date", style="white")
        table.add_column("Data Leaked", style="cyan")

        for b in breaches:
            table.add_row(
                b.get("Name", "N/A"),
                b.get("BreachDate", "N/A"),
                ", ".join(b.get("DataClasses", []))
            )

        console.print(table)

    except Exception as e:
        console.print(f"[red]Breach check failed: {e}[/red]")


def check_password(password):
    # Uses k-anonymity — password never sent in full
    sha1 = hashlib.sha1(password.encode()).hexdigest().upper()
    prefix, suffix = sha1[:5], sha1[5:]

    response = requests.get(f"https://api.pwnedpasswords.com/range/{prefix}")
    hashes = response.text.splitlines()

    for line in hashes:
        h, count = line.split(":")
        if h == suffix:
            console.print(f"\n[bold red]⚠ This password has been leaked {count} times! Change it immediately.[/bold red]\n")
            return

    console.print(f"\n[bold green]✅ This password was not found in any known leaks.[/bold green]\n")
    
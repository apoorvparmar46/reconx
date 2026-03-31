import whois
import dns.resolver
from rich.console import Console
from rich.table import Table

console = Console()

def get_whois(domain):
    try:
        w = whois.whois(domain)
        table = Table(title=f"WHOIS — {domain}", style="cyan")
        table.add_column("Field", style="bold yellow")
        table.add_column("Value", style="white")

        table.add_row("Domain Name", str(w.domain_name))
        table.add_row("Registrar", str(w.registrar))
        table.add_row("Created", str(w.creation_date))
        table.add_row("Expires", str(w.expiration_date))
        table.add_row("Name Servers", str(w.name_servers))

        console.print(table)
    except Exception as e:
        console.print(f"[red]WHOIS failed: {e}[/red]")


def get_dns(domain):
    record_types = ["A", "MX", "TXT", "NS"]
    table = Table(title=f"DNS Records — {domain}", style="green")
    table.add_column("Type", style="bold yellow")
    table.add_column("Value", style="white")

    for record in record_types:
        try:
            answers = dns.resolver.resolve(domain, record)
            for r in answers:
                table.add_row(record, str(r))
        except:
            table.add_row(record, "Not found")

    console.print(table)
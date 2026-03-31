import requests
from rich.console import Console
from rich.table import Table

console = Console()

def get_ip_info(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        data = response.json()

        table = Table(title=f"IP Intelligence — {ip}", style="magenta")
        table.add_column("Field", style="bold yellow")
        table.add_column("Value", style="white")

        table.add_row("IP", data.get("query", "N/A"))
        table.add_row("Country", data.get("country", "N/A"))
        table.add_row("Region", data.get("regionName", "N/A"))
        table.add_row("City", data.get("city", "N/A"))
        table.add_row("ISP", data.get("isp", "N/A"))
        table.add_row("Org", data.get("org", "N/A"))
        table.add_row("Timezone", data.get("timezone", "N/A"))

        console.print(table)
    except Exception as e:
        console.print(f"[red]IP lookup failed: {e}[/red]")
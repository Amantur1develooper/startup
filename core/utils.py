import requests
from .models import Terminal

def check_terminals():
    terminals = Terminal.objects.all()
    
    for terminal in terminals:
        if not terminal.ngrok_url:
            terminal.is_active = False
            terminal.save()
            continue

        try:
            response = requests.get(f"{terminal.ngrok_url}/status", timeout=5)
            if response.status_code == 200:
                terminal.is_active = True
            else:
                terminal.is_active = False
        except requests.RequestException:
            terminal.is_active = False

        terminal.save()

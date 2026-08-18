import requests
import json
from rich import print as rprint


def instafind(username, verbose=False):
    url = "https://www.instagram.com/api/v1/web/accounts/account_recovery_send_ajax/"
    headers = {
        "Host": "www.instagram.com",
        "Content-Type": "application/x-www-form-urlencoded",
        "X-Csrftoken": "asdfgdfghjgfdhg",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
        "Accept": "*/*",
        "Referer": "https://www.instagram.com/accounts/password/reset/",
        "Origin": "https://www.instagram.com",
    }
    data = {
        "email_or_username": username
    }
    response = requests.post(url, headers=headers, data=data)
    try:
        result = json.loads(response.text)
        email = result.get("contact_point")
        if verbose:
            rprint(f"[bold pink][+] Your Instagram Account Email is[/bold pink] :- {email}")
        return {"success": True, "email": email}
    except Exception as e:
        if verbose:
            rprint("[!] Error decoding response")
        return {"success": False, "error": str(e)}
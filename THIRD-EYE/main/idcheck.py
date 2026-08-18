import requests
import json
from rich import print as rprint


def instafind(query, verbose=False):
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
        "email_or_username": query
    }
    response = requests.post(url, headers=headers, data=data)
    if verbose:
        rprint("\n[green][CHECK][/green] Checking Account On Instagram\n")
        rprint(" [red]If Status = [FAIL] fail Then Your Account is In Trouble or Account Did Not Exists \n If Status = [OK] ok Then Account Exists[/red]")
    try:
        result = response.json()
        with open("Data/instagram_information.json", "w", encoding="utf-8") as file:
            json.dump(result, file, ensure_ascii=False, indent=4)
        if verbose:
            rprint("[yellow]Instagram Information.json Saved in Data Folder[/yellow]")
            rprint("[LOOK]  Account Status :", result.get("status"), "\n")
        return {
            "found": result.get("status") == "ok",
            "status": result.get("status"),
            "raw": result,
        }
    except Exception:
        if verbose:
            rprint("[NOT FOUND]   Account Did Not Exists or Unable To Retrive Data\n")
        return {"found": False, "status": "error", "raw": None}
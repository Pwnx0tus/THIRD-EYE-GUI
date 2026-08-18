import requests
from rich import print as rprint


def firefox(email, verbose=False):
    try:
        response = requests.post(
            "https://api.accounts.firefox.com/v1/account/status",
            data={"email": email},
            timeout=10
        )
        if verbose:
            rprint("[green][CHECK][/green] Checking On Firefox.......... ")
        if "false" in response.text:
            if verbose:
                rprint("[-] Firefox: Not registered")
            return {"registered": False, "status": "not_registered"}
        elif "true" in response.text:
            if verbose:
                rprint("[+] Firefox: Registered")
            return {"registered": True, "status": "registered"}
        else:
            if verbose:
                rprint("[!] Firefox: Unknown (Possible Rate Limit)")
            return {"registered": None, "status": "unknown"}
    except requests.RequestException as e:
        if verbose:
            rprint(f"[!] Firefox: error ({e})")
        return {"registered": None, "status": "error", "error": str(e)}

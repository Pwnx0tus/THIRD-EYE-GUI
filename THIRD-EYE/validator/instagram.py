import requests
import json
from rich import print as rprint


def instafind(email, verbose=False):
    with open("main/check.json", "r") as file:
        config = json.load(file)

    url = config["url"]
    headers = config["headers"]
    payload_key = config["payload_key"]
    data = {payload_key: email}

    try:
        response = requests.post(url, headers=headers, data=data)
        result = response.json()
        contact_email = result.get("contact_point")
        if verbose:
            if contact_email:
                rprint(f"[+] Instagram account found!\n[-] Registered Email: {contact_email}\n")
            else:
                rprint("[!] No associated Instagram account found.")
        return {
            "found": contact_email is not None,
            "contact_email": contact_email,
        }
    except Exception as e:
        if verbose:
            rprint("[!] Error decoding response:", response.text if 'response' in dir() else str(e))
        return {"found": False, "error": str(e)}


if __name__ == "__main__":
    user_email = input("Enter email or username to check: ")
    if "@" in user_email and "." in user_email:
        rprint("[+] Valid Mail")
        instafind(user_email, verbose=True)
    else:
        rprint("[!] Please Enter Valid Email")

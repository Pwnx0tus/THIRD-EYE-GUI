import requests
import json
from rich import print as rprint
from .idcheck import instafind

def search_google(query, verbose=False):
    API_KEY = "AIzaSyDxQoDCbzrU22SwyLMln3Qj2__PMUFTC9o"
    SEARCH_ENGINE_ID = "84a64448a902c4626"

    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": API_KEY,
        "cx": SEARCH_ENGINE_ID,
        "q": query,
        "num": 10
    }

    if verbose:
        rprint("\n[green][FIND][/green] Searching Google...")
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        with open("Data/google_search_results.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        if verbose:
            rprint("[yellow]Google_Search_Results.json Saved in Data Folder[/yellow]\n")
        results = data.get("items", [])
        if verbose:
            rprint(f"[pink][+][/pink] Top {len(results)} Results for '{query}':")
            for index, item in enumerate(results, start=1):
                rprint(f"{index}. {item['title']}")
                rprint(f"   {item['link']}\n")
        return {
            "success": True,
            "query": str(query),
            "results": [
                {"title": item.get("title"), "link": item.get("link"), "snippet": item.get("snippet", "")}
                for item in results
            ]
        }
    else:
        if verbose:
            rprint("[pink][-][/pink] Google Search Error:", response.status_code)
        return {"success": False, "error": response.status_code, "detail": response.text}


def validate_phone_number(number, api_key=None, verbose=False):
    try:
        if not api_key:
            if verbose:
                api_key = input(f"Enter Your http://numverify.com API KEY:- ")
            else:
                return {"valid": False, "error": "Numverify API key is required"}
        url = "https://apilayer.net/api/validate"
        querystring = {"access_key": api_key, "number": number, "country_code": "IN", "format": "1"}

        if verbose:
            rprint("[red][+] Validating phone number...[/red]\n")
        response = requests.get(url, params=querystring)
        data = response.json()
        with open("Data/phone_validation.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        if verbose:
            rprint("[yellow]Phone_Validation.json Saved in Data Folder[/yellow]\n")
        if data.get("valid"):
            if verbose:
                rprint("[pink][<->][/pink] Phone Number is valid:")
                rprint(f"[pink][<->][/pink] Number: {data.get('number')}")
                rprint(f"[pink][<->][/pink] Country: {data.get('country_name')}")
                rprint(f"[pink][<->][/pink] Location: {data.get('location')}")
                rprint(f"[pink][<->][/pink] Carrier: {data.get('carrier')}")
                rprint(f"[pink][<->][/pink] Line Type: {data.get('line_type')}")
                rprint(f"[pink][<->][/pink] International Format: {data.get('international_format')}")
            return {
                "valid": True,
                "number": data.get("number"),
                "country": data.get("country_name"),
                "location": data.get("location"),
                "carrier": data.get("carrier"),
                "line_type": data.get("line_type"),
                "international_format": data.get("international_format"),
            }
        else:
            if verbose:
                rprint("[!] Invalid phone number.")
            return {"valid": False, "error": "Invalid phone number"}
    except Exception as e:
        if verbose:
            rprint("[!] Error during phone validation.")
        return {"valid": False, "error": str(e)}


def look(query, verbose=False):
    if verbose:
        rprint("\nTAKE A LOOK [0_0]")
        rprint(f"[pink][+][/pink] Look For Whatsapp : https://wa.me/{query}")
        rprint(f"[pink][+][/pink] Look For Telegram : https://t.me/{query}")
    return {
        "whatsapp_url": f"https://wa.me/{query}",
        "telegram_url": f"https://t.me/{query}",
    }


def WhatsappInfo(query, verbose=False):
    url = f"https://whatsapp-data1.p.rapidapi.com/number/91{query}"
    if verbose:
        rprint("WAIT......")
        rprint("Retriving Data From Whatsapp")
    headers = {
        "x-rapidapi-key": "a9aaf84445mshb4bf0006cf29d94p1822f9jsndf0fba00af47",
        "x-rapidapi-host": "whatsapp-data1.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        try:
            data = response.json()
            with open("Data/whatsapp_information.json", "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
            if verbose:
                rprint("[yellow]Whatsapp_Information.json Saved in Data Folder[/yellow]\n")
                rprint("[pink][<->][/pink] Profile Pic :", data.get("profilePic"))
                rprint("[pink][<->][/pink] Phone Number :", data.get("phone"))
                rprint("[pink][<->][/pink] About :", data.get("about\n"))
            return {
                "success": True,
                "profile_pic": data.get("profilePic"),
                "phone": data.get("phone"),
                "about": data.get("about"),
            }
        except Exception as e:
            if verbose:
                rprint("Failed to Retrive Data:", str(e))
            return {"success": False, "error": str(e)}
    else:
        return {"success": False, "error": f"HTTP {response.status_code}"}


if __name__ == "__main__":
    rprint("[magenta]Enter username to search[/magenta]: ", end="")
    query = int(input())
    search_google(query, verbose=True)
    rprint("\n" + "="*50 + "\n")
    validate_phone_number(query, verbose=True)
    look(query, verbose=True)
    WhatsappInfo(query, verbose=True)
    instafind(query)

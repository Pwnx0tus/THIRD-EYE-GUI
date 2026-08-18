import requests
import json
from rich import print as rprint


def check_ip(ip_address, verbose=False):
    try:
        API_KEY = "7695903ca38b47708d680f13c87cee10"
        url = f"https://api.ipstack.com/{ip_address}?access_key={API_KEY}"
        response = requests.get(url)
        data = response.json()
        with open("Data/ip_information.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        if verbose:
            rprint("[yellow]Ip Information.json Saved in Data Folder[/yellow]\n")
            rprint(f"IP Address: {data.get('ip')}")
            rprint(f"Country: {data.get('country_name')}")
            rprint(f"Region: {data.get('region_name')}")
            rprint(f"City: {data.get('city')}")
            rprint(f"Latitude: {data.get('latitude')}")
            rprint(f"Longitude: {data.get('longitude')}")
            rprint(f"ISP: {data.get('connection', {}).get('isp')}")
            rprint(f"Location: {data.get('location', {}).get('geoname_id')}")
            rprint(f"Language: {data.get('location', {}).get('languages', [{}])[0].get('name')}", "\n")
        return {
            "success": True,
            "ip": data.get("ip"),
            "country": data.get("country_name"),
            "region": data.get("region_name"),
            "city": data.get("city"),
            "latitude": data.get("latitude"),
            "longitude": data.get("longitude"),
            "isp": data.get("connection", {}).get("isp"),
            "geoname_id": data.get("location", {}).get("geoname_id"),
            "language": data.get("location", {}).get("languages", [{}])[0].get("name") if data.get("location", {}).get("languages") else None,
            "raw": data,
        }
    except Exception as e:
        if verbose:
            rprint("Error: Unable to validate the IP address. Please check your input or try again later.")
        return {"success": False, "error": str(e)}


def check_ip_address():
    """CLI entry point — preserved for backward compatibility."""
    rprint("[magenta]Enter IP Address to search[/magenta]: ", end="")
    ip = input()
    result = check_ip(ip, verbose=True)
    if not result["success"]:
        rprint("Error: Unable to validate the IP address. Please check your input or try again later. or check your internet connection.")
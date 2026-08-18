import requests
from rich import print as rprint


def hudson(email, verbose=False):
    api = "https://cavalier.hudsonrock.com/api/json/v2/osint-tools/search-by-email"

    try:
        response = requests.get(api, headers={'api-key': 'ROCKHUDSONROCK'}, params={'email': email})
        if verbose:
            rprint(response.text)
        try:
            return {"success": True, "data": response.json()}
        except Exception:
            return {"success": True, "data": response.text}
    except Exception as e:
        return {"success": False, "error": str(e)}

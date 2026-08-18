import requests
import json
import re
from rich import print as rprint
from bs4 import BeautifulSoup


def chess(username, verbose=False):
    url = f"https://www.chess.com/member/{username}"
    response = requests.get(url)
    try:
        soup = BeautifulSoup(response.text, 'html.parser')
        profilehead = soup.find("div", class_="profile-header-details-item").text.strip()
        name = soup.find("div", class_="profile-card-name").text.strip()
        plocation = soup.find("div", class_="profile-card-location").text.strip()
        if verbose:
            rprint("\n=== Chess.com Profile Information ===\n")
            rprint("[magenta][>>][/magenta]  Joined On Chess: ", profilehead)
            rprint("[magenta][>>][/magenta] Profile Name    : ", name)
            rprint("[magenta][>>][/magenta] User Location   : ", plocation)
        return {
            "success": True,
            "joined": profilehead,
            "name": name,
            "location": plocation,
        }
    except Exception as e:
        if verbose:
            rprint("Check Your Internet Or Unable To Extract Data")
        return {"success": False, "error": str(e)}


def instauser(username, verbose=False):
    headers_id = {
        'Host': 'www.instagram.com',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Accept-Language': 'en-GB,en;q=0.9',
        'Sec-Ch-Ua': '"Not)A;Brand";v="8", "Chromium";v="138"',
        'Sec-Ch-Ua-Model': '""',
        'Sec-Ch-Ua-Mobile': '?0',
        'X-Asbd-Id': '359341',
        'X-Ig-D': 'www',
        'X-Fb-Lsd': 'AVrpG3JvYVI',
        'Sec-Ch-Prefers-Color-Scheme': 'dark',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Sec-Ch-Ua-Platform-Version': '""',
        'Accept': '*/*',
        'Origin': 'https://www.instagram.com',
        'Sec-Fetch-Site': 'same-origin',
    }

    data_id = f'\r\n\r\n\r\nroute_urls[0]=%2F{username}%2F&route_urls[1]=%2Fstories%2F{username}%2F%3Fr%3D1&routing_namespace=igx_www%24a%2487a091182d5bd65bcb043a2888004e09&__a=1&__hs=20288.HYP%3Ainstagram_web_pkg.2.1...0&__comet_req=7&lsd=AVrpG3JvYVI'

    response_id = requests.post('https://www.instagram.com/ajax/bulk-route-definitions/', headers=headers_id, data=data_id, verify=True)

    match = re.search(r'"id"\s*:\s*"(\d+)"', response_id.text)
    if not match:
        return {"success": False, "error": "User ID not found"}

    userid = match.group(1)

    headers_profile = {
        'Host': 'www.instagram.com',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'X-Root-Field-Name': 'fetch__XDTUserDict',
        'Sec-Ch-Ua': '"Not)A;Brand";v="8", "Chromium";v="138"',
        'Sec-Ch-Ua-Model': '""',
        'Sec-Ch-Ua-Mobile': '?0',
        'X-Ig-App-Id': '936619743392459',
        'X-Fb-Lsd': 'AVrpG3JvIkk',
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Csrftoken': '4HAnA7JRaAhCK-yl2myRLS',
        'Accept-Language': 'en-GB,en;q=0.9',
        'X-Fb-Friendly-Name': 'PolarisProfilePageContentQuery',
        'X-Bloks-Version-Id': 'e1456a3f58800541d8a2ea65b55937920007fee744eed6e5b1a7723cbe417e5f',
        'X-Asbd-Id': '359341',
    }

    data_profile = f'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36\r\n\r\n\r\n\r\n&variables=%7B%22id%22%3A%22{userid}%22%2C%22render_surface%22%3A%22PROFILE%22%7D&doc_id=24098904923132686'

    response = requests.post('https://www.instagram.com/graphql/query', headers=headers_profile, data=data_profile, verify=True)

    data = response.json()

    with open("Data/instagramprofile_information.json", "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    try:
        user = data["data"]["user"]
        bio = user.get("biography")
        fullname = user.get("full_name")
        purl = user.get("hd_profile_pic_url_info", {}).get("url")
        fcount = user.get("following_count")
        mcount = user.get("media_count")
        uid = user.get("id")
        followcount = user.get("follower_count")
        linked = user.get("biography_with_entities", {}).get("entities", [])
        hashtags = [e["hashtag"] for e in linked if e.get("hashtag")]
        users = [e["user"] for e in linked if e.get("user")]

        if verbose:
            rprint("\n=== Instagram Profile Information ===\n")
            rprint("[magenta][>>][/magenta] Bio Of A Profile   : ", bio)
            rprint("[magenta][>>][/magenta] Fullname           : ", fullname)
            rprint("[magenta][>>][/magenta] Profile Pic URL    : ", purl)
            rprint("[magenta][>>][/magenta] Following          : ", fcount)
            rprint("[magenta][>>][/magenta] Followers          : ", followcount)
            rprint("[magenta][>>][/magenta] Posts              : ", mcount)
            rprint("[magenta][>>][/magenta] User ID            : ", uid)

        return {
            "success": True,
            "user_id": uid,
            "bio": bio,
            "full_name": fullname,
            "profile_pic_url": purl,
            "following": fcount,
            "followers": followcount,
            "posts": mcount,
            "hashtags": [{"name": h["name"], "id": h["id"]} for h in hashtags],
            "tagged_users": [{"username": u["username"], "id": u["id"]} for u in users],
        }
    except Exception as e:
        if verbose:
            rprint("[-] Failed to parse profile data:", e)
        return {"success": False, "error": str(e)}


def gitinfo(username, verbose=False):
    url = f"https://github.com/{username}"
    result = {
        "success": True,
        "username": username,
        "url": url,
    }

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        try:
            result["bio"] = soup.find("div", class_="p-note user-profile-bio mb-3 js-user-profile-bio f4").div.text.strip()
        except Exception:
            result["bio"] = None

        try:
            result["org"] = soup.find("span", class_="p-org").div.text.strip()
        except Exception:
            result["org"] = None

        try:
            result["country"] = soup.find("span", class_="p-label").text.strip()
        except Exception:
            result["country"] = None

        try:
            result["links"] = [a['href'] for a in soup.find_all("a", class_="Link--primary") if a.has_attr('href')]
        except Exception:
            result["links"] = []

        try:
            result["full_name"] = soup.find("span", class_="p-name").text.strip()
        except Exception:
            result["full_name"] = None

        try:
            result["handle"] = soup.find("span", class_="vcard-username").text.strip()
        except Exception:
            result["handle"] = None

        try:
            result["status"] = soup.find("div", class_="user-status-message-wrapper").div.text.strip()
        except Exception:
            result["status"] = None

        try:
            follow_spans = [span.text.strip() for span in soup.find_all("span", class_="text-bold")]
            result["followers"] = follow_spans[0] if len(follow_spans) > 0 else None
            result["following"] = follow_spans[1] if len(follow_spans) > 1 else None
        except Exception:
            result["followers"] = None
            result["following"] = None

        try:
            result["avatar_url"] = soup.find("img", class_="avatar")['src']
        except Exception:
            result["avatar_url"] = None

        if verbose:
            rprint("\n=== GitHub Profile Information ===\n")
            for k, v in result.items():
                rprint(f"[magenta][>>][/magenta] {k}: {v}")

    except Exception as e:
        result["success"] = False
        result["error"] = str(e)

    return result

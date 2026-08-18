import requests
import json
import time
from rich import print as rprint
from concurrent.futures import ThreadPoolExecutor, as_completed
from .instaemailfind import instafind as infind
from .scrap import chess, instauser, gitinfo


def load_sites_config(path="main/murl.json"):
    with open(path, 'r') as f:
        return json.load(f)


def check_username_on_site(username, site_name, site_config):
    url = site_config["url"].replace("{username}", username)
    headers = site_config.get("headers", {})
    timeout = site_config.get("timeout_seconds", 5)
    delay = site_config.get("rate_limit_delay", 1)
    allow_redirects = (site_config["redirect_behavior"] == "follow")

    try:
        response = requests.request(
            method=site_config["request_method"],
            url=url,
            headers=headers,
            timeout=timeout,
            allow_redirects=allow_redirects,
        )

        if not site_config["detect_based_on_message"]:
            if response.status_code in site_config["not_found_status_codes"]:
                return site_name, False, None
            return site_name, True, url

        content = response.text
        if site_config["not_found_message"] and site_config["not_found_message"] in content:
            return site_name, False, None
        if site_config["found_message"] and site_config["found_message"] in content:
            return site_name, True, url

        return site_name, None, None
    except requests.RequestException:
        return site_name, None, None
    finally:
        time.sleep(delay)


def check_username(username, progress_callback=None, verbose=False):
    """
    Checks the username across all configured sites.

    Args:
        username: The username string to search for.
        progress_callback: Optional callable(site_name, found, link, extra) called for each result.
        verbose: If True, prints results to console using rich.

    Returns:
        dict with 'found', 'not_found', 'unknown', 'extras' lists.
    """
    sites = load_sites_config()

    found_list = []
    not_found_list = []
    unknown_list = []
    extras = {}

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [
            executor.submit(check_username_on_site, username, site_name, site_config)
            for site_name, site_config in sites.items()
        ]

        for future in as_completed(futures):
            site_name, result, link = future.result()
            extra_data = {}

            if result is True:
                found_list.append({"site": site_name, "url": link})
                if verbose:
                    rprint(f"[+] Found on {site_name} : {link}")
            elif result is False:
                not_found_list.append(site_name)
            else:
                unknown_list.append(site_name)

            if site_name.lower() == "instagram":
                try:
                    instagram_data = infind(username)
                    insta_profile = instauser(username)
                    extra_data["instagram"] = {"email_find": instagram_data, "profile": insta_profile}
                    extras["instagram"] = extra_data["instagram"]
                    if verbose:
                        rprint("[magenta][+][/magenta] Running Instagram email lookup...\n")
                except Exception as e:
                    extras["instagram"] = {"error": str(e)}
            elif site_name.lower() == "chess.com":
                try:
                    chess_data = chess(username)
                    extras["chess"] = chess_data
                except Exception as e:
                    extras["chess"] = {"error": str(e)}
            elif site_name.lower() == "github":
                try:
                    git_data = gitinfo(username)
                    extras["github"] = git_data
                except Exception as e:
                    extras["github"] = {"error": str(e)}

            if progress_callback:
                progress_callback(site_name, result, link, extra_data)

    return {
        "username": username,
        "found": found_list,
        "not_found": not_found_list,
        "unknown": unknown_list,
        "extras": extras,
    }


def main():
    """CLI entry point — preserved for backward compatibility."""
    rprint("[magenta]Enter username to search[/magenta]: ", end="")
    username = input().strip()
    results = check_username(username, verbose=True)
    rprint(f"\n[bold green]Scan complete. Found on {len(results['found'])} sites.[/bold green]")


if __name__ == "__main__":
    main()

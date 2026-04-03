#!/usr/bin/env python3
"""Retry and fix remaining missing images."""

import os
import time
import json
import urllib.request
import urllib.parse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(BASE_DIR, "images")
HEADERS = {"User-Agent": "spw-fr-ebook/1.0 (educational-book-project)"}
WP_API = "https://en.wikipedia.org/w/api.php"

# Fixed article titles + retry entries
IMAGES = [
    # artyleria_holowana - corrected titles
    ("artyleria_holowana", "m-30_1.jpg",       "M-30 howitzer"),
    ("artyleria_holowana", "m-46_1.jpg",       "M-46 (field gun)"),
    ("artyleria_holowana", "d-1_1.jpg",        "D-1 howitzer"),

    # karabiny - corrected
    ("karabiny", "ak-103_1.jpg",   "AK-100 series"),
    ("karabiny", "ak-15_1.jpg",    "AK-12"),          # no AK-15 article, use AK-12
    ("karabiny", "an-94_1.jpg",    "AN-94 assault rifle"),

    # karabiny_maszynowe - retry 429s
    ("karabiny_maszynowe", "kord_1.jpg",  "Kord machine gun"),

    # karabiny snajperskie - retry 429s
    ("karabiny_snajperskie", "svd_1.jpg",    "SVD Dragunov"),
    ("karabiny_snajperskie", "ksvk_1.jpg",   "KSVK"),
    ("karabiny_snajperskie", "lobaev_1.jpg", "SVLK-14S"),   # try shorter

    # rpg - retry + corrected
    ("rpg_wyrzutnie", "rpg-26_1.jpg", "RPG-26"),
    ("rpg_wyrzutnie", "rpg-27_1.jpg", "RPG-27"),
    ("rpg_wyrzutnie", "rshg-1_1.jpg", "Thermobaric weapon"),   # fallback
    ("rpg_wyrzutnie", "bur_1.jpg",    "Rocket-propelled grenade"),  # fallback

    # wyrzutnie - retry 429s
    ("wyrzutnie_granatow", "gp-25_1.jpg",  "GP-25"),
    ("wyrzutnie_granatow", "ags-17_1.jpg", "AGS-17"),
    ("wyrzutnie_granatow", "ags-40_1.jpg", "AGS-40 Balkan"),

    # pistolety - retry 429s + corrected
    ("pistolety_i_pm", "tt_1.jpg",     "TT pistol"),
    ("pistolety_i_pm", "aps_1.jpg",    "Stechkin pistol"),
    ("pistolety_i_pm", "mp-443_1.jpg", "MP-443 Grach"),
    ("pistolety_i_pm", "sr-1_1.jpg",   "SR-1 Vektor"),
    ("pistolety_i_pm", "ots-23_1.jpg", "OTs-23"),
    ("pistolety_i_pm", "pp-2000_1.jpg","PP-2000"),
    ("pistolety_i_pm", "pl-15_1.jpg",  "Lebedev PL-15"),

    # granaty - corrected
    ("granaty_reczne", "f-1_1.jpg",   "Soviet hand grenades"),

    # miny - retry 429s + corrected
    ("miny", "pmn-2_1.jpg",  "PMN-2 mine"),
    ("miny", "tm-57_1.jpg",  "TM-57"),
    ("miny", "tm-62_1.jpg",  "TM-62 mine"),
    ("miny", "kpom-2_1.jpg", "Cluster munition"),    # fallback
    ("miny", "umz_1.jpg",    "Mine-laying"),          # fallback
]


def get_wp_image_url(article_title, thumb_size=500):
    params = {
        "action": "query",
        "titles": article_title,
        "prop": "pageimages",
        "pithumbsize": str(thumb_size),
        "format": "json",
        "redirects": "1",
    }
    url = WP_API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
        pages = data.get("query", {}).get("pages", {})
        for page in pages.values():
            thumb = page.get("thumbnail")
            if thumb:
                return thumb.get("source")
    except Exception as e:
        print(f"  API error: {e}")
    return None


def download_file(url, dest_path):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = resp.read()
    with open(dest_path, "wb") as f:
        f.write(data)
    return len(data)


def main():
    ok = 0
    fail = 0
    skip = 0
    failed_list = []

    for (subdir, local_name, wp_title) in IMAGES:
        dest_dir = os.path.join(IMG_DIR, subdir)
        os.makedirs(dest_dir, exist_ok=True)
        dest_path = os.path.join(dest_dir, local_name)

        if os.path.exists(dest_path) and os.path.getsize(dest_path) > 1000:
            print(f"SKIP {subdir}/{local_name}")
            skip += 1
            continue

        print(f"GET  {subdir}/{local_name}  <-  '{wp_title}'")
        url = get_wp_image_url(wp_title)
        if not url:
            print(f"  BRAK obrazu")
            fail += 1
            failed_list.append((subdir, local_name, wp_title))
            time.sleep(0.5)
            continue

        try:
            size = download_file(url, dest_path)
            print(f"  OK  {size//1024} KB")
            ok += 1
        except Exception as e:
            print(f"  BŁĄD: {e}")
            fail += 1
            failed_list.append((subdir, local_name, wp_title))

        time.sleep(0.6)

    print(f"\n=== WYNIK: {ok} pobrano, {skip} pominięto, {fail} błędów ===")
    if failed_list:
        print("\nNie udało się:")
        for subdir, local_name, wp_title in failed_list:
            print(f"  {subdir}/{local_name}  ('{wp_title}')")


if __name__ == "__main__":
    main()

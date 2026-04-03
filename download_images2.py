#!/usr/bin/env python3
"""Download images from Wikipedia using pageimages API."""

import os
import time
import json
import urllib.request
import urllib.parse
import urllib.error

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(BASE_DIR, "images")

HEADERS = {"User-Agent": "spw-fr-ebook/1.0 (educational-book-project)"}

# Mapping: (local_dir, local_filename, wikipedia_article_title)
IMAGES = [
    # --- artyleria_holowana ---
    ("artyleria_holowana", "m-30_1.jpg",       "122 mm howitzer M1938"),
    ("artyleria_holowana", "m-46_1.jpg",       "M-46 field gun"),
    ("artyleria_holowana", "d-1_1.jpg",        "152 mm howitzer D-1"),
    ("artyleria_holowana", "d-20_1.jpg",       "D-20 howitzer"),
    ("artyleria_holowana", "msta-b_1.jpg",     "2A65 Msta-B"),
    ("artyleria_holowana", "giatsint-b_1.jpg", "2A36 Giatsint-B"),
    ("artyleria_holowana", "vasilek_1.jpg",    "2B9 Vasilek"),
    ("artyleria_holowana", "podnos_1.jpg",     "2B14 Podnos"),
    ("artyleria_holowana", "sani_1.jpg",       "2S12 Sani"),

    # --- karabiny szturmowe ---
    ("karabiny", "aks-74u_1.jpg",  "AKS-74U"),
    ("karabiny", "ak-103_1.jpg",   "AK-103"),
    ("karabiny", "ak-15_1.jpg",    "AK-15"),
    ("karabiny", "an-94_1.jpg",    "AN-94"),
    ("karabiny", "aek-971_1.jpg",  "AEK-971"),
    ("karabiny", "sr-3_1.jpg",     "SR-3 Vikhr"),
    ("karabiny", "as-val_1.jpg",   "AS Val"),

    # --- karabiny maszynowe ---
    ("karabiny_maszynowe", "rpk_1.jpg",   "RPK"),
    ("karabiny_maszynowe", "rpl-20_1.jpg","RPL-20"),
    ("karabiny_maszynowe", "pk_1.jpg",    "PK machine gun"),
    ("karabiny_maszynowe", "pkp_1.jpg",   "PKP Pecheneg"),
    ("karabiny_maszynowe", "dshk_1.jpg",  "DShK"),
    ("karabiny_maszynowe", "nsv_1.jpg",   "NSV machine gun"),
    ("karabiny_maszynowe", "kord_1.jpg",  "Kord machine gun"),

    # --- karabiny snajperskie ---
    ("karabiny_snajperskie", "vss_1.jpg",    "VSS Vintorez"),
    ("karabiny_snajperskie", "svd_1.jpg",    "SVD Dragunov"),
    ("karabiny_snajperskie", "sv-98_1.jpg",  "SV-98"),
    ("karabiny_snajperskie", "orsis_1.jpg",  "Orsis T-5000"),
    ("karabiny_snajperskie", "ksvk_1.jpg",   "KSVK"),
    ("karabiny_snajperskie", "osv-96_1.jpg", "OSV-96"),
    ("karabiny_snajperskie", "lobaev_1.jpg", "Lobaev Arms SVLK-14S"),

    # --- rpg i wyrzutnie ---
    ("rpg_wyrzutnie", "rpg-7_1.jpg",  "RPG-7"),
    ("rpg_wyrzutnie", "rpg-18_1.jpg", "RPG-18"),
    ("rpg_wyrzutnie", "rpg-22_1.jpg", "RPG-22"),
    ("rpg_wyrzutnie", "rpg-26_1.jpg", "RPG-26"),
    ("rpg_wyrzutnie", "rpg-27_1.jpg", "RPG-27"),
    ("rpg_wyrzutnie", "rpg-29_1.jpg", "RPG-29"),
    ("rpg_wyrzutnie", "rpg-30_1.jpg", "RPG-30"),
    ("rpg_wyrzutnie", "rpg-32_1.jpg", "RPG-32 Hashim"),
    ("rpg_wyrzutnie", "rshg-1_1.jpg", "RShG-1"),
    ("rpg_wyrzutnie", "shmel_1.jpg",  "RPO-A Shmel"),
    ("rpg_wyrzutnie", "bur_1.jpg",    "MRO-A Bur"),

    # --- wyrzutnie granatow ---
    ("wyrzutnie_granatow", "gp-25_1.jpg",  "GP-25"),
    ("wyrzutnie_granatow", "gp-30_1.jpg",  "GP-30"),
    ("wyrzutnie_granatow", "gp-34_1.jpg",  "GP-34"),
    ("wyrzutnie_granatow", "ags-17_1.jpg", "AGS-17"),
    ("wyrzutnie_granatow", "ags-30_1.jpg", "AGS-30"),
    ("wyrzutnie_granatow", "ags-40_1.jpg", "AGS-40 Balkan"),
    ("wyrzutnie_granatow", "gm-94_1.jpg",  "GM-94"),

    # --- pistolety i pm ---
    ("pistolety_i_pm", "pm_1.jpg",          "Makarov pistol"),
    ("pistolety_i_pm", "tt_1.jpg",          "Tokarev pistol"),
    ("pistolety_i_pm", "aps_1.jpg",         "Stechkin pistol"),
    ("pistolety_i_pm", "pb_1.jpg",          "PB pistol"),
    ("pistolety_i_pm", "psm_1.jpg",         "PSM pistol"),
    ("pistolety_i_pm", "mp-443_1.jpg",      "MP-443 Grach"),
    ("pistolety_i_pm", "gsh-18_1.jpg",      "GSh-18"),
    ("pistolety_i_pm", "sr-1_1.jpg",        "SR-1 Vektor"),
    ("pistolety_i_pm", "ots-33_1.jpg",      "OTs-33 Pernach"),
    ("pistolety_i_pm", "ots-23_1.jpg",      "OTs-23 Drotik"),
    ("pistolety_i_pm", "pp-91_1.jpg",       "PP-91 Kedr"),
    ("pistolety_i_pm", "pp-2000_1.jpg",     "PP-2000"),
    ("pistolety_i_pm", "pl-15_1.jpg",       "PL-15 pistol"),
    ("pistolety_i_pm", "spp-1m_1.jpg",      "SPP-1"),
    ("pistolety_i_pm", "sps-underwater_1.jpg","APS underwater rifle"),

    # --- granaty reczne ---
    ("granaty_reczne", "f-1_1.jpg",   "F-1 grenade"),
    ("granaty_reczne", "rgd-5_1.jpg", "RGD-5"),
    ("granaty_reczne", "rgn_1.jpg",   "RGN grenade"),
    ("granaty_reczne", "rgo_1.jpg",   "RGO grenade"),
    ("granaty_reczne", "rkg-3_1.jpg", "RKG-3"),
    ("granaty_reczne", "vog-25_1.jpg","VOG-25"),

    # --- miny ---
    ("miny", "pmn_1.jpg",    "PMN mine"),
    ("miny", "pmn-2_1.jpg",  "PMN-2 mine"),
    ("miny", "ozm-72_1.jpg", "OZM-72"),
    ("miny", "pom-2_1.jpg",  "POM-2"),
    ("miny", "pfm-1_1.jpg",  "PFM-1"),
    ("miny", "mon-50_1.jpg", "MON-50"),
    ("miny", "mon-100_1.jpg","MON-100"),
    ("miny", "tm-57_1.jpg",  "TM-57"),
    ("miny", "tm-62_1.jpg",  "TM-62"),
    ("miny", "ptm-3_1.jpg",  "PTM-3"),
    ("miny", "kpom-2_1.jpg", "KPOM-2"),
    ("miny", "umz_1.jpg",    "UMZ (mine)"),
    ("miny", "vs-50_1.jpg",  "VS-50"),
]

WP_API = "https://en.wikipedia.org/w/api.php"


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
        print(f"  API error for '{article_title}': {e}")
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
            print(f"  BRAK obrazu dla artykułu '{wp_title}'")
            fail += 1
            failed_list.append((subdir, local_name, wp_title))
            time.sleep(0.5)
            continue

        try:
            size = download_file(url, dest_path)
            print(f"  OK  {size//1024} KB  [{url[:80]}...]")
            ok += 1
        except Exception as e:
            print(f"  BŁĄD pobierania: {e}")
            fail += 1
            failed_list.append((subdir, local_name, wp_title))

        time.sleep(0.5)

    print(f"\n=== WYNIK: {ok} pobrano, {skip} pominięto, {fail} błędów ===")
    if failed_list:
        print("\nNie udało się pobrać:")
        for subdir, local_name, wp_title in failed_list:
            print(f"  {subdir}/{local_name}  ('{wp_title}')")


if __name__ == "__main__":
    main()

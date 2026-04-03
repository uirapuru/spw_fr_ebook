#!/usr/bin/env python3
"""Download missing images from Wikimedia Commons for the e-book."""

import os
import time
import json
import urllib.request
import urllib.parse
import urllib.error

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(BASE_DIR, "images")

# Mapping: (local_dir, local_filename, wikimedia_commons_filename)
IMAGES = [
    # --- artyleria_holowana (missing) ---
    ("artyleria_holowana", "m-30_1.jpg",      "122_mm_howitzer_M1938_(M-30)_Batey_ha-Osef-1.jpg"),
    ("artyleria_holowana", "m-46_1.jpg",      "M-46_130mm_field_gun_batey_ha-osef_1.jpg"),
    ("artyleria_holowana", "d-1_1.jpg",       "152_mm_howitzer_D-1_batey_ha-osef_1.jpg"),
    ("artyleria_holowana", "d-20_1.jpg",      "D-20_152mm_gun-howitzer.jpg"),
    ("artyleria_holowana", "msta-b_1.jpg",    "2A65_howitzer.jpg"),
    ("artyleria_holowana", "giatsint-b_1.jpg","2A36_howitzer_batey_ha-osef_3.jpg"),
    ("artyleria_holowana", "vasilek_1.jpg",   "2B9_Vasilek_automatic_mortar.jpg"),
    ("artyleria_holowana", "podnos_1.jpg",    "2B14_Podnos_-_Nizhny_Tagil_2008.jpg"),
    ("artyleria_holowana", "sani_1.jpg",      "2S12_Sani_mortar_system.jpg"),

    # --- karabiny szturmowe (missing) ---
    ("karabiny", "aks-74u_1.jpg",  "AKS-74U_-_AM.jpg"),
    ("karabiny", "ak-103_1.jpg",   "AK-103_-_AM.jpg"),
    ("karabiny", "ak-15_1.jpg",    "AK-15_-_AM.jpg"),
    ("karabiny", "an-94_1.jpg",    "AN-94_Abakan_-_AM.jpg"),
    ("karabiny", "aek-971_1.jpg",  "AEK-971_-_AM.jpg"),
    ("karabiny", "sr-3_1.jpg",     "SR-3M_Whirlwind_-_AM.jpg"),
    ("karabiny", "as-val_1.jpg",   "AS_Val_-_AM.jpg"),

    # --- karabiny maszynowe ---
    ("karabiny_maszynowe", "rpk_1.jpg",        "RPK_-_AM.jpg"),
    ("karabiny_maszynowe", "rpl-20_1.jpg",     "RPL-20.jpg"),
    ("karabiny_maszynowe", "pk_1.jpg",         "PK_machine_gun_DD-SD-06-07351.jpg"),
    ("karabiny_maszynowe", "pkp_1.jpg",        "PKP_Pecheneg_-_AM.jpg"),
    ("karabiny_maszynowe", "dshk_1.jpg",       "DShK_in_Afghanistan.jpg"),
    ("karabiny_maszynowe", "nsv_1.jpg",        "UTES_12.7mm_machine_gun.jpg"),
    ("karabiny_maszynowe", "kord_1.jpg",       "Kord_(machine_gun)_-_AM.jpg"),

    # --- karabiny snajperskie ---
    ("karabiny_snajperskie", "vss_1.jpg",     "VSS_Vintorez_-_AM.jpg"),
    ("karabiny_snajperskie", "svd_1.jpg",     "SVD_Dragunov_-_AM.jpg"),
    ("karabiny_snajperskie", "sv-98_1.jpg",   "SV-98_-_AM.jpg"),
    ("karabiny_snajperskie", "orsis_1.jpg",   "Orsis_T-5000.jpg"),
    ("karabiny_snajperskie", "ksvk_1.jpg",    "KSVK_12.7.jpg"),
    ("karabiny_snajperskie", "osv-96_1.jpg",  "OSV-96_MAKS-2009.jpg"),
    ("karabiny_snajperskie", "lobaev_1.jpg",  "Lobaev_SVLK-14S.jpg"),

    # --- rpg i wyrzutnie ---
    ("rpg_wyrzutnie", "rpg-7_1.jpg",   "RPG-7_detached.jpg"),
    ("rpg_wyrzutnie", "rpg-18_1.jpg",  "RPG-18_-_AM.jpg"),
    ("rpg_wyrzutnie", "rpg-22_1.jpg",  "RPG-22_-_AM.jpg"),
    ("rpg_wyrzutnie", "rpg-26_1.jpg",  "RPG-26_-_AM.jpg"),
    ("rpg_wyrzutnie", "rpg-27_1.jpg",  "RPG-27_-_AM.jpg"),
    ("rpg_wyrzutnie", "rpg-29_1.jpg",  "RPG-29_-_AM.jpg"),
    ("rpg_wyrzutnie", "rpg-30_1.jpg",  "RPG-30.jpg"),
    ("rpg_wyrzutnie", "rpg-32_1.jpg",  "RPG-32.jpg"),
    ("rpg_wyrzutnie", "rshg-1_1.jpg",  "RShG-1.jpg"),
    ("rpg_wyrzutnie", "shmel_1.jpg",   "RPO-A_Shmel_-_AM.jpg"),
    ("rpg_wyrzutnie", "bur_1.jpg",     "MRO-A_Bur.jpg"),

    # --- wyrzutnie granatow ---
    ("wyrzutnie_granatow", "gp-25_1.jpg",  "GP-25_-_AM.jpg"),
    ("wyrzutnie_granatow", "gp-30_1.jpg",  "GP-30_-_AM.jpg"),
    ("wyrzutnie_granatow", "gp-34_1.jpg",  "GP-34_-_AM.jpg"),
    ("wyrzutnie_granatow", "ags-17_1.jpg", "AGS-17_DD-SC-86-00895.jpg"),
    ("wyrzutnie_granatow", "ags-30_1.jpg", "AGS-30_-_AM.jpg"),
    ("wyrzutnie_granatow", "ags-40_1.jpg", "AGS-40_Balkan.jpg"),
    ("wyrzutnie_granatow", "gm-94_1.jpg",  "GM-94_-_AM.jpg"),

    # --- pistolety i pm ---
    ("pistolety_i_pm", "pm_1.jpg",          "Makarov_DD-SC-84-10636.jpg"),
    ("pistolety_i_pm", "tt_1.jpg",          "TT_Tokarev_1940.jpg"),
    ("pistolety_i_pm", "aps_1.jpg",         "APS_Stechkin_-_AM.jpg"),
    ("pistolety_i_pm", "pb_1.jpg",          "PB_silent_pistol_-_AM.jpg"),
    ("pistolety_i_pm", "psm_1.jpg",         "PSM_pistol_-_AM.jpg"),
    ("pistolety_i_pm", "mp-443_1.jpg",      "MP-443_Grach_-_AM.jpg"),
    ("pistolety_i_pm", "gsh-18_1.jpg",      "GSh-18_-_AM.jpg"),
    ("pistolety_i_pm", "sr-1_1.jpg",        "SR-1_Vektor_-_AM.jpg"),
    ("pistolety_i_pm", "ots-33_1.jpg",      "OTs-33_Pernach_-_AM.jpg"),
    ("pistolety_i_pm", "ots-23_1.jpg",      "OTs-23_Drotik_-_AM.jpg"),
    ("pistolety_i_pm", "pp-91_1.jpg",       "PP-91_Kedr_-_AM.jpg"),
    ("pistolety_i_pm", "pp-2000_1.jpg",     "PP-2000_-_AM.jpg"),
    ("pistolety_i_pm", "pl-15_1.jpg",       "PL-15_pistol.jpg"),
    ("pistolety_i_pm", "spp-1m_1.jpg",      "SPP-1M.jpg"),
    ("pistolety_i_pm", "sps-underwater_1.jpg", "APS_underwater_rifle_-_AM.jpg"),

    # --- granaty reczne ---
    ("granaty_reczne", "f-1_1.jpg",   "F-1_Limonka_grenade.jpg"),
    ("granaty_reczne", "rgd-5_1.jpg", "RGD-5.jpg"),
    ("granaty_reczne", "rgn_1.jpg",   "RGN_grenade.jpg"),
    ("granaty_reczne", "rgo_1.jpg",   "RGO_grenade.jpg"),
    ("granaty_reczne", "rkg-3_1.jpg", "RKG-3.jpg"),
    ("granaty_reczne", "vog-25_1.jpg","VOG-25.jpg"),

    # --- miny ---
    ("miny", "pmn_1.jpg",    "PMN_mine.jpg"),
    ("miny", "pmn-2_1.jpg",  "PMN-2_mine.jpg"),
    ("miny", "ozm-72_1.jpg", "OZM-72.jpg"),
    ("miny", "pom-2_1.jpg",  "POM-2.jpg"),
    ("miny", "pfm-1_1.jpg",  "PFM-1_butterfly_mine.jpg"),
    ("miny", "mon-50_1.jpg", "MON-50.jpg"),
    ("miny", "mon-100_1.jpg","MON-100.jpg"),
    ("miny", "tm-57_1.jpg",  "TM-57.jpg"),
    ("miny", "tm-62_1.jpg",  "TM-62M.jpg"),
    ("miny", "ptm-3_1.jpg",  "PTM-3.jpg"),
    ("miny", "kpom-2_1.jpg", "KPOM-2.jpg"),
    ("miny", "umz_1.jpg",    "UMZ_mine_scattering_system.jpg"),
    ("miny", "vs-50_1.jpg",  "VS-50.jpg"),
]

API_URL = "https://commons.wikimedia.org/w/api.php"
HEADERS = {"User-Agent": "spw-fr-ebook/1.0 (educational-book-project)"}


def get_image_url(wiki_filename, width=500):
    """Get thumbnail URL from Wikimedia Commons API."""
    params = {
        "action": "query",
        "titles": f"File:{wiki_filename}",
        "prop": "imageinfo",
        "iiprop": "url",
        "iiurlwidth": str(width),
        "format": "json",
    }
    url = API_URL + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
        pages = data.get("query", {}).get("pages", {})
        for page in pages.values():
            ii = page.get("imageinfo", [])
            if ii:
                return ii[0].get("thumburl") or ii[0].get("url")
    except Exception as e:
        print(f"  API error for {wiki_filename}: {e}")
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

    for (subdir, local_name, wiki_name) in IMAGES:
        dest_dir = os.path.join(IMG_DIR, subdir)
        os.makedirs(dest_dir, exist_ok=True)
        dest_path = os.path.join(dest_dir, local_name)

        if os.path.exists(dest_path) and os.path.getsize(dest_path) > 1000:
            print(f"SKIP {subdir}/{local_name}")
            skip += 1
            continue

        print(f"GET  {subdir}/{local_name}  <-  {wiki_name}")
        url = get_image_url(wiki_name)
        if not url:
            print(f"  BRAK URL dla {wiki_name}")
            fail += 1
            failed_list.append((subdir, local_name, wiki_name))
            time.sleep(0.3)
            continue

        try:
            size = download_file(url, dest_path)
            print(f"  OK  {size//1024} KB")
            ok += 1
        except Exception as e:
            print(f"  BŁĄD pobierania: {e}")
            fail += 1
            failed_list.append((subdir, local_name, wiki_name))

        time.sleep(0.4)  # be polite to Wikimedia

    print(f"\n=== WYNIK: {ok} pobrano, {skip} pominięto, {fail} błędów ===")
    if failed_list:
        print("\nNie udało się pobrać:")
        for subdir, local_name, wiki_name in failed_list:
            print(f"  {subdir}/{local_name}  ({wiki_name})")


if __name__ == "__main__":
    main()

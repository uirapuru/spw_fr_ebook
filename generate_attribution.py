#!/usr/bin/env python3
"""Generate attribution page (zrodla_grafik.md) for all images in the e-book.

Queries Wikimedia Commons extmetadata API to get author, license, and URL for each image.
Run: python3 generate_attribution.py
"""

import os
import time
import json
import re
import urllib.request
import urllib.parse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(BASE_DIR, "images")
HEADERS = {"User-Agent": "spw-fr-ebook/1.0 (educational-book-project)"}
WP_API = "https://en.wikipedia.org/w/api.php"
COMMONS_API = "https://commons.wikimedia.org/w/api.php"

# ── Known direct Commons filenames ──────────────────────────────────────────
KNOWN_COMMONS = {
    # artyleria_holowana
    "artyleria_holowana/m-30_1.jpg":      "122_mm_howitzer_M1938_(M-30)_Batey_ha-Osef-1.jpg",
    "artyleria_holowana/m-46_1.jpg":      "M-46_130mm_field_gun_batey_ha-osef_1.jpg",
    "artyleria_holowana/d-1_1.jpg":       "152_mm_howitzer_D-1_batey_ha-osef_1.jpg",
    "artyleria_holowana/d-20_1.jpg":      "D-20_152mm_gun-howitzer.jpg",
    "artyleria_holowana/msta-b_1.jpg":    "2A65_howitzer.jpg",
    "artyleria_holowana/giatsint-b_1.jpg":"2A36_howitzer_batey_ha-osef_3.jpg",
    "artyleria_holowana/vasilek_1.jpg":   "2B9_Vasilek_automatic_mortar.jpg",
    "artyleria_holowana/podnos_1.jpg":    "2B14_Podnos_-_Nizhny_Tagil_2008.jpg",
    "artyleria_holowana/sani_1.jpg":      "2S12_Sani_mortar_system.jpg",
    # karabiny szturmowe
    "karabiny/aks-74u_1.jpg":  "AKS-74U_-_AM.jpg",
    "karabiny/ak-103_1.jpg":   "AK-103_-_AM.jpg",
    "karabiny/ak-15_1.jpg":    "AK-15_-_AM.jpg",
    "karabiny/an-94_1.jpg":    "AN-94_Abakan_-_AM.jpg",
    "karabiny/aek-971_1.jpg":  "AEK-971_-_AM.jpg",
    "karabiny/sr-3_1.jpg":     "SR-3M_Whirlwind_-_AM.jpg",
    "karabiny/as-val_1.jpg":   "AS_Val_-_AM.jpg",
    # karabiny maszynowe
    "karabiny_maszynowe/rpk_1.jpg":  "RPK_-_AM.jpg",
    "karabiny_maszynowe/rpl-20_1.jpg":"RPL-20.jpg",
    "karabiny_maszynowe/pk_1.jpg":   "PK_machine_gun_DD-SD-06-07351.jpg",
    "karabiny_maszynowe/pkp_1.jpg":  "PKP_Pecheneg_-_AM.jpg",
    "karabiny_maszynowe/dshk_1.jpg": "DShK_in_Afghanistan.jpg",
    "karabiny_maszynowe/nsv_1.jpg":  "UTES_12.7mm_machine_gun.jpg",
    "karabiny_maszynowe/kord_1.jpg": "Kord_(machine_gun)_-_AM.jpg",
    # karabiny snajperskie
    "karabiny_snajperskie/vss_1.jpg":   "VSS_Vintorez_-_AM.jpg",
    "karabiny_snajperskie/svd_1.jpg":   "SVD_Dragunov_-_AM.jpg",
    "karabiny_snajperskie/sv-98_1.jpg": "SV-98_-_AM.jpg",
    "karabiny_snajperskie/orsis_1.jpg": "Orsis_T-5000.jpg",
    "karabiny_snajperskie/ksvk_1.jpg":  "KSVK_12.7.jpg",
    "karabiny_snajperskie/osv-96_1.jpg":"OSV-96_MAKS-2009.jpg",
    "karabiny_snajperskie/lobaev_1.jpg":"Lobaev_SVLK-14S.jpg",
    # rpg i wyrzutnie
    "rpg_wyrzutnie/rpg-7_1.jpg":  "RPG-7_detached.jpg",
    "rpg_wyrzutnie/rpg-18_1.jpg": "RPG-18_-_AM.jpg",
    "rpg_wyrzutnie/rpg-22_1.jpg": "RPG-22_-_AM.jpg",
    "rpg_wyrzutnie/rpg-26_1.jpg": "RPG-26_-_AM.jpg",
    "rpg_wyrzutnie/rpg-27_1.jpg": "RPG-27_-_AM.jpg",
    "rpg_wyrzutnie/rpg-29_1.jpg": "RPG-29_-_AM.jpg",
    "rpg_wyrzutnie/rpg-30_1.jpg": "RPG-30.jpg",
    "rpg_wyrzutnie/rpg-32_1.jpg": "RPG-32.jpg",
    "rpg_wyrzutnie/rshg-1_1.jpg": "RShG-1.jpg",
    "rpg_wyrzutnie/shmel_1.jpg":  "RPO-A_Shmel_-_AM.jpg",
    "rpg_wyrzutnie/bur_1.jpg":    "MRO-A_Bur.jpg",
    # wyrzutnie granatow
    "wyrzutnie_granatow/gp-25_1.jpg":  "GP-25_-_AM.jpg",
    "wyrzutnie_granatow/gp-30_1.jpg":  "GP-30_-_AM.jpg",
    "wyrzutnie_granatow/gp-34_1.jpg":  "GP-34_-_AM.jpg",
    "wyrzutnie_granatow/ags-17_1.jpg": "AGS-17_DD-SC-86-00895.jpg",
    "wyrzutnie_granatow/ags-30_1.jpg": "AGS-30_-_AM.jpg",
    "wyrzutnie_granatow/ags-40_1.jpg": "AGS-40_Balkan.jpg",
    "wyrzutnie_granatow/gm-94_1.jpg":  "GM-94_-_AM.jpg",
    # pistolety i pm
    "pistolety_i_pm/pm_1.jpg":            "Makarov_DD-SC-84-10636.jpg",
    "pistolety_i_pm/tt_1.jpg":            "TT_Tokarev_1940.jpg",
    "pistolety_i_pm/aps_1.jpg":           "APS_Stechkin_-_AM.jpg",
    "pistolety_i_pm/pb_1.jpg":            "PB_silent_pistol_-_AM.jpg",
    "pistolety_i_pm/psm_1.jpg":           "PSM_pistol_-_AM.jpg",
    "pistolety_i_pm/mp-443_1.jpg":        "MP-443_Grach_-_AM.jpg",
    "pistolety_i_pm/gsh-18_1.jpg":        "GSh-18_-_AM.jpg",
    "pistolety_i_pm/sr-1_1.jpg":          "SR-1_Vektor_-_AM.jpg",
    "pistolety_i_pm/ots-33_1.jpg":        "OTs-33_Pernach_-_AM.jpg",
    "pistolety_i_pm/ots-23_1.jpg":        "OTs-23_Drotik_-_AM.jpg",
    "pistolety_i_pm/pp-91_1.jpg":         "PP-91_Kedr_-_AM.jpg",
    "pistolety_i_pm/pp-2000_1.jpg":       "PP-2000_-_AM.jpg",
    "pistolety_i_pm/pl-15_1.jpg":         "PL-15_pistol.jpg",
    "pistolety_i_pm/spp-1m_1.jpg":        "SPP-1M.jpg",
    "pistolety_i_pm/sps-underwater_1.jpg":"APS_underwater_rifle_-_AM.jpg",
    # granaty reczne
    "granaty_reczne/f-1_1.jpg":  "F-1_Limonka_grenade.jpg",
    "granaty_reczne/rgd-5_1.jpg":"RGD-5.jpg",
    "granaty_reczne/rgn_1.jpg":  "RGN_grenade.jpg",
    "granaty_reczne/rgo_1.jpg":  "RGO_grenade.jpg",
    "granaty_reczne/rkg-3_1.jpg":"RKG-3.jpg",
    "granaty_reczne/vog-25_1.jpg":"VOG-25.jpg",
    # miny
    "miny/pmn_1.jpg":    "PMN_mine.jpg",
    "miny/pmn-2_1.jpg":  "PMN-2_mine.jpg",
    "miny/ozm-72_1.jpg": "OZM-72.jpg",
    "miny/pom-2_1.jpg":  "POM-2.jpg",
    "miny/pfm-1_1.jpg":  "PFM-1_butterfly_mine.jpg",
    "miny/mon-50_1.jpg": "MON-50.jpg",
    "miny/mon-100_1.jpg":"MON-100.jpg",
    "miny/tm-57_1.jpg":  "TM-57.jpg",
    "miny/tm-62_1.jpg":  "TM-62M.jpg",
    "miny/ptm-3_1.jpg":  "PTM-3.jpg",
    "miny/kpom-2_1.jpg": "KPOM-2.jpg",
    "miny/umz_1.jpg":    "UMZ_mine_scattering_system.jpg",
    "miny/vs-50_1.jpg":  "VS-50_mine.jpg",  # corrected (was wrong image)
    # bwd (added v1.2)
    "bwd/bmd-1_1.jpg": "Vdvcompetition11.jpg",
    "bwd/bmd-2_1.jpg": "BMD-2_airborne_combat_vehicle.jpg",
    "bwd/bmd-3_1.jpg": "BMD-3_Army-2022_2022-08-20_2657.jpg",
    "bwd/bmd-4_1.jpg": "2008_Moscow_Victory_Day_Parade_-_BMD-4.jpg",
    # apc (mt-lb added v1.2)
    "apc/mt-lb_1.jpg": "RWS2017-37.jpg",
    # czolgi (t-62m corrected in v1.1)
    "czolgi/t-62m_1.jpg": "T-62M_-_Army-2023-14.jpg",
    # przeciwlotnicze (Strela-3 = SA-14 Gremlin, WP article has no pageimage)
    "przeciwlotnicze/strela-3_1.jpg": "SA-14_missile_and_launch_tube.jpg",
    # karabiny (AK-12 article has no pageimage)
    "karabiny/ak-12_1.jpg": "AK-12_-_Army-2023-12.jpg",
}

# ── Wikipedia article → Commons filename (via pageimages API, piprop=name) ──
# For _2 images: use tuple (article, image_index) to pick N-th image from article
WIKI_ARTICLES = {
    # czolgi
    "czolgi/t-55_1.jpg":       "T-55",
    "czolgi/t-62_1.jpg":       "T-62",
    "czolgi/t-72_1.jpg":       "T-72",
    "czolgi/t-72_2.jpg":       ("T-72", 1),
    "czolgi/t-80_1.jpg":       "T-80",
    "czolgi/t-80_2.jpg":       ("T-80", 1),
    "czolgi/t-90_1.jpg":       "T-90",
    "czolgi/t-90_2.jpg":       ("T-90", 1),
    "czolgi/2s25-sprut_1.jpg": "2S25 Sprut-SD",
    # bwp
    "bwp/bmp-1_1.jpg":  "BMP-1",
    "bwp/bmp-2_1.jpg":  "BMP-2",
    "bwp/bmp-2_2.jpg":  ("BMP-2", 1),
    "bwp/bmp-3_1.jpg":  "BMP-3",
    "bwp/bmp-3_2.jpg":  ("BMP-3", 1),
    # apc
    "apc/btr-80_1.jpg": "BTR-80",
    "apc/btr-80_2.jpg": ("BTR-80", 1),
    "apc/btr-90_1.jpg": "BTR-90",
    "apc/btr-90_2.jpg": ("BTR-90", 1),
    "apc/tigr_1.jpg":   "GAZ Tigr",
    "apc/tigr_2.jpg":   ("GAZ Tigr", 1),
    # artyleria_holowana (not in KNOWN_COMMONS)
    "artyleria_holowana/d-30_1.jpg": "D-30 howitzer",
    "artyleria_holowana/mt-12_1.jpg":"MT-12 Rapira",
    # artyleria_samobiezna
    "artyleria_samobiezna/2s1_1.jpg":       "2S1 Gvozdika",
    "artyleria_samobiezna/2s19-msta-s_1.jpg":"2S19 Msta",
    "artyleria_samobiezna/2s23_1.jpg":      "2S23 Nona-SVK",
    "artyleria_samobiezna/2s3_1.jpg":       "2S3 Akatsiya",
    "artyleria_samobiezna/2s4_1.jpg":       "2S4 Tyulpan",
    "artyleria_samobiezna/2s5_1.jpg":       "2S5 Giatsint-S",
    "artyleria_samobiezna/2s9_1.jpg":       "2S9 Nona",
    # przeciwlotnicze
    "przeciwlotnicze/s-300_1.jpg":      "S-300 missile system",
    "przeciwlotnicze/s-400_1.jpg":      "S-400",
    "przeciwlotnicze/pantsir_1.jpg":    "Pantsir missile system",
    "przeciwlotnicze/tor_1.jpg":        "Tor missile system",
    "przeciwlotnicze/igla_1.jpg":       "9K38 Igla",
    "przeciwlotnicze/strela-3_1.jpg":   "9K34 Strela-3",
    "przeciwlotnicze/verba_1.jpg":      "9K333 Verba",
    "przeciwlotnicze/zu-23-2_1.jpg":    "ZU-23-2",
    "przeciwlotnicze/zsu-23-4_1.jpg":   "ZSU-23-4",
    "przeciwlotnicze/s-60_1.jpg":       "57 mm AZP S-60",
    "przeciwlotnicze/2k22-tunguska_1.jpg":"2K22 Tunguska",
    "przeciwlotnicze/9k33-osa_1.jpg":   "9K33 Osa",
    # karabiny (not in KNOWN_COMMONS)
    "karabiny/ak-12_1.jpg": "AK-12",
    "karabiny/ak-74_1.jpg": "AK-74",
    "karabiny/akm_1.jpg":   "AKM",
    # lotnictwo
    "lotnictwo/ka-52_1.jpg":   "Kamov Ka-52",
    "lotnictwo/ka-52_2.jpg":   ("Kamov Ka-52", 1),
    "lotnictwo/mi-24_1.jpg":   "Mil Mi-24",
    "lotnictwo/mi-24_2.jpg":   ("Mil Mi-24", 1),
    "lotnictwo/mi-28_1.jpg":   "Mil Mi-28",
    "lotnictwo/mi-28_2.jpg":   ("Mil Mi-28", 1),
    "lotnictwo/su-25_1.jpg":   "Sukhoi Su-25",
    "lotnictwo/su-25_2.jpg":   ("Sukhoi Su-25", 1),
    "lotnictwo/su-27_1.jpg":   "Sukhoi Su-27",
    "lotnictwo/su-27_2.jpg":   ("Sukhoi Su-27", 1),
    # lotnictwo — samoloty (dodane v1.2)
    "lotnictwo/su-24m_1.jpg":  "Sukhoi Su-24",
    "lotnictwo/su-34_1.jpg":   "Sukhoi Su-34",
    "lotnictwo/su-35s_1.jpg":  "Sukhoi Su-35",
    "lotnictwo/mig-29_1.jpg":  "Mikoyan MiG-29",
    "lotnictwo/mig-31k_1.jpg": "Mikoyan MiG-31",
    "lotnictwo/tu-22m3_1.jpg": "Tupolev Tu-22M",
    "lotnictwo/tu-95ms_1.jpg": "Tupolev Tu-95",
    "lotnictwo/tu-160_1.jpg":  "Tupolev Tu-160",
    # lotnictwo — śmigłowce (dodane v1.2)
    "lotnictwo/mi-8_1.jpg":    "Mil Mi-8",
    "lotnictwo/mi-35m_1.jpg":  "Mil Mi-35",
    "lotnictwo/mi-26_1.jpg":   "Mil Mi-26",
    # drony bojowe (dodane v1.2)
    "drony_bojowe/geran-2_1.jpg":  "HESA Shahed 136",
    "drony_bojowe/geran-1_1.jpg":  "HESA Shahed 131",
    "drony_bojowe/lancet_1.jpg":   "ZALA Lancet",
    "drony_bojowe/orlan-10_1.jpg": "STC Orlan-10",
    "drony_bojowe/orlan-30_1.jpg": "STC Orlan-10",
    "drony_bojowe/gerbera_1.jpg":  "Gerbera (drone)",
    # przeciwpancerne
    "przeciwpancerne/fagot_1.jpg":   "9M111 Fagot",
    "przeciwpancerne/konkurs_1.jpg": "9M113 Konkurs",
    "przeciwpancerne/kornet_1.jpg":  "9M133 Kornet",
    "przeciwpancerne/metis_1.jpg":   "9K115 Metis",
    "przeciwpancerne/metis-m_1.jpg": "9K115-2 Metis-M",
    # artyleria samobiezna (2s40 dodane)
    "artyleria_samobiezna/2s40-floks_1.jpg": "2S40 Floks",
}

# Ordering of images in the output (by directory category)
CATEGORY_ORDER = [
    "lotnictwo", "drony_bojowe",
    "czolgi", "bwd", "bwp", "apc",
    "artyleria_samobiezna", "artyleria_holowana",
    "przeciwlotnicze", "przeciwpancerne",
    "karabiny", "karabiny_maszynowe", "karabiny_snajperskie",
    "rpg_wyrzutnie", "wyrzutnie_granatow",
    "pistolety_i_pm", "granaty_reczne", "miny",
]


def api_get(url, params):
    full_url = url + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(full_url, headers=HEADERS)
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                return json.loads(resp.read())
        except Exception as e:
            if attempt < 2:
                time.sleep(2 ** attempt)
            else:
                print(f"  ERR {e}")
    return {}


def get_wp_pageimage_name(article):
    """Return the Commons filename (without 'File:' prefix) for an article's main image."""
    data = api_get(WP_API, {
        "action": "query",
        "titles": article,
        "prop": "pageimages",
        "piprop": "name",
        "format": "json",
        "redirects": "1",
    })
    for page in data.get("query", {}).get("pages", {}).values():
        name = page.get("pageimage")
        if name:
            return name
    return None


def get_wp_article_images(article):
    """Return list of Commons filenames (jpg only) for all images in the article."""
    data = api_get(WP_API, {
        "action": "query",
        "titles": article,
        "prop": "images",
        "imlimit": "50",
        "format": "json",
        "redirects": "1",
    })
    result = []
    for page in data.get("query", {}).get("pages", {}).values():
        for img in page.get("images", []):
            title = img.get("title", "")
            # Strip "File:" prefix, keep only jpg/jpeg
            if title.lower().startswith("file:"):
                fname = title[5:]
                if fname.lower().endswith((".jpg", ".jpeg", ".png")):
                    result.append(fname)
    return result


def get_commons_metadata(commons_filename):
    """Query Commons extmetadata for Artist, LicenseShortName, DescriptionUrl."""
    data = api_get(COMMONS_API, {
        "action": "query",
        "titles": f"File:{commons_filename}",
        "prop": "imageinfo",
        "iiprop": "extmetadata|url",
        "format": "json",
    })
    for page in data.get("query", {}).get("pages", {}).values():
        ii = page.get("imageinfo", [{}])
        if not ii:
            return None
        info = ii[0]
        meta = info.get("extmetadata", {})

        def val(key):
            v = meta.get(key, {}).get("value", "") or ""
            # strip HTML tags
            v = re.sub(r"<[^>]+>", "", v).strip()
            return v

        artist = val("Artist") or val("Credit") or "—"
        license_name = val("LicenseShortName") or val("License") or "—"
        desc_url = info.get("descriptionurl") or (
            "https://commons.wikimedia.org/wiki/File:" +
            urllib.parse.quote(commons_filename.replace(" ", "_"))
        )
        return {
            "commons_filename": commons_filename,
            "artist": artist,
            "license": license_name,
            "url": desc_url,
        }
    return None


def resolve_commons_filename(local_key):
    """Resolve the Commons filename for a local image path key."""
    if local_key in KNOWN_COMMONS:
        return KNOWN_COMMONS[local_key]

    if local_key in WIKI_ARTICLES:
        entry = WIKI_ARTICLES[local_key]
        if isinstance(entry, str):
            # Simple article title — get pageimage
            name = get_wp_pageimage_name(entry)
            time.sleep(0.5)
            return name
        else:
            # Tuple (article, index) — get N-th image from article image list
            article, idx = entry
            images = get_wp_article_images(article)
            time.sleep(0.5)
            if len(images) > idx:
                return images[idx]
    return None


def collect_all_images():
    """Build ordered list of (local_key, local_path) for all images."""
    result = []
    for cat in CATEGORY_ORDER:
        cat_dir = os.path.join(IMG_DIR, cat)
        if not os.path.isdir(cat_dir):
            continue
        files = sorted(f for f in os.listdir(cat_dir) if f.lower().endswith(".jpg"))
        for fname in files:
            local_key = f"{cat}/{fname}"
            local_path = os.path.join(cat_dir, fname)
            result.append((local_key, local_path))
    return result


def main():
    images = collect_all_images()
    total = len(images)
    print(f"Znaleziono {total} obrazów. Pobieranie metadanych z Commons...\n")

    entries = []   # list of (local_key, metadata_dict or None, commons_filename or None)
    failed = []

    for i, (local_key, _) in enumerate(images, 1):
        print(f"[{i:3}/{total}] {local_key}", end=" ... ", flush=True)

        commons_name = resolve_commons_filename(local_key)
        if not commons_name:
            print("BRAK nazwy Commons")
            entries.append((local_key, None, None))
            failed.append(local_key)
            continue

        time.sleep(0.6)  # polite to APIs
        meta = get_commons_metadata(commons_name)
        if meta:
            print(f"OK  [{meta['license']}]  {meta['artist'][:40]}")
            entries.append((local_key, meta, commons_name))
        else:
            print(f"BRAK metadanych (Commons: {commons_name})")
            # Still include the URL even without metadata
            desc_url = (
                "https://commons.wikimedia.org/wiki/File:" +
                urllib.parse.quote(commons_name.replace(" ", "_"))
            )
            entries.append((local_key, {"commons_filename": commons_name,
                                        "artist": "—",
                                        "license": "—",
                                        "url": desc_url}, commons_name))
            failed.append(local_key)
        time.sleep(0.5)

    # ── Generate markdown ─────────────────────────────────────────────────
    lines = [
        "# Źródła grafik",
        "",
        "Wszystkie grafiki użyte w podręczniku pochodzą z **Wikimedia Commons** "
        "i są dostępne na wolnych licencjach. Poniżej zestawienie każdego obrazu "
        "z podaniem autora, licencji i odnośnika do strony źródłowej.",
        "",
        "Każdy punkt zawiera nazwę pliku, autora, licencję i klikalny odnośnik URL "
        "do strony pliku w Wikimedia Commons.",
        "",
    ]

    for idx, (local_key, meta, commons_name) in enumerate(entries, 1):
        file_name = os.path.basename(local_key)
        if meta:
            artist = meta["artist"].replace("|", "/").replace("\n", " ")
            if len(artist) > 80:
                artist = artist[:77] + "..."
            license_str = meta["license"]
            url = meta["url"]
            link = f"[Wikimedia Commons](<{url}>)"
        else:
            artist = "—"
            license_str = "—"
            link = "—"
        lines.append(f"Zdj. {idx}. `{file_name}`, **autor**: {artist}, lic. {license_str},")
        lines.append(f"**url**: {link}")
        lines.append("")

    out_path = os.path.join(BASE_DIR, "zrodla_grafik.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print(f"\n✓ Zapisano: {out_path}")
    print(f"  Łącznie: {total} obrazów,  błędy: {len(failed)}")
    if failed:
        print("\nObrazy bez metadanych:")
        for k in failed:
            print(f"  {k}")


if __name__ == "__main__":
    main()

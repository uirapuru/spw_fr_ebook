#!/usr/bin/env python3
"""Add image references to markdown files that don't have them."""

import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(BASE_DIR, "images")

# Explicit mapping: (category_dir, md_basename) -> image_filename
# Only needed when image name != md_basename + "_1.jpg"
EXPLICIT_MAP = {
    ("artyleria_holowana", "2b9-vasilek"):   "vasilek_1.jpg",
    ("artyleria_holowana", "2b14-podnos"):   "podnos_1.jpg",
    ("artyleria_holowana", "2s12-sani"):     "sani_1.jpg",
    ("artyleria_holowana", "giatsint-b"):    "giatsint-b_1.jpg",
    ("artyleria_holowana", "msta-b"):        "msta-b_1.jpg",
    ("karabiny_maszynowe", "pkp-pecheneg"):  "pkp_1.jpg",
    ("karabiny_snajperskie", "vss-vintorez"): "vss_1.jpg",
    ("karabiny_snajperskie", "orsis-t5000"): "orsis_1.jpg",
    ("karabiny_snajperskie", "lobaev"):      "lobaev_1.jpg",
    ("pistolety_i_pm",  "pm"):               "pm_1.jpg",
    ("pistolety_i_pm",  "tt"):               "tt_1.jpg",
    ("pistolety_i_pm",  "aps"):              "aps_1.jpg",
    ("pistolety_i_pm",  "pb"):               "pb_1.jpg",
    ("pistolety_i_pm",  "psm"):              "psm_1.jpg",
    ("pistolety_i_pm",  "mp-443"):           "mp-443_1.jpg",
    ("pistolety_i_pm",  "gsh-18"):           "gsh-18_1.jpg",
    ("pistolety_i_pm",  "sr-1"):             "sr-1_1.jpg",
    ("pistolety_i_pm",  "ots-33"):           "ots-33_1.jpg",
    ("pistolety_i_pm",  "ots-23"):           "ots-23_1.jpg",
    ("pistolety_i_pm",  "pp-91"):            "pp-91_1.jpg",
    ("pistolety_i_pm",  "pp-2000"):          "pp-2000_1.jpg",
    ("pistolety_i_pm",  "pl-14"):            "pl-15_1.jpg",
    ("pistolety_i_pm",  "spp-1m"):           "spp-1m_1.jpg",
    ("pistolety_i_pm",  "sps-underwater"):   "sps-underwater_1.jpg",
    ("rpg_wyrzutnie",   "shmel"):            "shmel_1.jpg",
    ("rpg_wyrzutnie",   "bur"):              "bur_1.jpg",
    ("rpg_wyrzutnie",   "rshg-1"):           "rshg-1_1.jpg",
    ("wyrzutnie_granatow", "agk-17"):        "ags-17_1.jpg",
    ("wyrzutnie_granatow", "agk-30"):        "ags-30_1.jpg",
    ("wyrzutnie_granatow", "agk-40"):        "ags-40_1.jpg",
    ("granaty_reczne",  "f-1"):              "f-1_1.jpg",
    ("granaty_reczne",  "rgd-5"):            "rgd-5_1.jpg",
    ("granaty_reczne",  "rgn"):              "rgn_1.jpg",
    ("granaty_reczne",  "rgo"):              "rgo_1.jpg",
    ("granaty_reczne",  "rkg-3"):            "rkg-3_1.jpg",
    ("granaty_reczne",  "vog-25"):           "vog-25_1.jpg",
    ("miny", "pmn"):                         "pmn_1.jpg",
    ("miny", "pmn-2"):                       "pmn-2_1.jpg",
    ("miny", "ozm-72"):                      "ozm-72_1.jpg",
    ("miny", "pom-2"):                       "pom-2_1.jpg",
    ("miny", "pfm-1"):                       "pfm-1_1.jpg",
    ("miny", "mon-50"):                      "mon-50_1.jpg",
    ("miny", "mon-100"):                     "mon-100_1.jpg",
    ("miny", "tm-57"):                       "tm-57_1.jpg",
    ("miny", "tm-62"):                       "tm-62_1.jpg",
    ("miny", "ptm-3"):                       "ptm-3_1.jpg",
    ("miny", "kpom-2"):                      "kpom-2_1.jpg",
    ("miny", "umz"):                         "umz_1.jpg",
    ("miny", "vs-50"):                       "vs-50_1.jpg",
}

# Weapon names for alt text
WEAPON_NAMES = {
    ("artyleria_holowana", "m-30"):         "Haubica M-30 122 mm",
    ("artyleria_holowana", "m-46"):         "Armata M-46 130 mm",
    ("artyleria_holowana", "d-1"):          "Haubica D-1 152 mm",
    ("artyleria_holowana", "d-20"):         "Haubica-armata D-20 152 mm",
    ("artyleria_holowana", "msta-b"):       "Haubica 2A65 Msta-B 152 mm",
    ("artyleria_holowana", "giatsint-b"):   "Armata 2A36 Giacynt-B 152 mm",
    ("artyleria_holowana", "2b9-vasilek"):  "Moździerz automatyczny 2B9 Wasilek",
    ("artyleria_holowana", "2b14-podnos"):  "Moździerz piechoty 2B14 Podnos",
    ("artyleria_holowana", "2s12-sani"):    "Ciężki moździerz 2S12 Sani",
    ("karabiny", "aks-74u"):      "AKS-74U — skrócony karabin szturmowy",
    ("karabiny", "ak-103"):       "AK-103 — karabin szturmowy 7,62 mm",
    ("karabiny", "ak-15"):        "AK-15 — karabin szturmowy nowej generacji",
    ("karabiny", "an-94"):        "AN-94 Abakan — karabin szturmowy",
    ("karabiny", "aek-971"):      "AEK-971 — karabin szturmowy ze zrównoważoną automatyką",
    ("karabiny", "sr-3"):         "SR-3 Wihr — kompaktowy karabin szturmowy",
    ("karabiny", "as-val"):       "AS Val — tłumiony karabin szturmowy",
    ("karabiny_maszynowe", "rpk"):         "RPK — ręczny karabin maszynowy",
    ("karabiny_maszynowe", "rpl-20"):      "RPL-20 — ręczny karabin maszynowy",
    ("karabiny_maszynowe", "pk"):          "PK/PKM — karabin maszynowy ogólnego przeznaczenia",
    ("karabiny_maszynowe", "pkp-pecheneg"):"PKP Pieczenieg — karabin maszynowy",
    ("karabiny_maszynowe", "dshk"):        "DShK — ciężki karabin maszynowy 12,7 mm",
    ("karabiny_maszynowe", "nsv"):         "NSW Utes — ciężki karabin maszynowy 12,7 mm",
    ("karabiny_maszynowe", "kord"):        "Kord — ciężki karabin maszynowy 12,7 mm",
    ("karabiny_snajperskie", "vss-vintorez"): "VSS Wintorez — tłumiony karabin snajperski",
    ("karabiny_snajperskie", "svd"):          "SVD Dragunow — karabin snajperski",
    ("karabiny_snajperskie", "sv-98"):        "SV-98 — karabin snajperski bolt-action",
    ("karabiny_snajperskie", "orsis-t5000"):  "Orsis T-5000 — precyzyjny karabin snajperski",
    ("karabiny_snajperskie", "ksvk"):         "KSVK 12,7 mm — wielkokalibrowy karabin snajperski",
    ("karabiny_snajperskie", "osv-96"):       "OSV-96 — wielkokalibrowy karabin snajperski",
    ("karabiny_snajperskie", "lobaev"):       "Lobaev SVLK-14S — karabin dalekiego zasięgu",
    ("rpg_wyrzutnie", "rpg-7"):    "RPG-7 — granatnik przeciwpancerny",
    ("rpg_wyrzutnie", "rpg-18"):   "RPG-18 Mucha — jednorazowy granatnik",
    ("rpg_wyrzutnie", "rpg-22"):   "RPG-22 Netto — jednorazowy granatnik",
    ("rpg_wyrzutnie", "rpg-26"):   "RPG-26 Agleń — jednorazowy granatnik",
    ("rpg_wyrzutnie", "rpg-27"):   "RPG-27 Tavolga — ciężki granatnik",
    ("rpg_wyrzutnie", "rpg-29"):   "RPG-29 Wampir — granatnik przeciwpancerny",
    ("rpg_wyrzutnie", "rpg-30"):   "RPG-30 Kryuk — granatnik z systemem APS",
    ("rpg_wyrzutnie", "rpg-32"):   "RPG-32 Hashim — modułowy granatnik",
    ("rpg_wyrzutnie", "rshg-1"):   "RShG-1 — granatnik termobaryczny",
    ("rpg_wyrzutnie", "shmel"):    "RPO-A Szmiel — wyrzutnia termobaryczna",
    ("rpg_wyrzutnie", "bur"):      "MRO-A Bur — lekka wyrzutnia termobaryczna",
    ("wyrzutnie_granatow", "gp-25"):  "GP-25 Kostior — granatnik podlufowy",
    ("wyrzutnie_granatow", "gp-30"):  "GP-30 Obuwka — granatnik podlufowy",
    ("wyrzutnie_granatow", "gp-34"):  "GP-34 — granatnik podlufowy Ratnik",
    ("wyrzutnie_granatow", "agk-17"): "AGS-17 Płamia — automatyczny granatnik 30 mm",
    ("wyrzutnie_granatow", "agk-30"): "AGS-30 — automatyczny granatnik 30 mm",
    ("wyrzutnie_granatow", "agk-40"): "AGS-40 Bałkan — automatyczny granatnik 40 mm",
    ("wyrzutnie_granatow", "gm-94"):  "GM-94 — rewolwerowy granatnik pump-action",
    ("pistolety_i_pm", "pm"):          "Pistolet PM Makarow",
    ("pistolety_i_pm", "tt"):          "Pistolet TT Tokariew",
    ("pistolety_i_pm", "aps"):         "APS Steczkin — pistolet maszynowy",
    ("pistolety_i_pm", "pb"):          "PB (6P9) — tłumiony pistolet",
    ("pistolety_i_pm", "psm"):         "PSM — ultrakompaktowy pistolet",
    ("pistolety_i_pm", "mp-443"):      "MP-443 Grach — pistolet 9×19 mm",
    ("pistolety_i_pm", "gsh-18"):      "GSz-18 — pistolet 9×19 mm",
    ("pistolety_i_pm", "sr-1"):        "SR-1 Wektor — pistolet wysokopenetracyjny",
    ("pistolety_i_pm", "ots-33"):      "OTs-33 Piernacz — pistolet maszynowy",
    ("pistolety_i_pm", "ots-23"):      "OTs-23 Drotik — pistolet maszynowy",
    ("pistolety_i_pm", "pp-91"):       "PP-91 Kedr — pistolet maszynowy",
    ("pistolety_i_pm", "pp-2000"):     "PP-2000 — pistolet maszynowy",
    ("pistolety_i_pm", "pl-14"):       "PL-15 Lebiediew — pistolet 9×19 mm",
    ("pistolety_i_pm", "spp-1m"):      "SPP-1M — pistolet podwodny",
    ("pistolety_i_pm", "sps-underwater"): "APS podwodny — karabinek podwodny",
    ("granaty_reczne", "f-1"):   "F-1 Limonka — granat defensywny",
    ("granaty_reczne", "rgd-5"): "RGD-5 — granat ofensywny",
    ("granaty_reczne", "rgn"):   "RGN — granat ofensywny z zapalnikiem uderzeniowym",
    ("granaty_reczne", "rgo"):   "RGO — granat defensywny z zapalnikiem uderzeniowym",
    ("granaty_reczne", "rkg-3"): "RKG-3 — granat przeciwpancerny kumulacyjny",
    ("granaty_reczne", "vog-25"):"VOG-25 — nabój do granatnika podlufowego",
    ("miny", "pmn"):    "Mina PMN — nacisgowa mina przeciwpiechotna",
    ("miny", "pmn-2"):  "Mina PMN-2 — plastikowa mina przeciwpiechotna",
    ("miny", "ozm-72"): "OZM-72 — wyskakująca mina odłamkowa",
    ("miny", "pom-2"):  "POM-2 — rozsypywana mina odłamkowa",
    ("miny", "pfm-1"):  "PFM-1 Motyl — lotnicza mina rozsypywana",
    ("miny", "mon-50"): "MON-50 — kierunkowa mina odłamkowa",
    ("miny", "mon-100"):"MON-100 — duża kierunkowa mina odłamkowa",
    ("miny", "tm-57"):  "TM-57 — ciężka mina przeciwpancerna",
    ("miny", "tm-62"):  "TM-62M — mina przeciwpancerna",
    ("miny", "ptm-3"):  "PTM-3 — rozsypywana mina przeciwpancerna",
    ("miny", "kpom-2"): "KPOM-2 — kasetowy element minowy",
    ("miny", "umz"):    "UMZ — naziemny system rozsypywania min",
    ("miny", "vs-50"):  "VS-50 — mina nacisgowa plastikowa",
    # also files that already have img but maybe some don't
    ("przeciwlotnicze", "strela-3"):   "9K34 Striełła-3 — MANPADS",
    ("przeciwpancerne", "konkurs"):    "9M113 Konkurs — ppk",
    ("przeciwpancerne", "kornet"):     "9M133 Kornet — ppk",
    ("przeciwpancerne", "metis"):      "9K115 Metis — lekki ppk",
    ("przeciwpancerne", "metis-m"):    "9K115-2 Metis-M — lekki ppk",
}


def has_image(content):
    return "![" in content


def get_image_path(category, md_base):
    """Return (rel_img_path, alt_text) or (None, None)."""
    # Check explicit map
    key = (category, md_base)
    if key in EXPLICIT_MAP:
        img_name = EXPLICIT_MAP[key]
    else:
        img_name = md_base + "_1.jpg"

    img_abs = os.path.join(IMG_DIR, category, img_name)
    if os.path.exists(img_abs) and os.path.getsize(img_abs) > 500:
        rel_path = f"../images/{category}/{img_name}"
        alt = WEAPON_NAMES.get(key, md_base.replace("-", " ").title())
        return rel_path, alt
    return None, None


def add_image_to_file(filepath, rel_img, alt_text):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    if has_image(content):
        return False  # already has image

    # Find insertion point: after the h1 + optional h3 + first ---
    lines = content.split("\n")
    insert_after = 0
    found_sep = False
    for i, line in enumerate(lines):
        if line.strip() == "---" and i > 0:
            insert_after = i
            found_sep = True
            break

    if not found_sep:
        # Insert after the first heading
        for i, line in enumerate(lines):
            if line.startswith("# ") or line.startswith("### "):
                insert_after = i
                break

    img_block = [
        "",
        f'![{alt_text}]({rel_img})',
        "",
    ]

    new_lines = lines[:insert_after + 1] + img_block + lines[insert_after + 1:]
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(new_lines))
    return True


def main():
    categories = [
        "czolgi", "bwp", "apc", "artyleria_samobiezna", "artyleria_holowana",
        "przeciwlotnicze", "przeciwpancerne", "lotnictwo",
        "karabiny", "karabiny_maszynowe", "karabiny_snajperskie",
        "rpg_wyrzutnie", "wyrzutnie_granatow", "pistolety_i_pm",
        "granaty_reczne", "miny",
    ]

    updated = 0
    skipped = 0
    no_img = []

    for cat in categories:
        cat_dir = os.path.join(BASE_DIR, cat)
        if not os.path.isdir(cat_dir):
            continue
        for fname in sorted(os.listdir(cat_dir)):
            if not fname.endswith(".md"):
                continue
            md_base = fname[:-3]
            filepath = os.path.join(cat_dir, fname)

            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            if has_image(content):
                skipped += 1
                continue

            rel_img, alt = get_image_path(cat, md_base)
            if not rel_img:
                no_img.append(f"{cat}/{fname}")
                continue

            if add_image_to_file(filepath, rel_img, alt):
                print(f"UPDATED {cat}/{fname}  -> {rel_img}")
                updated += 1

    print(f"\n=== WYNIK: {updated} zaktualizowano, {skipped} już miało, {len(no_img)} bez obrazu ===")
    if no_img:
        print("\nBez obrazu:")
        for f in no_img:
            print(f"  {f}")


if __name__ == "__main__":
    main()

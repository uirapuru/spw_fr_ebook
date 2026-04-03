#!/usr/bin/env python3
"""Download images for new e-book entries (aircraft, helicopters, drones)."""

import os, time, json, urllib.request, urllib.parse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(BASE_DIR, "images")
HEADERS = {"User-Agent": "spw-fr-ebook/1.0 (educational-book-project)"}
WP_API = "https://en.wikipedia.org/w/api.php"
COMMONS_API = "https://commons.wikimedia.org/w/api.php"

# (local_dir, local_filename, wikipedia_article_OR commons:FILENAME)
IMAGES = [
    # --- lotnictwo: samoloty ---
    ("lotnictwo", "su-24m_1.jpg",   "wp:Sukhoi Su-24"),
    ("lotnictwo", "su-34_1.jpg",    "wp:Sukhoi Su-34"),
    ("lotnictwo", "su-35s_1.jpg",   "wp:Sukhoi Su-35"),
    ("lotnictwo", "mig-29_1.jpg",   "wp:Mikoyan MiG-29"),
    ("lotnictwo", "mig-31k_1.jpg",  "wp:Mikoyan MiG-31"),
    ("lotnictwo", "tu-22m3_1.jpg",  "wp:Tupolev Tu-22M"),
    ("lotnictwo", "tu-95ms_1.jpg",  "wp:Tupolev Tu-95"),
    ("lotnictwo", "tu-160_1.jpg",   "wp:Tupolev Tu-160"),
    # --- lotnictwo: śmigłowce ---
    ("lotnictwo", "mi-8_1.jpg",     "wp:Mil Mi-8"),
    ("lotnictwo", "mi-35m_1.jpg",   "wp:Mil Mi-35"),
    ("lotnictwo", "mi-26_1.jpg",    "wp:Mil Mi-26"),
    # --- drony bojowe ---
    ("drony_bojowe", "geran-2_1.jpg",  "wp:HESA Shahed 136"),
    ("drony_bojowe", "orlan-10_1.jpg", "wp:STC Orlan-10"),
    ("drony_bojowe", "lancet_1.jpg",   "wp:ZALA Lancet"),
    ("drony_bojowe", "geran-1_1.jpg",  "wp:HESA Shahed 131"),
    ("drony_bojowe", "orlan-30_1.jpg", "wp:STC Orlan-10"),  # same family
    ("drony_bojowe", "gerbera_1.jpg",  "wp:Gerbera (drone)"),
]


def get_wp_pageimage(article):
    params = {"action": "query", "titles": article,
              "prop": "pageimages", "pithumbsize": "600",
              "format": "json", "redirects": "1"}
    url = WP_API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            data = json.loads(r.read())
        for page in data.get("query", {}).get("pages", {}).values():
            thumb = page.get("thumbnail")
            if thumb:
                return thumb.get("source")
    except Exception as e:
        print(f"  WP API error: {e}")
    return None


def download(url, dest):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30) as r:
        data = r.read()
    with open(dest, "wb") as f:
        f.write(data)
    return len(data)


def main():
    ok = fail = skip = 0
    for (subdir, local_name, source) in IMAGES:
        dest_dir = os.path.join(IMG_DIR, subdir)
        os.makedirs(dest_dir, exist_ok=True)
        dest = os.path.join(dest_dir, local_name)

        if os.path.exists(dest) and os.path.getsize(dest) > 1000:
            print(f"SKIP {subdir}/{local_name}")
            skip += 1
            continue

        print(f"GET  {subdir}/{local_name}", end=" ... ", flush=True)

        article = source[3:] if source.startswith("wp:") else None
        url = get_wp_pageimage(article) if article else None

        if not url:
            print("BRAK URL")
            fail += 1
            time.sleep(0.5)
            continue

        try:
            size = download(url, dest)
            print(f"OK {size//1024} KB")
            ok += 1
        except Exception as e:
            print(f"BŁĄD: {e}")
            fail += 1
        time.sleep(0.7)

    print(f"\n=== {ok} pobrano, {skip} pominięto, {fail} błędów ===")


if __name__ == "__main__":
    main()

# Instrukcja obsługi i rozbudowy e-booka

## Co zostało zrobione

### Struktura projektu

```
spw_fr_ebook/
├── index.md                  ← strona główna (tabela kategorii)
├── spis_tresci.md            ← pełny spis treści z linkami
├── INSTRUKCJA.md             ← ten plik
├── images/                   ← wszystkie obrazy (138 plików)
│   ├── czolgi/
│   ├── bwp/
│   ├── apc/
│   ├── artyleria_samobiezna/
│   ├── artyleria_holowana/
│   ├── przeciwlotnicze/
│   ├── przeciwpancerne/
│   ├── lotnictwo/
│   ├── karabiny/
│   ├── karabiny_maszynowe/
│   ├── karabiny_snajperskie/
│   ├── rpg_wyrzutnie/
│   ├── wyrzutnie_granatow/
│   ├── pistolety_i_pm/
│   ├── granaty_reczne/
│   └── miny/
├── czolgi/                   ← 7 pojazdów (T-55 do 2S25 Sprut-SD)
├── bwp/                      ← 3 wozy (BMP-1, BMP-2, BMP-3)
├── apc/                      ← 3 pojazdy (BTR-80, BTR-90, Tigr)
├── artyleria_samobiezna/     ← 8 pojazdów (2S1 do 2S40, + 2S19 Msta-S)
├── artyleria_holowana/       ← 11 dział i moździerzy
├── przeciwlotnicze/          ← 12 systemów (ZU-23-2 do S-400)
├── przeciwpancerne/          ← 5 ppk (Fagot do Kornet)
├── lotnictwo/                ← 5 statków powietrznych
├── karabiny/                 ← 10 karabinów szturmowych
├── karabiny_maszynowe/       ← 7 karabinów maszynowych
├── karabiny_snajperskie/     ← 7 karabinów snajperskich
├── rpg_wyrzutnie/            ← 11 granatników i wyrzutni
├── wyrzutnie_granatow/       ← 7 wyrzutni granatów
├── pistolety_i_pm/           ← 15 pistoletów i PM
├── granaty_reczne/           ← 6 granatów
└── miny/                     ← 13 min
```

Łącznie: **130 plików treści**, **138 obrazów**, **16 kategorii**, **143 hasła** (index.md liczy 143, spis_tresci.md jest autorytatywny).

### Zawartość kategorii (stan kwiecień 2026)

| # | Kategoria | Liczba | Hasła |
|---|-----------|--------|-------|
| 1 | Czołgi | 7 | T-55, T-62, T-62M, T-72, T-80, T-90, 2S25 Sprut-SD |
| 2 | BWP | 3 | BMP-1, BMP-2, BMP-3 |
| 3 | APC | 3 | BTR-80, BTR-90, Tigr |
| 4 | Art. samobieżna | 8 | 2S19 Msta-S, 2S1, 2S3, 2S4, 2S5, 2S9, 2S23, 2S40 |
| 5 | Art. holowana | 11 | D-30, M-30, M-46, D-1, D-20, Msta-B, Giacynt-B, MT-12, 2B9, 2B14, 2S12 |
| 6 | Systemy plot. | 12 | ZU-23-2, ZSU-23-4, S-60, 2K22 Tunguska, 9K33 Osa, Tor, Pancyr-S1, Striełła-3, Igła, Werba, S-300, S-400 |
| 7 | ATGM | 5 | Fagot, Konkurs, Metis, Metis-M, Kornet |
| 8 | Lotnictwo | 5 | Mi-24, Mi-28, Ka-52, Su-25, Su-27 |
| 9 | Karabiny szturmowe | 10 | AK-74, AKS-74U, AKM, AK-12, AK-103, AK-15, AN-94, AEK-971, SR-3, AS Val |
| 10 | Karabiny maszynowe | 7 | RPK, RPL-20, PK/PKM, PKP, DShK, NSW, Kord |
| 11 | Karabiny snajperskie | 7 | VSS, SVD, SV-98, Orsis T-5000, KSVK, OSV-96, Lobaev |
| 12 | RPG i wyrzutnie | 11 | RPG-7, RPG-18, RPG-22, RPG-26, RPG-27, RPG-29, RPG-30, RPG-32, RShG-1, Szmiel, Bur |
| 13 | Wyrzutnie granatów | 7 | GP-25, GP-30, GP-34, AGS-17, AGS-30, AGS-40, GM-94 |
| 14 | Pistolety i PM | 15 | PM, TT, APS, PB, PSM, MP-443, GSz-18, SR-1, OTs-33, OTs-23, PP-91, PP-2000, PL-15, SPP-1M, APS podwodny |
| 15 | Granaty ręczne | 6 | F-1, RGD-5, RGN, RGO, RKG-3, VOG-25 |
| 16 | Miny | 13 | PMN, PMN-2, OZM-72, POM-2, PFM-1, MON-50, MON-100, TM-57, TM-62M, PTM-3, KPOM-2, UMZ, VS-50 |

---

## Format każdego pliku .md

Każde hasło ma identyczną strukturę:

```markdown
# Nazwa polska
### Nazwa angielska | Nazwa rosyjska

![Opis zdjęcia](../images/KATALOG/PLIK_1.jpg)

---

## Opis

Jeden akapit: historia, kraj produkcji, kontekst operacyjny, użycie w konfliktach.

## Dane techniczne

| Parametr | Wartość |
|----------|---------|
| Typ | ... |
| Kraj produkcji | ZSRR / Rosja |
| Rok wprowadzenia | RRRR |
| Masa | X kg / t |
| ... | ... |

## Charakterystyczne cechy rozpoznawcze

> Jak odróżnić [BROŃ] od podobnych:

- **Cecha wizualna — wyjaśnienie:** szczegółowy opis co widzieć i jak to odróżnia od podobnych
- **Kolejna cecha:** ...
(minimum 5–6 punktów, każdy zaczyna się pogrubioną nazwą cechy)

## Ciekawostka

> Jeden akapit — konkretny fakt historyczny, taktyczny lub techniczny, najlepiej z konkretną datą/miejscem/liczbą.
```

**Ważne zasady formatu:**
- Ścieżka obrazu jest **zawsze relatywna**: `../images/KATEGORIA/PLIK.jpg`
- Nagłówek h3 (`###`) zawiera wersję angielską i cyrylicą
- Sekcja "Charakterystyczne cechy" to najważniejsza część — praktyczne rozpoznawanie w terenie
- Ciekawostka musi być konkretna i weryfikowalna

---

## Jak dodać nową broń

### 1. Utwórz plik .md

Plik trafia do odpowiedniego katalogu kategorii. Nazwa pliku = skrócona nazwa broni bez spacji, małymi literami, myślniki zamiast spacji.

Przykłady:
- T-55 → `czolgi/t-55.md`
- BMP-1P → `bwp/bmp-1p.md`
- AK-74M → `karabiny/ak-74m.md`

Użyj formatu opisanego powyżej.

### 2. Pobierz dane — workflow z NotebookLM (zalecany)

NotebookLM (`notebooklm-py`) jest zainstalowany i skonfigurowany. To najszybszy sposób na zebranie danych do hasła:

```bash
# 1. Utwórz nowy notebook dla partii broni
notebooklm create "Badany sprzęt: nazwa1, nazwa2, ..." --json

# 2. Ustaw kontekst
notebooklm use <notebook_id>

# 3. Dodaj artykuły Wikipedii jako źródła (równolegle)
notebooklm source add "https://en.wikipedia.org/wiki/Nazwa_artykulu" --json &
notebooklm source add "https://pl.wikipedia.org/wiki/Nazwa_artykulu" --json &
wait

# 4. Poczekaj na zaindeksowanie
notebooklm source wait <source_id> --timeout 120

# 5. Zapytaj o dane techniczne i cechy rozpoznawcze
notebooklm ask "Podaj dane techniczne X: masa, kaliber, zasięg, rok wprowadzenia..." -s <source_id>
```

**Gotowe pytanie do kopiowania** (dostosuj nazwę broni):

```
Podaj pełne dane techniczne [BROŃ]: masa, wymiary, załoga, uzbrojenie (kaliber, zasięg, szybkostrzelność), silnik, prędkość, zasięg operacyjny, pancerz, rok wprowadzenia. Opisz charakterystyczne cechy rozpoznawcze wizualnego identyfikowania [BROŃ] — jak odróżnić od podobnych systemów. Podaj ciekawostkę i użycie w Ukrainie od 2022.
```

**Uwagi:**
- Użyj flagi `-s <source_id>` żeby ograniczyć zapytanie do konkretnego źródła
- Jeśli artykuł EN nie ma danych, dodaj wersję PL: `https://pl.wikipedia.org/wiki/...`
- Jeśli URL Wikipedii się nie indeksuje (strona ujednoznaczniająca), sprawdź dokładniejszy URL: `https://en.wikipedia.org/wiki/57_mm_AZP_S-60` zamiast `https://en.wikipedia.org/wiki/S-60`

### 3. Pobierz obraz

**Metoda A — przez Wikipedia pageimages API (zalecana):**

```python
import urllib.request, json, urllib.parse, time

WP_API = "https://en.wikipedia.org/w/api.php"
HEADERS = {"User-Agent": "spw-fr-ebook/1.0"}

def get_wp_image(article_title, size=600):
    params = {
        "action": "query", "titles": article_title,
        "prop": "pageimages", "pithumbsize": str(size),
        "format": "json", "redirects": "1",
    }
    url = WP_API + "?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(urllib.request.Request(url, headers=HEADERS)) as r:
        data = json.loads(r.read())
    for page in data.get("query",{}).get("pages",{}).values():
        t = page.get("thumbnail")
        if t: return t.get("source")
    return None

img_url = get_wp_image("T-55")
# pobierz img_url i zapisz jako images/czolgi/t-55_1.jpg
time.sleep(0.5)  # obowiązkowe — limit Wikimedia
```

**Metoda B — przez Wikimedia Commons API (gdy znasz nazwę pliku):**

```python
COMMONS_API = "https://commons.wikimedia.org/w/api.php"

def get_commons_image(filename, size=600):
    params = {
        "action": "query", "titles": f"File:{filename}",
        "prop": "imageinfo", "iiprop": "url",
        "iiurlwidth": str(size), "format": "json",
    }
    url = COMMONS_API + "?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(urllib.request.Request(url, headers=HEADERS)) as r:
        data = json.loads(r.read())
    for page in data.get("query",{}).get("pages",{}).values():
        ii = page.get("imageinfo", [])
        if ii: return ii[0].get("thumburl") or ii[0].get("url")
    return None

# Wyszukiwanie pliku na Commons:
def search_commons(query, limit=10):
    params = {
        "action": "query", "list": "search",
        "srsearch": query, "srnamespace": "6",
        "srlimit": str(limit), "format": "json",
    }
    url = COMMONS_API + "?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(urllib.request.Request(url, headers=HEADERS)) as r:
        data = json.loads(r.read())
    return [r["title"] for r in data.get("query",{}).get("search",[])]

# Przykład:
results = search_commons("T-62M tank")
for r in results:
    print(r)
```

**Ważne przy pobieraniu:**
- `time.sleep(0.5)` między zapytaniami — Wikimedia ma limit (HTTP 429)
- Przy 429: poczekaj 3–5 sekund i spróbuj ponownie
- Zapisuj do `images/KATEGORIA/NAZWABRONI_1.jpg`
- Rozmiar 600px optymalny; nie przekraczaj 1000px bez potrzeby

**Jeśli Wikipedia nie ma miniaturki:**
1. Szukaj ręcznie: `search_commons("nazwa sprzętu")`
2. Użyj dokładniejszego tytułu artykułu (np. `"T-62M"` zamiast `"T-62"`)
3. Sprawdź polską Wikipedię: `https://pl.wikipedia.org/wiki/...`

### 4. Dodaj odniesienie do obrazu w pliku .md

```markdown
![Opis alternatywny](../images/KATEGORIA/NAZWABRONI_1.jpg)
```

Wstaw po nagłówkach h1+h3, przed pierwszym `---`.

### 5. Zaktualizuj changelog.md

Plik `changelog.md` musi być aktualizowany przy **każdej** zmianie w e-booku.

**Reguła tego samego dnia:** jeśli data ostatniego wiersza w changelog == data dzisiejsza → dopisz opis do istniejącego wiersza (nie podbijaj wersji). Jeśli data jest starsza → dodaj nowy wiersz i podbij MINOR (np. 1.1 → 1.2).

**Changelog dotyczy wyłącznie treści e-booka.** Zmiany w dokumentacji (INSTRUKCJA.md, skrypty, CLAUDE.md) nie są wpisywane.

| Typ zmiany | Wersja |
|------------|--------|
| Nowe hasła lub kategorie | +MINOR (1.1 → 1.2) |
| Poprawki haseł, zdjęć, danych technicznych | dopisz do bieżącego wpisu dnia |
| Zmiany w dokumentacji / skryptach | **nie wpisuj do changelog** |
| Przebudowa struktury haseł | +MAJOR (1.x → 2.0) |

Format wiersza:
```markdown
| 1.2 | 2026-05-10 | **Nowe hasła — kategoria:** nazwa1, nazwa2. **Poprawki:** opis. |
```

### 6. Zaktualizuj spis_tresci.md

Dodaj linię w odpowiedniej sekcji:

```markdown
- [NAZWA — Opis](KATEGORIA/PLIK.md)
```

### 6b. Zaktualizuj zrodla_grafik.md (lista atrybucji grafik)

Po dodaniu nowych obrazów należy zaktualizować plik `zrodla_grafik.md`:

1. Otwórz `generate_attribution.py` i dodaj mapowanie nowego obrazu:
   - Jeśli znasz nazwę pliku na Wikimedia Commons → dodaj do sekcji `KNOWN_COMMONS`:
     ```python
     "KATEGORIA/plik_1.jpg": "Commons_filename.jpg",
     ```
   - Jeśli znasz tytuł artykułu Wikipedia → dodaj do sekcji `WIKI_ARTICLES`:
     ```python
     "KATEGORIA/plik_1.jpg": "Tytuł artykułu Wikipedia",
     ```
2. Uruchom skrypt: `python3 generate_attribution.py`
3. Sprawdź wynik — upewnij się, że nowe obrazy mają atrybucję

**Nie edytuj `zrodla_grafik.md` ręcznie** — jest generowany automatycznie przez skrypt.

### 7. Zaktualizuj index.md

Zmień liczbę pozycji w tabeli kategorii i łączną liczbę haseł:

```markdown
| 1 | [Czołgi](spis_tresci.md#1-czołgi) | 8 |   ← zmień liczbę

Niniejszy podręcznik zawiera opisy **144 typów uzbrojenia...   ← zmień liczbę
```

---

## Jak dodać nową kategorię

1. Utwórz katalog: `mkdir NOWA_KATEGORIA/`
2. Utwórz katalog obrazów: `mkdir images/NOWA_KATEGORIA/`
3. Dodaj pliki .md w nowym katalogu
4. Dodaj sekcję w `spis_tresci.md`:
   ```markdown
   ## 17. Nowa kategoria
   
   - [Broń A](nowa_kategoria/bron-a.md)
   ```
5. Dodaj wiersz w tabeli w `index.md`
6. Zaktualizuj ten plik (INSTRUKCJA.md) — tabelę kategorii i drzewo katalogów

---

## Skrypty pomocnicze

W katalogu projektu dostępne są skrypty (można je adaptować):

- `download_images2.py` — pobieranie przez Wikipedia pageimages API (po tytule artykułu) — **zalecany**
- `download_images.py` — pobieranie przez Wikimedia Commons API (po nazwie pliku)
- `download_images3.py` — wersja z poprawionymi/alternatywnymi tytułami
- `add_images_to_md.py` — masowe dodawanie `![...]` do plików bez obrazów

Skrypty działają w trybie SKIP — jeśli obraz już istnieje i ma >1 KB, jest pomijany. Bezpiecznie uruchamiać wielokrotnie.

---

## Workflow z NotebookLM — wskazówki operacyjne

NotebookLM jest zainstalowany (`pip install notebooklm-py`) i zalogowany (Google OAuth, ciasteczka w `~/.notebooklm/`). Sprawdzenie stanu:

```bash
notebooklm status       # aktywny notebook
notebooklm auth check   # weryfikacja logowania
notebooklm list         # lista notebooków
```

### Zalecany workflow dla partii haseł

1. Jeden notebook na sesję/temat (np. "SPW FR: czołgi radzieck WWII")
2. Dodaj wszystkie artykuły Wikipedia równolegle (`& ... wait`)
3. Poczekaj na zaindeksowanie (`source wait` w tle, wszystkie równolegle)
4. Odpytuj każdy sprzęt oddzielnie z flagą `-s <source_id>` — precyzyjniejsze odpowiedzi
5. Pobierz obrazy osobnym skryptem Python po zebraniu danych

### Typowe problemy

| Problem | Rozwiązanie |
|---------|-------------|
| Źródło zwraca stronę ujednoznaczniającą | Użyj dokładniejszego URL (np. `57_mm_AZP_S-60`) |
| NotebookLM "nie zna" tematu | Dodaj artykuł z polskiej Wikipedii jako drugie źródło |
| `source wait` timeout | Źródło jest duże; spróbuj `--timeout 300` |
| HTTP 429 przy pobieraniu obrazów | `time.sleep(3)` i ponów; nie pobieraj równolegle |

---

## Znane problemy i obejścia

### Brakujące obrazy dla niszowych broni

Niektóre bronie nie mają miniaturki na Wikipedii (`BRAK obrazu`). Rozwiązania:
1. Szukaj ręcznie na Wikimedia Commons: `commons.wikimedia.org/wiki/Category:T-55`
2. Użyj funkcji `search_commons("nazwa sprzętu")` — patrz sekcja "Pobierz obraz"
3. Sprawdź czy obraz T-62M i T-62 nie jest ten sam (Wikipedia zwraca główne zdjęcie artykułu T-62 dla obu) — w takim przypadku wyszukaj specyficznie na Commons: `"T-62M tank"`, `"T-62M - Army-2023"`
4. Zostaw plik bez obrazu i wróć później

### Błędy HTTP 429 (rate limiting Wikimedia)

- Zwiększ `time.sleep()` do 0.8–1.0 sekundy między zapytaniami
- Przy pobraniu wielu obrazów kolejno: zrób przerwę 3–5 sek po każdym
- Uruchamiaj skrypt kilka razy — pliki już pobrane są pomijane (SKIP)
- **Nie pobieraj obrazów równolegle** (wątki/background) — pewny 429

### Ścieżki obrazów

Obraz zawsze musi być w katalogu `images/KATEGORIA/` a ścieżka w .md zawsze `../images/KATEGORIA/PLIK.jpg`. Ścieżka absolutna nie zadziała przy eksporcie do PDF.

---

## Budowanie PDF

Projekt zawiera `Makefile` i `template.tex`. Budowanie:

```bash
make          # buduje PDF
make clean    # czyści pliki tymczasowe
```

PDF wychodzi do katalogu `build/`. Jeśli brakuje obrazu, LaTeX zgłosi błąd — sprawdź `build/*.log`.

---

## Konwencje nazewnictwa

| Element | Konwencja | Przykład |
|---------|-----------|---------|
| Plik .md | małe litery, myślniki | `t-55.md`, `rpg-7.md`, `2s19-msta-s.md` |
| Katalog kategorii | małe litery, podkreślniki | `karabiny_maszynowe/` |
| Obraz | `NAZWAMD_NUMER.jpg` | `t-55_1.jpg`, `2s19-msta-s_1.jpg` |
| Katalog obrazów | identyczny z katalogiem kategorii | `images/czolgi/` |

---

*Ostatnia aktualizacja: kwiecień 2026. Stan: 130 haseł, 16 kategorii, 138 obrazów.*

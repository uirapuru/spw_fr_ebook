# Instrukcja obsługi i rozbudowy e-booka

## Co zostało zrobione

### Struktura projektu

```
spw_fr_ebook/
├── index.md                  ← strona główna (tabela kategorii)
├── spis_tresci.md            ← pełny spis treści z linkami
├── INSTRUKCJA.md             ← ten plik
├── images/                   ← wszystkie obrazy
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
├── czolgi/                   ← T-72, T-80, T-90
├── bwp/                      ← BMP-1, BMP-2, BMP-3
├── apc/                      ← BTR-80, BTR-90, Tigr
├── artyleria_samobiezna/     ← 7 pojazdów (2S1 do 2S40)
├── artyleria_holowana/       ← 11 dział i moździerzy
├── przeciwlotnicze/          ← 7 systemów (S-300 do Werba)
├── przeciwpancerne/          ← 5 ppk (Fagot do Kornet)
├── lotnictwo/                ← Mi-24, Mi-28, Ka-52, Su-25, Su-27
├── karabiny/                 ← 10 karabinów szturmowych
├── karabiny_maszynowe/       ← 7 karabinów maszynowych
├── karabiny_snajperskie/     ← 7 karabinów snajperskich
├── rpg_wyrzutnie/            ← 11 granatników i wyrzutni
├── wyrzutnie_granatow/       ← 7 wyrzutni granatów
├── pistolety_i_pm/           ← 15 pistoletów i PM
├── granaty_reczne/           ← 6 granatów
└── miny/                     ← 13 min
```

Łącznie: **120 plików treści**, **134 obrazy**, **16 kategorii**.

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

Użyj formatu opisanego powyżej. Dane techniczne pobieraj z:
- Wikipedia (angielska wersja — zwykle najdokładniejsza)
- Jane's Defence (jeśli dostępne)
- GlobalSecurity.org

### 2. Pobierz obraz

**Metoda A — przez Wikipedia API (zalecana):**

```python
import urllib.request, json, urllib.parse

WP_API = "https://en.wikipedia.org/w/api.php"
HEADERS = {"User-Agent": "spw-fr-ebook/1.0"}

def get_wp_image(article_title, size=500):
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

url = get_wp_image("T-55")  # tytuł artykułu na Wikipedii
# pobierz url i zapisz jako images/czolgi/t-55_1.jpg
```

**Metoda B — przez Wikimedia Commons API:**

Jeśli znasz dokładną nazwę pliku na Commons (np. `T-55_tank.jpg`):

```python
COMMONS_API = "https://commons.wikimedia.org/w/api.php"
params = {
    "action": "query", "titles": "File:T-55_tank.jpg",
    "prop": "imageinfo", "iiprop": "url", "iiurlwidth": "500",
    "format": "json",
}
# zwraca thumburl
```

**Ważne przy pobieraniu:**
- Dodaj `time.sleep(0.5)` między zapytaniami — Wikimedia ma limit zapytań
- Jeśli dostaniesz HTTP 429, poczekaj i spróbuj ponownie
- Zapisuj do `images/KATEGORIA/NAZWABRONI_1.jpg`
- Rozmiar 500px jest wystarczający; 800px często zwraca 429

**Jeśli Wikipedia nie ma miniaturki w infoboxie** (BRAK obrazu z API):
- Spróbuj inny tytuł artykułu (np. `"T-55 tank"` zamiast `"T-55"`)
- Szukaj ręcznie na commons.wikimedia.org
- Jako fallback użyj podobnej broni z tej samej rodziny

### 3. Dodaj odniesienie do obrazu w pliku .md

```markdown
![Opis alternatywny](../images/KATEGORIA/NAZWABRONI_1.jpg)
```

Wstaw po nagłówkach h1+h3, przed pierwszym `---`.

### 4. Zaktualizuj spis_tresci.md

Dodaj linię w odpowiedniej sekcji:

```markdown
- [NAZWA — Opis](KATEGORIA/PLIK.md)
```

### 5. Zaktualizuj index.md

Zmień liczbę pozycji w tabeli kategorii:

```markdown
| 1 | [Czołgi](spis_tresci.md#1-czołgi) | 4 |   ← zmień liczbę
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

---

## Skrypty pomocnicze

W katalogu projektu dostępne są skrypty (można je adaptować):

- `download_images.py` — pobieranie przez Wikimedia Commons API (po nazwie pliku)
- `download_images2.py` — pobieranie przez Wikipedia pageimages API (po tytule artykułu) — **zalecany**
- `download_images3.py` — wersja z poprawionymi/alternatywnymi tytułami
- `add_images_to_md.py` — masowe dodawanie `![...]` do plików bez obrazów

---

## Znane problemy i obejścia

### Brakujące obrazy dla niszowych broni

Niektóre bronie nie mają miniaturki na Wikipedii (`BRAK obrazu`). Rozwiązania:
1. Szukaj ręcznie na Wikimedia Commons: `commons.wikimedia.org/wiki/Category:T-55`
2. Użyj podobnego sprzętu jako zastępnik (zanotuj to w pliku!)
3. Zostaw plik bez obrazu i wróć później

### Błędy HTTP 429 (rate limiting)

Wikimedia ogranicza częstotliwość zapytań. Rozwiązania:
- Zwiększ `time.sleep()` do 0.8–1.0 sekundy
- Uruchamiaj skrypt kilka razy — pliki już pobrane są pomijane (SKIP)
- Poczekaj kilka minut i uruchom ponownie

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

## Notebooklm

Projekt był pierwotnie powiązany z narzędziem `notebooklm-py`. Aby z niego korzystać:

```bash
pip install notebooklm-py
notebooklm login           # logowanie przez Google OAuth
notebooklm list            # lista notatników
notebooklm source add ./PLIK.md   # dodanie pliku jako źródła
notebooklm ask "Pytanie"   # czat z treścią
```

Notebooklm może być używany do:
- Generowania streszczeń kategorii
- Tworzenia quizów z materiału
- Podcastów na podstawie wybranych haseł
- Weryfikacji treści (pytając o konkretne fakty)

---

## Konwencje nazewnictwa

| Element | Konwencja | Przykład |
|---------|-----------|---------|
| Plik .md | małe litery, myślniki | `t-55.md`, `rpg-7.md` |
| Katalog kategorii | małe litery, podkreślniki | `karabiny_maszynowe/` |
| Obraz | `NAZWAMD_NUMER.jpg` | `t-55_1.jpg`, `t-55_2.jpg` |
| Katalog obrazów | identyczny z katalogiem kategorii | `images/czolgi/` |

---

*Ostatnia aktualizacja: kwiecień 2026. Stan: 120 haseł, 16 kategorii, 134 obrazy.*

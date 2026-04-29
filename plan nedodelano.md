# Workflow pro zadávání záznamů do databáze ptáků

## Cíl
Navrhnout přehledný a efektivní proces pro zadávání nových záznamů do existující databáze tabulky `ptaci`.

---

## 1. Vstup do formuláře
- Uživatel otevře sekci **„Přidat nový záznam“**
- Systém zobrazí formulář rozdělený do logických bloků:
  - Základní informace
  - Biologické údaje
  - Ekologické údaje

---

## 2. Zadávání dat

### 2.1 Základní informace
- `nazev` (povinné)
- `vedecky_nazev` (povinné)
- `rad`
- `celed`

### 2.2 Biologické údaje
- `delka_cm`
- `rozpeti_cm`
- `hmotnost_g`
- `snuska_ks`

### 2.3 Ekologické údaje
- `status_ohrozeni`
  - Doporučeno jako výběr (např. LC, NT, VU, EN, CR)
- `typ_potravy`
  - Výběr nebo vícenásobná volba (např. hmyz, semena, maso)
- `migrace`
  - Boolean (0 = nemigruje, 1 = migruje)
- `vyskyt_kontinent`
  - Výběr z kontinentů nebo více hodnot

---

## 3. Validace dat
- Povinná pole musí být vyplněna:
  - `nazev`
  - `vedecky_nazev`
- Numerická pole:
  - musí obsahovat čísla
  - nesmí být záporná
- Logické kontroly:
  - rozpětí křídel ≥ délka těla (volitelné pravidlo)
- Kontrola duplicit:
  - podle `nazev` + `vedecky_nazev`

---

## 4. Potvrzení záznamu
- Uživatel klikne na **„Uložit“**
- Systém:
  - provede validaci
  - zobrazí chyby (pokud existují)
  - nebo zobrazí rekapitulaci

---

## 5. Uložení do databáze
- Po potvrzení:
  - data se uloží do tabulky `ptaci`
  - systém vrátí ID nového záznamu

---

## 6. Zpětná vazba uživateli
- Úspěch:
  - „Záznam byl úspěšně uložen“
- Chyba:
  - konkrétní hlášení (např. „Neplatná hmotnost“)

---

## 7. Volitelné rozšíření
- Automatické doplňování (autocomplete) pro:
  - řád
  - čeleď
- Import dat (CSV)
- Napojení na externí databáze (např. taxonomické API)
- Ukládání rozepsaného formuláře

---

## Otevřené otázky
1. Má být `typ_potravy` jedna hodnota, nebo více hodnot?
2. Má být `vyskyt_kontinent` jedna hodnota, nebo seznam?
3. Má aplikace řešit vícejazyčnost?
4. Má být kontrola duplicit striktní, nebo jen upozornění?
5. Budou uživatelé rozlišeni (role, oprávnění)?

---
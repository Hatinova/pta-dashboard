# Workflow pro zadávání záznamů do databáze ptáků

## 1. Krok: Přidat záznam

V této části bude doplněna možnost vkládání nových ptáků do databáze `ptaci`.  
Tato funkce se aktivuje tlačítkem umístěným v levém spodním rohu hlavní plochy aplikace.  

Po kliknutí na tlačítko se otevře formulář odpovídající struktuře databázové tabulky.  
Uživatel bude vyplňovat tyto položky:
- `nazev` (TEXT)  
- `vedecky_nazev` (TEXT)  
- `rad` (TEXT)  
- `celed` (TEXT)  
- `delka_cm` (INTEGER)  
- `rozpeti_cm` (INTEGER)  
- `hmotnost_g` (INTEGER)  
- `status_ohrozeni` (TEXT)  
- `typ_potravy` (TEXT)  
- `migrace` (INTEGER)  
- `vyskyt_kontinent` (TEXT)  
- `snuska_ks` (REAL)  

Pole `id` se nezadává, protože se generuje automaticky (`AUTOINCREMENT`).  

Po vyplnění formuláře uživatel odešle data tlačítkem „Přidat záznam“.  
Aplikace zkontroluje datové typy (INTEGER, REAL, TEXT) a následně provede SQL dotaz typu `INSERT INTO ptaci (...) VALUES (...)`.  

Po úspěšném uložení se zobrazí potvrzení a nový záznam se objeví v seznamu databáze.  
V případě chyby aplikace zobrazí hlášení a umožní opravu vstupních dat.

## 2. Krok: Úprava záznamů

V této fázi bude vytvořeno tlačítko v levém dolním rohu které otevře formulář (nebo formulář), který umožní upravovat existující záznamy v tabulce `ptaci`.  
Formulář bude obsahovat vstupní pole pro všechny sloupce (např. `nazev`, `vedecky_nazev`, `rad`, `celed`, `delka_cm`, `rozpeti_cm`, `hmotnost_g`, `status_ohrozeni`, `typ_potravy`, `migrace`, `vyskyt_kontinent`, `snuska_ks`).  

Po výběru konkrétního záznamu (např. ze seznamu nebo zadáním `id`) se formulář předvyplní aktuálními hodnotami z databáze.  
Uživatel bude moci hodnoty upravit a potvrdit změny tlačítkem „Uložit“.  

Po odeslání formuláře aplikace provede SQL dotaz typu `UPDATE ptaci SET ... WHERE id = ?`.  
Součástí bude kontrola datových typů (např. čísla u `delka_cm`, `hmotnost_g`) a ošetření chyb (např. neplatný vstup nebo selhání databáze).  
Po úspěšném uložení se zobrazí potvrzení a aktualizovaný záznam.

## 3. Krok: Odebírání záznamů

V této fázi bude přidána možnost mazání existujících záznamů z tabulky `ptaci`.  
Uživatel bude moci vybrat konkrétní záznam (např. ze seznamu) a odstranit jej pomocí tlačítka „Smazat“.  

Před samotným smazáním bude zobrazena potvrzovací výzva, aby nedošlo k nechtěnému odstranění dat.  

Po potvrzení aplikace provede SQL dotaz typu `DELETE FROM ptaci WHERE id = ?`,  
čímž dojde k trvalému odstranění záznamu z databáze.  

Po úspěšném smazání se aktualizuje zobrazený seznam záznamů.  
V případě chyby (např. neplatné `id` nebo problém s databází) aplikace zobrazí chybovou hlášku.


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




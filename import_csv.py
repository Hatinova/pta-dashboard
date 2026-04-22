#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Import skript pro načtení dat z CSV souboru do SQLite databáze.
Načítá dataset_ptaci_final.csv a vytváří ptaci.db s tabulkou ptaci.
"""

import csv
import sqlite3
import os
from pathlib import Path

# Cesty k souborům
CSV_FILE = os.path.join(os.path.dirname(__file__), 'dataset_ptaci_final.csv')
DB_FILE = os.path.join(os.path.dirname(__file__), 'ptaci.db')

def create_database():
    """Vytvoří SQLite databázi a tabulku ptaci."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Vytvoření tabulky
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ptaci (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nazev TEXT,
            vedecky_nazev TEXT,
            rad TEXT,
            celed TEXT,
            delka_cm INTEGER,
            rozpeti_cm INTEGER,
            hmotnost_g INTEGER,
            status_ohrozeni TEXT,
            typ_potravy TEXT,
            migrace INTEGER,
            vyskyt_kontinent TEXT,
            snuska_ks REAL
        )
    ''')
    conn.commit()
    conn.close()

def import_csv_data():
    """Načte data z CSV souboru a vloží je do databáze."""
    
    # Kontrola, zda CSV soubor existuje
    if not os.path.exists(CSV_FILE):
        print(f"Chyba: Soubor {CSV_FILE} nebyl nalezen.")
        return 0
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    imported_count = 0
    
    try:
        # Otevření CSV souboru s kódováním utf-8-sig (BOM)
        with open(CSV_FILE, 'r', encoding='utf-8-sig') as csvfile:
            csv_reader = csv.DictReader(csvfile)
            
            # Kontrola, zda soubor má řádky
            if csv_reader.fieldnames is None:
                print("Chyba: CSV soubor nemá záhlaví.")
                return 0
            
            for row in csv_reader:
                try:
                    # Konverze datových typů
                    delka_cm = int(row.get('delka_cm')) if row.get('delka_cm') else None
                    rozpeti_cm = int(row.get('rozpeti_cm')) if row.get('rozpeti_cm') else None
                    hmotnost_g = int(row.get('hmotnost_g')) if row.get('hmotnost_g') else None
                    migrace = int(row.get('migrace')) if row.get('migrace') else None
                    snuska_ks = float(row.get('snuska_ks')) if row.get('snuska_ks') else None
                    
                    # Vložení záznamu do databáze
                    cursor.execute('''
                        INSERT INTO ptaci (
                            nazev, vedecky_nazev, rad, celed, delka_cm, rozpeti_cm,
                            hmotnost_g, status_ohrozeni, typ_potravy, migrace,
                            vyskyt_kontinent, snuska_ks
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        row.get('nazev'),
                        row.get('vedecky_nazev'),
                        row.get('rad'),
                        row.get('celed'),
                        delka_cm,
                        rozpeti_cm,
                        hmotnost_g,
                        row.get('status_ohrozeni'),
                        row.get('typ_potravy'),
                        migrace,
                        row.get('vyskyt_kontinent'),
                        snuska_ks
                    ))
                    imported_count += 1
                    
                except ValueError as e:
                    print(f"Varování: Chyba při konverzi datového typu u řádku {imported_count + 1}: {e}")
                    continue
                except Exception as e:
                    print(f"Varování: Chyba při vložení řádku {imported_count + 1}: {e}")
                    continue
        
        conn.commit()
        
    except UnicodeDecodeError as e:
        print(f"Chyba: Problém s kódováním souboru: {e}")
    except Exception as e:
        print(f"Chyba při čtení CSV souboru: {e}")
    finally:
        conn.close()
    
    return imported_count

def main():
    """Hlavní funkce programu."""
    print("Spouštím import dat z CSV souboru do SQLite...")
    print(f"CSV soubor: {CSV_FILE}")
    print(f"Databáze: {DB_FILE}")
    print()
    
    # Smazání staré databáze, pokud existuje
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
        print("Stará databáze byla smazána.")
    
    # Vytvoření databáze a tabulky
    create_database()
    print("Databáze a tabulka byly vytvořeny.")
    print()
    
    # Import dat
    imported = import_csv_data()
    
    print()
    print(f"Import dokončen: {imported} záznamů bylo importováno.")
    
    # Ověření
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM ptaci')
    total_records = cursor.fetchone()[0]
    conn.close()
    
    print(f"Ověření: Tabulka ptaci obsahuje {total_records} záznamů.")

if __name__ == '__main__':
    main()

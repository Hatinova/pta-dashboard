from flask import Flask, render_template, request
import sqlite3
import os

app = Flask(__name__)

# Povolené sloupce pro řazení (ochrana proti SQL injection)
ALLOWED_SORT_COLUMNS = {
    "nazev", "vedecky_nazev", "rad", "celed",
    "delka_cm", "rozpeti_cm", "hmotnost_g",
    "status_ohrozeni", "typ_potravy", "migrace",
    "vyskyt_kontinent", "snuska_ks",
}

def get_db():
    """Otevře spojení na databázi ptaci.db a nastaví row_factory."""
    db = sqlite3.connect('ptaci.db')
    db.row_factory = sqlite3.Row
    return db

def build_query(params):
    """
    Ze zadaných parametrů sestaví WHERE klauzuli a seznam hodnot.
    Vrací tuple (where_clause, values).
    """
    conditions = []
    values = []
    
    if params.get('rad'):
        conditions.append('rad = ?')
        values.append(params.get('rad'))
    
    if params.get('celed'):
        conditions.append('celed = ?')
        values.append(params.get('celed'))
    
    if params.get('typ_potravy'):
        conditions.append('typ_potravy = ?')
        values.append(params.get('typ_potravy'))
    
    if params.get('vyskyt_kontinent'):
        conditions.append('vyskyt_kontinent = ?')
        values.append(params.get('vyskyt_kontinent'))
    
    if params.get('migrace') is not None and params.get('migrace') != '':
        conditions.append('migrace = ?')
        values.append(int(params.get('migrace')))
    
    if params.get('status_ohrozeni'):
        conditions.append('status_ohrozeni = ?')
        values.append(params.get('status_ohrozeni'))
    
    if params.get('hmotnost_min'):
        conditions.append('hmotnost_g >= ?')
        values.append(float(params.get('hmotnost_min')))
    
    if params.get('hmotnost_max'):
        conditions.append('hmotnost_g <= ?')
        values.append(float(params.get('hmotnost_max')))
    
    where_clause = ' AND '.join(conditions) if conditions else ''
    return where_clause, values

def get_filter_options(conn):
    """
    Z databáze načte unikátní hodnoty pro dropdowny.
    Vrací slovník s listy hodnot.
    """
    cursor = conn.cursor()
    options = {}
    
    cursor.execute('SELECT DISTINCT rad FROM ptaci ORDER BY rad')
    options['rady'] = [row['rad'] for row in cursor.fetchall() if row['rad']]
    
    cursor.execute('SELECT DISTINCT celed FROM ptaci ORDER BY celed')
    options['celedi'] = [row['celed'] for row in cursor.fetchall() if row['celed']]
    
    cursor.execute('SELECT DISTINCT typ_potravy FROM ptaci ORDER BY typ_potravy')
    options['potravy'] = [row['typ_potravy'] for row in cursor.fetchall() if row['typ_potravy']]
    
    cursor.execute('SELECT DISTINCT vyskyt_kontinent FROM ptaci ORDER BY vyskyt_kontinent')
    options['kontinenty'] = [row['vyskyt_kontinent'] for row in cursor.fetchall() if row['vyskyt_kontinent']]
    
    cursor.execute('SELECT DISTINCT status_ohrozeni FROM ptaci ORDER BY status_ohrozeni')
    options['stavy'] = [row['status_ohrozeni'] for row in cursor.fetchall() if row['status_ohrozeni']]
    
    return options

def validate_sort_params(razeni, smer):
    """
    Validuje parametry pro řazení.
    Vrací tuple (razeni, smer) s bezpečnými hodnotami.
    """
    # Validace sloupce - pokud není v povolené množině, použij výchozí
    if razeni not in ALLOWED_SORT_COLUMNS:
        razeni = 'nazev'
    
    # Validace směru - povoleno jen ASC nebo DESC
    if smer.upper() not in ('ASC', 'DESC'):
        smer = 'ASC'
    else:
        smer = smer.upper()
    
    return razeni, smer

@app.route('/')
def dashboard():
    db = get_db()
    cursor = db.cursor()
    
    # Získání filtrů z GET parametrů
    params = request.args
    
    # Získání možností pro dropdowny
    filter_options = get_filter_options(db)
    
    # Sestavení WHERE klauzule
    where_clause, values = build_query(params)
    
    # Validace a získání parametrů řazení
    razeni = params.get('razeni', 'nazev')
    smer = params.get('smer', 'ASC')
    razeni, smer = validate_sort_params(razeni, smer)
    
    # Agregační dotaz pro statistiky
    stats_query = '''
        SELECT
            COUNT(*) as pocet,
            ROUND(AVG(delka_cm), 1) as prum_delka,
            MAX(hmotnost_g) as max_hmotnost,
            MIN(hmotnost_g) as min_hmotnost,
            ROUND(AVG(hmotnost_g), 1) as prum_hmotnost,
            ROUND(AVG(rozpeti_cm), 1) as prum_rozpeti
        FROM ptaci
    '''
    if where_clause:
        stats_query += f' WHERE {where_clause}'
    
    cursor.execute(stats_query, values)
    stats = cursor.fetchone()
    
    # Dotazy pro grafy
    # 1. Druhy podle řádu
    druhy_rad = cursor.execute(
        f'SELECT rad, COUNT(*) as pocet FROM ptaci {("WHERE " + where_clause) if where_clause else ""} GROUP BY rad ORDER BY pocet DESC',
        values
    ).fetchall()
    
    # 2. Průměrná hmotnost podle typu potravy
    hmotnost_potrava = cursor.execute(
        f'SELECT typ_potravy, ROUND(AVG(hmotnost_g), 0) as prum FROM ptaci {("WHERE " + where_clause) if where_clause else ""} GROUP BY typ_potravy ORDER BY prum DESC',
        values
    ).fetchall()
    
    # 3. Tažní vs. netažní
    migrace = cursor.execute(
        f'SELECT migrace, COUNT(*) as pocet FROM ptaci {("WHERE " + where_clause) if where_clause else ""} GROUP BY migrace',
        values
    ).fetchall()
    
    # 4. Druhy podle kontinentu
    druhy_kontinent = cursor.execute(
        f'SELECT vyskyt_kontinent, COUNT(*) as pocet FROM ptaci {("WHERE " + where_clause) if where_clause else ""} GROUP BY vyskyt_kontinent ORDER BY pocet DESC',
        values
    ).fetchall()
    
    # Příprava dat pro grafy
    graf_rad_labels = [r['rad'] for r in druhy_rad]
    graf_rad_data = [r['pocet'] for r in druhy_rad]
    
    graf_potrava_labels = [r['typ_potravy'] for r in hmotnost_potrava]
    graf_potrava_data = [r['prum'] for r in hmotnost_potrava]
    
    migrace_labels = ['Tažný' if r['migrace'] else 'Netažný' for r in migrace]
    migrace_data = [r['pocet'] for r in migrace]
    
    graf_kontinent_labels = [r['vyskyt_kontinent'] for r in druhy_kontinent]
    graf_kontinent_data = [r['pocet'] for r in druhy_kontinent]
    
    # Sestavení SQL dotazu
    if where_clause:
        query = f'SELECT * FROM ptaci WHERE {where_clause} ORDER BY {razeni} {smer}'
    else:
        query = f'SELECT * FROM ptaci ORDER BY {razeni} {smer}'
    
    cursor.execute(query, values)
    ptaci = cursor.fetchall()
    db.close()
    
    return render_template('dashboard.html', ptaci=ptaci, filter_options=filter_options, params=params, razeni=razeni, smer=smer, stats=stats, 
                         graf_rad_labels=graf_rad_labels, graf_rad_data=graf_rad_data,
                         graf_potrava_labels=graf_potrava_labels, graf_potrava_data=graf_potrava_data,
                         migrace_labels=migrace_labels, migrace_data=migrace_data,
                         graf_kontinent_labels=graf_kontinent_labels, graf_kontinent_data=graf_kontinent_data)

if __name__ == '__main__':
    app.run(debug=True)

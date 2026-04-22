from flask import Flask, render_template, request
import sqlite3
import os

app = Flask(__name__)

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
        conditions.append('potrava = ?')
        values.append(params.get('typ_potravy'))
    
    if params.get('kontinent'):
        conditions.append('kontinent = ?')
        values.append(params.get('kontinent'))
    
    if params.get('migrace') is not None and params.get('migrace') != '':
        conditions.append('migrace = ?')
        values.append(int(params.get('migrace')))
    
    if params.get('status'):
        conditions.append('status = ?')
        values.append(params.get('status'))
    
    if params.get('hmotnost_min'):
        conditions.append('hmotnost >= ?')
        values.append(float(params.get('hmotnost_min')))
    
    if params.get('hmotnost_max'):
        conditions.append('hmotnost <= ?')
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
    
    cursor.execute('SELECT DISTINCT potrava FROM ptaci ORDER BY potrava')
    options['potravy'] = [row['potrava'] for row in cursor.fetchall() if row['potrava']]
    
    cursor.execute('SELECT DISTINCT kontinent FROM ptaci ORDER BY kontinent')
    options['kontinenty'] = [row['kontinent'] for row in cursor.fetchall() if row['kontinent']]
    
    cursor.execute('SELECT DISTINCT status FROM ptaci ORDER BY status')
    options['stavy'] = [row['status'] for row in cursor.fetchall() if row['status']]
    
    return options

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
    
    # Sestavení SQL dotazu
    if where_clause:
        query = f'SELECT * FROM ptaci WHERE {where_clause} ORDER BY nazev ASC'
    else:
        query = 'SELECT * FROM ptaci ORDER BY nazev ASC'
    
    cursor.execute(query, values)
    ptaci = cursor.fetchall()
    db.close()
    
    return render_template('dashboard.html', ptaci=ptaci, filter_options=filter_options, params=params)

if __name__ == '__main__':
    app.run(debug=True)

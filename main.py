import sqlite3

def initializare_baza_date():
    # Se creeaza sau se conecteaza la un fisier de baza de date local
    conn = sqlite3.connect('biblioteca.db')
    cursor = conn.cursor()

    # Crearea tabelei pentru Carti (Structurarea bazei de date)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Carti (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titlu TEXT NOT NULL,
            autor TEXT NOT NULL,
            categorie TEXT,
            disponibil INTEGER DEFAULT 1
        )
    ''')

    # Crearea tabelei pentru Utilizatori
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Utilizatori (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nume TEXT NOT NULL
        )
    ''')

    # Salveaza schimbarile
    conn.commit()
    return conn

def adauga_carte(conn, titlu, autor, categorie):
    # Operatia CREATE (din CRUD)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Carti (titlu, autor, categorie) VALUES (?, ?, ?)', (titlu, autor, categorie))
    conn.commit()
    print(f"\n[SUCCES] Cartea '{titlu}' a fost adaugata in baza de date!")

def afiseaza_carti(conn):
    # Operatia READ (din CRUD)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Carti')
    carti = cursor.fetchall()
    
    print("\n--- Lista Cartilor din Biblioteca ---")
    if not carti:
        print("Biblioteca este goala momentan.")
    for carte in carti:
        status = "Disponibila" if carte[4] == 1 else "Imprumutata"
        print(f"ID: {carte[0]} | Titlu: {carte[1]} | Autor: {carte[2]} | Categorie: {carte[3]} | Status: {status}")

def cautare_avansata(conn, termen):
    # Functia de cautare avansata
    cursor = conn.cursor()
    # Cauta termenul in titlu, autor sau categorie
    cursor.execute('SELECT * FROM Carti WHERE titlu LIKE ? OR autor LIKE ? OR categorie LIKE ?', 
                   (f'%{termen}%', f'%{termen}%', f'%{termen}%'))
    rezultate = cursor.fetchall()
    
    print(f"\n--- Rezultate Cautare pentru '{termen}' ---")
    if rezultate:
        for carte in rezultate:
            status = "Disponibila" if carte[4] == 1 else "Imprumutata"
            print(f"ID: {carte[0]} | Titlu: {carte[1]} | Autor: {carte[2]} | Status: {status}")
    else:
        print("Nu s-au gasit carti care sa corespunda cautarii.")

def meniu_principal():
    conn = initializare_baza_date()
    
    while True:
        print("\n=== Sistem Administrare Biblioteca ===")
        print("1. Adauga o carte noua (C)")
        print("2. Vezi toate cartile (R)")
        print("3. Cauta o carte (Cautare avansata)")
        print("0. Iesire")
        
        alegere = input("Alege o optiune (0-3): ")
        
        if alegere == '1':
            titlu = input("Introdu titlul cartii: ")
            autor = input("Introdu autorul: ")
            categorie = input("Introdu categoria (ex: SF, Educatie): ")
            adauga_carte(conn, titlu, autor, categorie)
        elif alegere == '2':
            afiseaza_carti(conn)
        elif alegere == '3':
            termen = input("Introdu un cuvant cheie (titlu/autor/categorie): ")
            cautare_avansata(conn, termen)
        elif alegere == '0':
            print("Se inchide aplicatia. La revedere!")
            break
        else:
            print("Optiune invalida! Te rog alege o cifra din meniu.")
            
    conn.close()

# Punctul de pornire al programului
if __name__ == '__main__':
    meniu_principal()
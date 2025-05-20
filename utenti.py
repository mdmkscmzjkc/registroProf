from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)
utente = None  # Variabile globale per l'utente loggato

# Funzione per leggere il registro da file
def leggiRegistro(filePath):
    try:
        with open(filePath, "r") as file:
            return json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

# Funzione per aggiungere un nuovo voto al registro
def scriviRegistro(dati, nomeProf, materia, voto):
    prof = {
        "nomeProf": nomeProf,
        "materia": materia,
        "voto": voto,
        "nome": utente["username"]
    }
    dati.append(prof)

# Funzione per salvare il registro su file
def scriviFile(filePath, dati):
    with open(filePath, "w") as file:
        json.dump(dati, file, indent=4)

# Carica gli utenti dal file
def load_users():
    utentiFilePath = 'C:\\Users\\23-info-03\\Desktop\\RegistroProf\\registro\\utenti.json'
    with open(utentiFilePath, 'r') as f:
        return json.load(f)

@app.route('/')
def index():
    return redirect(url_for('home'))

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    global utente  # Corretto: usiamo la variabile globale

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        users = load_users()
        for user in users:
            if user['username'] == username and user['password'] == password:
                utente = user
                return redirect(url_for('server_page'))

        return render_template('login.html', error='Credenziali errate')

    return render_template('login.html')

@app.route('/registro')
def server_page():
    return render_template("server.html")

@app.route('/inserisci', methods=['POST'])
def inserisci():
    nomeProf = request.form['nomeProf']
    materia = request.form['materia']
    voto = request.form['voto']

    filePath = os.path.join(app.static_folder, 'registro.json')
    dati = leggiRegistro(filePath)
    
    scriviRegistro(dati, nomeProf, materia, voto)
    scriviFile(filePath, dati)
    
    return "Success", 200

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for
import json, os

app = Flask(__name__)
utente = None

def leggiRegistro(filePath):
    file = open(filePath, "r")
    try:
        dati = json.load(file)
        return dati
    except json.JSONDecodeError:
        return []

def scriviRegistro(dati, nomeProf, materia, voto):
    prof = {
        "nomeProf": nomeProf,
        "materia": materia,
        "voto": voto,
        "nome": utente["username"]
    }
    dati.append(prof)

def scriviFile(filePath, dati):
    file = open(filePath, "wt")
    json.dump(dati, file)

def load_users():
    utentiFilePath = os.path.join(app.static_folder, 'c:\\Users\\23-info-03\\Desktop\\RegistroProf\\registro\\utenti.json')
    with open(utentiFilePath, 'r') as f:
        return json.loads(f.read())

@app.route('/')
def index():
    return redirect(url_for('home'))

@app.route('/home')
def home():
    return render_template('index.html')  # Mostra la pagina index.html all'avvio

@app.route('/login', methods=['GET', 'POST'])
def login():
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
    
    return 200, "Success"

if __name__ == '__main__':
    app.run(debug=True)

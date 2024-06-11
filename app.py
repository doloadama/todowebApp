import random
import re
import mysql.connector
from flask import Flask, render_template, request, session, redirect, jsonify, url_for
import requests
from googletrans import Translator


from faker import Faker

fake = Faker('fr_FR')
translator = Translator()

app = Flask(__name__)
app.secret_key = '123456789@1234'

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="toto",
        database="todo"
    )

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/view-tasks')
def view_tasks_page():
    return render_template('view_tache.html')

@app.route('/api/tasks', methods=['GET'])
def api_tasks():
    offset = int(request.args.get('offset', 0))
    limit = int(request.args.get('limit', 10))  # la limite par défaut est 10
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, titre, description, statut, id_user FROM tache LIMIT %s OFFSET %s", (limit, offset))
    tasks = cursor.fetchall()
    cursor.close()
    conn.close()

    #Réccupérer les id des utilisateurs
    existe_id = []
    t= []
    for t in tasks:
        existe_id.append(t['id'])
    print(existe_id)

    # Si le nombre de tâches récupérées est inférieur à la limite demandée
    if len(tasks) < limit:
        tache_add = limit - len(tasks)

        # Récupérer les tâches additionnelles depuis l'API externe
        response = requests.get(f'https://jsonplaceholder.typicode.com/todos?_limit={tache_add}')
        if response.status_code == 200:
            tache_additionnelles = response.json()
            #cursor.execute('INSERT INTO tache ${tache_additionneles[0]}')
            for tache in tache_additionnelles:
                # Convertir les clé pour correspondre au schéma de la table
                tache['titre'] = tache.pop('title', 'No title')
                tache['description'] = fake.text()
                tache['statut'] = 'complete' if tache['completed'] else 'incomplete'

                #Vérifier si l'id dans le
                if tache['id'] in existe_id:
                    tache['id'] = random.randint(1, 200)

                if  tache['id_user'] in [t['user_id'] for t in tasks]:
                    tache['id_user'] = random.randint(1, 50)

            tasks.extend(tache_additionnelles)

    return jsonify(tasks)

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password,))
        account = cursor.fetchone()
        cursor.close()
        conn.close()
        if account:
            session['loggedin'] = True
            session['id'] = account[0]
            session['username'] = account[1]
            msg = 'Logged in successfully!'
            return render_template('view_tache.html')
        else:
            msg = 'Incorrect username/password!'
    return render_template('login.html', msg=msg)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password:
            msg = 'Please fill out the form!'
        else:
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            conn.commit()
            msg = 'You have successfully registered!'
        cursor.close()
        conn.close()
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('register.html', msg=msg)


@app.route('/ajouter', methods=['GET', 'POST'])
def ajouter():
    msg = ''
    if request.method == 'POST':
        titre = request.form.get('titre')
        description = request.form.get('description')
        statut = request.form.get('statut')


        if not titre or not description or not statut:
            msg = 'Remplir les champs!'
        else:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM tache WHERE titre=%s", (titre,))
            task = cursor.fetchone()
            if task:
                msg = 'La tâche existe déjà!'
            else:
                try:
                    # Insert the task into the database
                    cursor.execute("INSERT INTO tache (titre, description, statut, id_user) VALUES (%s, %s, %s, %s)",
                                   (titre, description, statut, session['id']))
                    conn.commit()
                    msg = 'Task ajoutée avec succes!'
                except Exception as e:
                    msg = f"Une erreur est survenue: {e}"
                finally:
                    cursor.close()
                    conn.close()
    return render_template('view_tache.html', msg=msg)


@app.route('/modifier/<int:id>', methods=['GET', 'POST'])
def modifier(id):
    if request.method == 'POST':
        titre = request.form['titre']
        description = request.form['description']
        statut = request.form['statut']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE tache SET titre=%s, description=%s, statut=%s WHERE id=%s",
                       (titre, description, statut, id))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/view-tasks')
    else:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tache WHERE id=%s", (id,))
        task = cursor.fetchone()
        cursor.close()
        conn.close()
        return render_template('modifier.html', tache=task)


@app.route('/supprimer/<int:id>', methods=['POST'])
def supprimer(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Récupérer la tâche avant de la supprimer
    cursor.execute("SELECT * FROM tache WHERE id=%s", (id,))
    task = cursor.fetchone()

    if task:
        # Insérer la tâche dans la table des tâches archivées
        cursor.execute(
            "INSERT INTO tache_archive (id, titre, description, statut, id_user) VALUES (%s, %s, %s, %s, %s)",
            (task['id'], task['titre'], task['description'], task['statut'], task['id_user']))
        # Supprimer la tâche de la table des tâches
        cursor.execute("DELETE FROM tache WHERE id=%s", (id,))
        conn.commit()

    cursor.close()
    conn.close()
    return ('', 204)

@app.route('/api/archived-tasks', methods=['GET'])
def api_archived_tasks():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tache_archive")
    tasks = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(tasks)



if __name__ == '__main__':
    app.run(debug=True)

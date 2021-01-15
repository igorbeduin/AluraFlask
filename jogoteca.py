from flask import Flask, render_template, request, redirect, session, flash, url_for

app = Flask(__name__)
app.secret_key = 'blabla'

class Usuario:
    def __init__(self, id, nome, senha):
        self.id = id
        self.nome = nome
        self.senha = senha

class Jogo:
    def __init__(self, nome, categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console

User1 = Usuario("Igor", 'igor', '1234')
User2 = Usuario("Fulano", 'fules', '5678')
users = {User1.id: User1, User2.id: User2}

jogo1 = Jogo("Super Mario", "Acao", "SNES")
jogo2 = Jogo("Pokemon Gold", "RPG", "GBA")
lista = [jogo1, jogo2]

@app.route("/")
def index():
    return render_template("lista.html", titulo="Jogos", jogos=lista)

@app.route("/novo")
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    return render_template("novo.html", titulo="Novo Jogo")

@app.route("/criar", methods=["POST"])
def criar():
    nome = request.form["nome"]
    categoria = request.form["categoria"]
    console = request.form["console"]
    lista.append(Jogo(nome, categoria, console))
    return redirect(url_for('index'))

@app.route("/login")
def login():    
    return render_template("login.html", proxima=request.args.get('proxima'))

@app.route("/autenticar", methods=["POST"])
def autenticar():
    if request.form['usuario'] in users:
        usuario = users[request.form['usuario']]
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.id
            flash(usuario.nome + " logou com sucesso!")
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)

    else:
        flash("Tente novamente")
        return redirect(url_for('login'))

@app.route("/logout")
def logout():
    session['usuario_logado'] = None
    flash("Nenhum usuario logado")
    return redirect(url_for('index'))

app.run(debug=True)

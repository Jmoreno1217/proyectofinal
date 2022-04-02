from flask import Flask, render_template, request, session, redirect
from funciones import funciones
from passlib.hash import sha256_crypt

app=Flask(__name__)
app.secret_key ='lwiu74dhn2SuF3w'
logeado = 0
tipo = str
diccionarioUsuarios = funciones.lee_diccionario_usuarios('usuarios.csv')
@app.route("/")
def index():
    global logeado
    global tipo
    return render_template("index.html",log = logeado,tipo = tipo)

@app.route("/login", methods=['GET','POST'])
def login():
    global logeado
    global tipo
    if 'logged_in' in session:
        if session['logged_in'] == True:
            logeado = 1
    if request.method == 'GET':
        return render_template("login.html")
    else:
        if request.method == 'POST':
            usuario = request.form['username']
            password = request.form['password']
            print(diccionarioUsuarios[usuario]['password'])
            if usuario in diccionarioUsuarios:
                password_hashed = sha256_crypt.hash(diccionarioUsuarios[usuario]['password'])
                contrasenia_correcta = sha256_crypt.verify(password,password_hashed)
                if contrasenia_correcta == True:
                    session['username'] = usuario
                    session['nombre']   = diccionarioUsuarios[usuario]['nombreCompleto']
                    session['logged_in']= True
                    tipo = diccionarioUsuarios[usuario]['tipo']
                    return redirect("/")
                else:
                    msg = f'La contraseña es incorrecta para el usuario: {usuario}.'
                    return render_template("login.html",mensaje=msg)
@app.route("/logout", methods=['GET'])
def logout():
    global logeado
    global tipo
    session.clear()
    logeado = 0
    tipo = None
    return redirect("/")

@app.route("/usuarios")
def listaUsuarios():
    return render_template("usuarios.html", diccUsuarios = diccionarioUsuarios)

@app.route("/usuariova/<usuario>")
def vistaUsuarioAdmin(usuario):
    print(usuario)
    print(diccionarioUsuarios[usuario])
    return render_template("usuariova.html",usuario = diccionarioUsuarios[usuario])
if __name__ == "__main__":
    logeado = 0
    app.run(debug=True)
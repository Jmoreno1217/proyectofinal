from asyncio.windows_events import NULL
from flask import Flask, render_template, request, session, redirect
from funciones import funciones
from passlib.hash import sha256_crypt
import datetime
from usuario import usuario1

app=Flask(__name__)
app.secret_key ='lwiu74dhn2SuF3w'
logeado = False
tipo = str
usuarioActivo=NULL
diccionarioUsuarios = funciones.lee_diccionario_usuarios('usuarios.csv')
diccionarioServicios = funciones.lee_diccionario_servicios('servicios.csv')
diccCliente = {'Agendar cita':'/agendar_cita','Historial de recetas':'/historial_recetas','Historial de atención':'/historial_atencion'}
diccUsuario = {'Agendar cita':'/agendar_cita','Historial de recetas':'/historial_recetas','Historial de atención':'/historial_atencion','Agregar una receta':'/agregar_receta', 'Agregar una atención':'/agregar_atencion'}
diccAdmin = {'Agendar cita':'/agendar_cita','Historial de recetas':'/historial_recetas',
                'Historial de atención':'/historial_atencion','Agregar una receta':'/agregar_receta', 'Agregar una atención':
                '/agregar_atencion','Usuarios':'/usuarios','Medicinas':'/medicinas','Servicios':'/servicios','Informe de ventas diarias':'/ventas_diarias','Informe de ventas mensuales':'/ventas_mensuales'}
def pagNoEncontrada():
    return redirect("/pag_no_encontrada")

@app.route("/")
def index():
    print(diccionarioServicios)
    global logeado
    global tipo
    global usuarioActivo
    if logeado==False:
        return render_template("index.html",log = logeado,tipo = diccCliente)
    elif usuarioActivo.tipo == 'cliente':
        return render_template("index.html",log = logeado,tipo = diccCliente)
    elif usuarioActivo.tipo=='usuario':
        return render_template("index.html",log = logeado,tipo = diccUsuario)
    elif usuarioActivo.tipo=='administrador':
        return render_template("index.html",log = logeado,tipo = diccAdmin)
    else:
        return render_template("index.html",log = logeado,tipo = diccCliente)

@app.route("/login", methods=['GET','POST'])
def login():
    global logeado
    global tipo
    global usuarioActivo
    if request.method == 'GET':
        return render_template("login.html")
    else:
        try:
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
                        usuarioActivo=usuario1(diccionarioUsuarios[usuario]['id'],
                                               diccionarioUsuarios[usuario]['usuario'],
                                               diccionarioUsuarios[usuario]['nombreCompleto'],
                                               diccionarioUsuarios[usuario]['password'],
                                               diccionarioUsuarios[usuario]['correo'],
                                               diccionarioUsuarios[usuario]['tipo'])
                        #usuarioActivo.id=diccionarioUsuarios[usuario]['id']
                        #usuarioActivo.usuario=diccionarioUsuarios[usuario]['usuario']
                        #usuarioActivo.nombreCompleto=diccionarioUsuarios[usuario]['nombreCompleto']
                        #usuarioActivo.password=diccionarioUsuarios[usuario]['password']
                        #usuarioActivo.correo=diccionarioUsuarios[usuario]['correo']
                        #usuarioActivo.tipo=diccionarioUsuarios[usuario]['tipo']
                        tipo = diccionarioUsuarios[usuario]['tipo']
                        if 'logged_in' in session:
                            if session['logged_in'] == True:
                                logeado = True
                            else:
                                logeado = False 
                        return redirect("/")
                    else:
                        msg = f'La contraseña es incorrecta para el usuario: {usuario}.'
                        return render_template("login.html",mensaje=msg)
        except:
                msg = f'No esta registrado el usuario ingresado.'
                return render_template("login.html",mensaje=msg)
@app.route("/logout", methods=['GET'])
def logout():
    global logeado
    global tipo
    session.clear()
    logeado = False
    tipo = None
    return redirect("/")

@app.route("/usuarios")
def listaUsuarios():
    global tipo
    if tipo != "administrador":
        return redirect("/acceso_restringido")
    return render_template("usuarios.html", diccUsuarios = diccionarioUsuarios)

@app.route("/usuariova/<usuario>")
def vistaUsuarioAdmin(usuario):    
    global tipo
    if tipo != "administrador":
        return redirect("/acceso_Restringido")
    print(usuario)
    print(diccionarioUsuarios[usuario])
    return render_template("usuariova.html",usuario = diccionarioUsuarios[usuario])

@app.route("/servicios")
def vistaServicios():
    return render_template("servicios.html",servicios=diccionarioServicios)

@app.route("/agendar_cita", methods=['GET','POST'])
def crearCita():
    global logeado
    global usuarioActivo
    print(logeado)
    if logeado==False:
        return redirect("/login")
    diccionarioCitas = funciones.lee_diccionario_citas('citas.csv')
    if request.method == "GET":
        if tipo=="cliente":
            return render_template("citaC.html")
        else:
            return render_template("citaU.html", dictUsuarios = diccionarioUsuarios)
    else:
        if request.method=="POST":
            if usuarioActivo.tipo == 'cliente':
                id= len(diccionarioCitas)+1
                idCliente = usuarioActivo.id
                nombre_paciente = request.form['nombre_paciente']
                tipo2 = request.form['tipo']
                servicio = request.form['atencion']
                fecha = request.form['fecha']
                hora_cita = request.form['hora_cita']
                temp =[id, idCliente,nombre_paciente,tipo2,servicio,fecha,hora_cita]
            else:
                id= len(diccionarioCitas)+1
                idCliente = request.form['cliente']
                nombre_paciente = request.form['nombre_paciente']
                tipo2 = request.form['tipo']
                servicio = request.form['atencion']
                fecha = request.form['fecha']
                hora_cita = request.form['hora_cita']
                temp =[id, idCliente,nombre_paciente,tipo2,servicio,fecha,hora_cita]
            try:
                funciones.escribir_archivo("citas.csv",temp)
                if tipo=="cliente":
                    return render_template("citaC.html", mensaje = "Cita registrada!!!")
                else:
                    return render_template("citaU.html",dictUsuarios = diccionarioUsuarios, mensaje = "Cita registrada!!!")
            except:
                if tipo=="cliente":
                    return render_template("citaC.html", mensaje = "Ha ocurrido un error, intente mas tarde o solicite asistencia.")
                else:
                    return render_template("citaU.html",dictUsuarios = diccionarioUsuarios, mensaje = "Ha ocurrido un error, intente mas tarde o solicite asistencia.")

@app.route("/agregar_atencion", methods=['GET','POST'])
def crearAtencion():
    global logeado
    global usuarioActivo
    print(logeado)
    if logeado==False:
        return redirect("/login")
    diccionarioCitas = funciones.lee_diccionario_citas('citas.csv')
    if request.method == "GET":
        if tipo=="cliente":
            return redirect("/acceso_restringido")
        else:
            return render_template("citaA.html", dictUsuarios = diccionarioUsuarios)
    else:
        if request.method=="POST":
            x = datetime.datetime.now()
            id= len(diccionarioCitas)+1
            idCliente = request.form['cliente']
            nombre_paciente = request.form['nombre_paciente']
            tipo2 = request.form['tipo']
            servicio = request.form['atencion']
            fecha = x.strftime("%Y") + "-" + x.strftime("%m")+"-"+x.strftime("%d")
            hora_cita = x.strftime("%H")+":"+x.strftime("%M")
            temp =[id, idCliente,nombre_paciente,tipo2,servicio,fecha,hora_cita]
            try:
                funciones.escribir_archivo("citas.csv",temp)
                return render_template("citaA.html",dictUsuarios = diccionarioUsuarios, mensaje = "Cita registrada!!!")
            except:
                return render_template("citaA.html",dictUsuarios = diccionarioUsuarios, mensaje = "Ha ocurrido un error, intente mas tarde o solicite asistencia.")

@app.route("/acceso_restringido")
def accesoRestringido():
    return render_template("nopermiso.html",log = logeado)
if __name__ == "__main__":
    logeado = False
    app.run(debug=True)

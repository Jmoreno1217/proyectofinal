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
diccionarioMedicamentos = funciones.lee_diccionario_medicamentos('medicamentos.csv')
diccCliente = {'Agendar cita':'/agendar_cita','Historial de recetas':'/historial_recetas','Historial de atención':'/historial_atencion'}
diccUsuario = {'Agendar cita':'/agendar_cita','Historial de recetas':'/historial_recetas','Historial de atención':'/historial_atencion','Agregar una receta':'/agregar_receta', 'Agregar una atención':'/agregar_atencion'}
diccAdmin = {'Agendar cita':'/agendar_cita','Historial de recetas':'/historial_recetas',
                'Historial de atención':'/historial_atencion','Agregar una receta':'/agregar_receta', 'Agregar una atención':
                '/agregar_atencion','Usuarios':'/usuarios','Medicamentos':'/medicamentos','Servicios':'/servicios','Informe de ventas diarias':'/ventas_diarias','Informe de ventas mensuales':'/ventas_mensuales'}

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
    global logeado
    if logeado==False:
        return redirect("/login")
    if tipo != "administrador":
        return redirect("/acceso_restringido")
    diccionarioUsuarios = funciones.lee_diccionario_usuarios('usuarios.csv')
    return render_template("usuarios.html", diccUsuarios = diccionarioUsuarios)

@app.route("/usuariova/<usuario>")
def vistaUsuarioAdmin(usuario):    
    global tipo
    global logeado
    if logeado==False:
        return redirect("/login")
    if tipo != "administrador":
        return redirect("/acceso_restringido")
    print(usuario)
    print(diccionarioUsuarios[usuario])
    return render_template("usuariova.html",usuario = diccionarioUsuarios[usuario])

@app.route("/servicios")
def vistaServicios():
    global tipo
    global logeado
    if logeado==False:
        return redirect("/login")
    if tipo != "administrador":
        return redirect("/acceso_restringido")
    diccionarioServicios = funciones.lee_diccionario_servicios('servicios.csv')
    return render_template("servicios.html",servicios=diccionarioServicios, diccUsuarios = diccionarioUsuarios)

@app.route("/agendar_cita", methods=['GET','POST'])
def crearCita():
    global logeado
    global usuarioActivo
    print(logeado)
    if logeado==False:
        return redirect("/login")
    diccionarioUsuarios = funciones.lee_diccionario_usuarios('usuarios.csv')
    diccionarioServicios = funciones.lee_diccionario_servicios('servicios.csv')
    if request.method == "GET":
        if tipo=="cliente":
            return render_template("citaC.html")
        else:
            return render_template("citaU.html", dictUsuarios = diccionarioUsuarios)
    else:
        if request.method=="POST":
            if usuarioActivo.tipo == 'cliente':
                x = datetime.datetime.now()
                id= funciones.generar_id(diccionarioServicios)
                idCliente = usuarioActivo.id
                nombre_paciente = request.form['nombre_paciente']
                tipo2 = request.form['tipo']
                servicio = request.form['atencion']
                fecha = request.form['fecha']
                hora_cita = request.form['hora_cita']
                temp =[id, idCliente,nombre_paciente,tipo2,servicio,fecha,hora_cita]
                temp2 =[id, "cita"]
            else:
                x = datetime.datetime.now()
                id= funciones.generar_id(diccionarioServicios)
                idCliente = request.form['cliente']
                nombre_paciente = request.form['nombre_paciente']
                tipo2 = request.form['tipo']
                servicio = request.form['atencion']
                fecha = request.form['fecha']
                hora_cita = request.form['hora_cita']
                temp =[id, idCliente,nombre_paciente,tipo2,servicio,fecha,hora_cita]
                temp2 =[id, "cita"]
            try:
                funciones.escribir_archivo("servicios.csv",temp2)
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
    if logeado==False:
        return redirect("/login")
    diccionarioUsuarios = funciones.lee_diccionario_usuarios('usuarios.csv')
    diccionarioServicios = funciones.lee_diccionario_servicios('servicios.csv')
    if request.method == "GET":
        if tipo=="cliente":
            return redirect("/acceso_restringido")
        else:
            return render_template("citaA.html", dictUsuarios = diccionarioUsuarios)
    else:
        if request.method=="POST":
            x = datetime.datetime.now()
            id= funciones.generar_id(diccionarioServicios)
            idCliente = request.form['cliente']
            nombre_paciente = request.form['nombre_paciente']
            tipo2 = request.form['tipo']
            servicio = request.form['atencion']
            fecha = x.strftime("%Y") + "-" + x.strftime("%m")+"-"+x.strftime("%d")
            hora_cita = x.strftime("%H")+":"+x.strftime("%M")
            temp =[id, idCliente,nombre_paciente,tipo2,servicio,fecha,hora_cita]
            temp2 =[id, "cita"]
            try:
                funciones.escribir_archivo("servicios.csv",temp2)
                funciones.escribir_archivo("citas.csv",temp)
                return render_template("citaA.html",dictUsuarios = diccionarioUsuarios, mensaje = "Cita registrada!!!")
            except:
                return render_template("citaA.html",dictUsuarios = diccionarioUsuarios, mensaje = "Ha ocurrido un error, intente mas tarde o solicite asistencia.")

@app.route("/cita/<id>")
def detalleCita(id):
    global logeado
    if logeado==False:
        return redirect("/login")
    diccCita = funciones.lee_diccionario_citas("citas.csv")
    cita = diccCita[id]
    print(cita['idCliente'])
    idcliente = cita['idCliente']
    cliente = str
    for usuario in diccionarioUsuarios.items():
        if usuario[1]['id'] == idcliente:
            cliente = usuario[1]['nombreCompleto']
    return render_template("detalleCita.html", cita = cita, cliente = cliente)

@app.route("/medicamentos")
def verMedicamentos():
    global tipo
    global logeado
    if logeado==False:
        return redirect("/login")
    if tipo != "administrador":
        return redirect("/acceso_restringido")
    diccionarioMedicamentos = funciones.lee_diccionario_medicamentos('medicamentos.csv')
    return render_template("medicamentos.html", medicamentos = diccionarioMedicamentos)

@app.route("/medicamento/<codigo>")
def medicamentoEspesifico(codigo):
    global tipo
    global logeado
    if logeado==False:
        return redirect("/login")
    if tipo != "administrador":
        return redirect("/acceso_restringido")
    diccionarioMedicamentos = funciones.lee_diccionario_medicamentos('medicamentos.csv')
    medicamento=diccionarioMedicamentos[codigo]
    return render_template("descMedicamento.html", medicamento = medicamento)

@app.route("/añadir_medicina", methods=['GET','POST'])
def agregarMedicina():
    global tipo
    global logeado
    if logeado==False:
        return redirect("/login")
    if tipo != "administrador":
        return redirect("/acceso_restringido")
    if request.method=="GET":
        return render_template("agregarMedicina.html")
    else:
        if request.method == "POST":
            codigo = request.form['codigo']
            nombre_medicamento = request.form['nombre_medicamento']
            formula = request.form['formula']
            formula = formula.replace(',','☺')
            administracion = request.form['administracion']
            presentacion = request.form['presentacion']
            tipo_animal = request.form['tipo_animal']
            try:
                medicamento=[codigo, nombre_medicamento, formula, administracion, presentacion, tipo_animal]
                funciones.escribir_archivo("medicamentos.csv", medicamento)
                return render_template("agregarMedicina.html", mensaje= "Medicamento agregado con exito!!!")
            except:
                return render_template("agregarMedicina.html", mensaje= "Ha ocurrido un error, intente mas tarde o solicite asistencia.")
                pass
            pass
    pass

@app.route("/acceso_restringido")
def accesoRestringido():
    return render_template("sinpermiso.html",log = logeado)

if __name__ == "__main__":
    logeado = False
    #s = funciones.generar_id(funciones.lee_diccionario_servicios("servicios.csv"))
    #print(s)
    app.run(debug=True)

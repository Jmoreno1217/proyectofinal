'''
    Equipo:
        -Alvarez Portillo, Lilian Yeitnaletzi.
        -Badachi Benitez, Yubitza Adamaris.
        -Moreno Laines, Juan Pedro.
    Materia: Desarollo de Sistemas 4.
    Fecha de entrega: 06 de Mayo de 2022.
    Creditos:
        -Diseño de formularios: https://codepen.io/
        -Diseño de la pantilla base: AlexCG Design (https://www.youtube.com/channel/UCm0q786c9bW9FiQvesV126A)
'''
from ast import Pass
from asyncio.windows_events import NULL
from flask import Flask, render_template, request, session, redirect, url_for
from funciones import funciones
from passlib.hash import sha256_crypt
import datetime
from usuario import usuario1
from flask_weasyprint import render_pdf

app=Flask(__name__)
app.secret_key ='lwiu74dhn2SuF3w'
logeado = False
tipo = str
usuarioActivo=NULL
diccionarioUsuarios = funciones.lee_diccionario_usuarios('usuarios.csv')
diccionarioServicios = funciones.lee_diccionario_servicios('servicios.csv')
diccionarioMedicamentos = funciones.lee_diccionario_medicamentos('medicamentos.csv')
diccIndexCliente = {'Agendar cita':'/agendar_cita','Historial de recetas':'/historial_recetas','Historial de atención':'/historial_atencion'}
diccIndexUsuario = {'Agendar cita':'/agendar_cita','Historial de recetas':'/historial_recetas','Historial de atención':'/historial_atencion','Agregar una receta':'/agregar_receta', 'Agregar una atención':'/agregar_atencion'}
diccIndexAdmin = {'Agendar cita':'/agendar_cita','Historial de recetas':'/historial_recetas',
                'Historial de atención':'/historial_atencion','Agregar una receta':'/agregar_receta', 'Agregar una atención':
                '/agregar_atencion','Usuarios':'/usuarios','Medicamentos':'/medicamentos','Servicios':'/servicios','Informe de ventas diarias':'/ventas_diarias','Informe de ventas mensuales':'/ventas_mensuales'}

@app.route("/")
def index():
    print(diccionarioServicios)
    global logeado
    global tipo
    global usuarioActivo
    if logeado==False:
        return render_template("index.html",log = logeado,tipo = diccIndexCliente)
    elif usuarioActivo.tipo == 'cliente':
        return render_template("index.html",log = logeado,tipo = diccIndexCliente)
    elif usuarioActivo.tipo=='usuario':
        return render_template("index.html",log = logeado,tipo = diccIndexUsuario)
    elif usuarioActivo.tipo=='administrador':
        return render_template("index.html",log = logeado,tipo = diccIndexAdmin)
    else:
        return render_template("index.html",log = logeado,tipo = diccIndexCliente)

@app.route("/login", methods=['GET','POST'])
def login():
    global logeado
    global tipo
    global usuarioActivo
    diccionarioUsuarios=funciones.lee_diccionario_usuarios("usuarios.csv")
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

@app.route("/cambiar_contraseña", methods=['GET','POST'])
def passMod():
    if request.method == 'GET':
        return render_template("passMod.html")
    else:
        if request.method=='POST':
            diccionarioUsuarios=funciones.lee_diccionario_usuarios("usuarios.csv")
            try:
                if request.method == 'POST':
                    usuario = request.form['username']
                    password = request.form['password']
                    npass = request.form['npassword']
                    if usuario in diccionarioUsuarios and diccionarioUsuarios[usuario]['password']==password:
                        user = diccionarioUsuarios[usuario]
                        funciones.cambiaContrasena(user, npass, "usuarios.csv")
                        return redirect("/login")
                    else:
                        return render_template('passMod',usuario=usuario,mensaje='Las credenciales no coinciden con ninguna almacenada, intente de nuevo.')
            except:
                    msg = f'No esta registrado el usuario ingresado.'
                    return render_template("passMod.html",mensaje=msg)
    

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

@app.route("/agregar_usuario", methods=['GET','POST'])
def agregarUsuarioAdmin():
    global tipo
    global logeado
    if logeado==False:
        return redirect("/login")
    if tipo != "administrador":
        return redirect("/acceso_restringido")
    diccionarioUsuarios = funciones.lee_diccionario_usuarios('usuarios.csv')
    if request.method=="GET":
        return render_template("agregarUsuario.html",admin = 1)
        pass
    else:
        if request.method=="POST":
            try:
                id = funciones.generar_id_usuario(diccionarioUsuarios)
                user = request.form['user']
                nombreCompleto = request.form['nombreCompleto']
                password = request.form['password']
                correo = request.form['correo']
                tipo2= request.form['tipo']
                tipo2= tipo2.lower()
                temp = [id,user,nombreCompleto,password,correo,tipo2]
                funciones.escribir_archivo("usuarios.csv",temp)
                return render_template("agregarUsuario.html",admin = 1, mensaje="Usuario agregado con exito!!!")
            except:
                return render_template("agregarUsuario.html",admin = 1, mensaje="Ha ocurrido un error, intente mas tarde o solicite asistencia.")

@app.route("/usuariova/<usuario>")
def vistaUsuarioAdmin(usuario):    
    global tipo
    global logeado
    if logeado==False:
        return redirect("/login")
    if tipo != "administrador":
        return redirect("/acceso_restringido")
    diccionarioUsuarios = funciones.lee_diccionario_usuarios('usuarios.csv')
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
                id= funciones.generar_id(diccionarioServicios)
                idCliente = usuarioActivo.id
                nombre_paciente = request.form['nombre_paciente']
                tipo2 = request.form['tipo']
                servicio = request.form['atencion']
                fecha = request.form['fecha']
                hora_cita = request.form['hora_cita']
                temp =[id, idCliente,nombre_paciente,tipo2,servicio,fecha,hora_cita]
                temp2 =[id, "cita", "0"]
            else:
                id= funciones.generar_id(diccionarioServicios)
                idCliente = request.form['cliente']
                nombre_paciente = request.form['nombre_paciente']
                tipo2 = request.form['tipo']
                servicio = request.form['atencion']
                fecha = request.form['fecha']
                hora_cita = request.form['hora_cita']
                temp =[id, idCliente,nombre_paciente,tipo2,servicio,fecha,hora_cita]
                temp2 =[id, "cita", fecha, "50"]
            try:
                funciones.escribir_archivo("servicios.csv",temp2)
                funciones.escribir_archivo("citas.csv",temp)
                if tipo=="cliente":
                    doc="r"+id
                    url="/pdf/"+doc
                    return redirect(url)
                    #return render_template("citaC.html", mensaje = "Cita registrada!!!")
                else:
                    doc="r"+id
                    url="/pdf/"+doc
                    return redirect(url)
                    #return render_template("citaU.html",dictUsuarios = diccionarioUsuarios, mensaje = "Cita registrada!!!")
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
    if tipo == "cliente":
        return redirect("/acceso_restringido")
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
            temp2 =[id, "atencion",fecha,"50"]
            try:
                funciones.escribir_archivo("servicios.csv",temp2)
                funciones.escribir_archivo("citas.csv",temp)
                doc="A"+id
                url="/pdf/"+doc
                return redirect(url)
                #return render_template("citaA.html",dictUsuarios = diccionarioUsuarios, mensaje = "Cita registrada!!!")
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
    return render_template("detalleCita.html", cita = cita, cliente = cliente, mensaje = "Cita")

@app.route("/citarecibo/<id>")
def citaRecibo(id):
    global logeado
    if logeado==False:
        return redirect("/login")
    diccCita = funciones.lee_diccionario_citas("citas.csv")
    cita = diccCita[id]
    print(cita['idCliente'])
    idcliente = cita['idCliente']
    cliente = str
    x=datetime.datetime.now()
    fechaE= x.strftime("%Y") + "-" + x.strftime("%m")+"-"+x.strftime("%d")
    for usuario in diccionarioUsuarios.items():
        if usuario[1]['id'] == idcliente:
            cliente = usuario[1]['nombreCompleto']
    return render_template("recibo.html", cita = cita, cliente = cliente, mensaje = "Cita", fechaE = fechaE)

@app.route("/atencion/<id>")
def detalleAtencion(id):
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
    return render_template("detalleCita.html", cita = cita, cliente = cliente, mensaje = "Atención")

@app.route("/atencionrecibo/<id>")
def atencionRecibo(id):
    global logeado
    if logeado==False:
        return redirect("/login")
    diccCita = funciones.lee_diccionario_citas("citas.csv")
    cita = diccCita[id]
    print(cita['idCliente'])
    idcliente = cita['idCliente']
    cliente = str
    x=datetime.datetime.now()
    fechaE= x.strftime("%Y") + "-" + x.strftime("%m")+"-"+x.strftime("%d")
    for usuario in diccionarioUsuarios.items():
        if usuario[1]['id'] == idcliente:
            cliente = usuario[1]['nombreCompleto']
    mensaje = "Atención"
    return render_template("recibo.html", cita = cita, cliente = cliente, mensaje=mensaje, fechaE = fechaE)

@app.route("/receta/<id>")
def detalleReceta(id):
    global logeado
    if logeado==False:
        return redirect("/login")
    diccRecetas=funciones.lee_diccionario_recetas("recetas.csv")
    receta = diccRecetas[id]
    return render_template("detalleReceta.html",receta = receta)

@app.route("/recetarecibo/<id>")
def reciboReceta(id):
    global logeado
    #if logeado==False:
     #   return redirect("/login")
    diccRecetas=funciones.lee_diccionario_recetas("recetas.csv")
    diccCita = funciones.lee_diccionario_citas("citas.csv")
    diccionarioUsuarios = funciones.lee_diccionario_usuariosID('usuarios.csv')
    diccionarioServicios = funciones.lee_diccionario_servicios('servicios.csv')
    cita = diccCita[diccRecetas[id]['id_cita']]
    medicamentos = diccRecetas[id]['medicamentosRecetados']
    medicamentos = medicamentos.replace("☺",",")
    indicaciones = diccRecetas[id]['detalles']
    indicaciones = indicaciones.replace("☺",",")
    idcliente= cita['idCliente']
    cliente = diccionarioUsuarios[idcliente]
    nombreCliente = cliente['nombreCompleto']
    receta = diccRecetas[id]
    mascota = cita['nombreMascota']
    servicio = diccionarioServicios[id]
    subTotal = str(servicio['subTotal'])
    iva = (float(subTotal)*0.16)
    total = float(subTotal)+float(iva)
    return render_template("receta.html",receta = receta, nombre = nombreCliente, mascota = mascota, medicamentos = medicamentos, indicaciones = indicaciones, subTotal = subTotal, iva = iva, total = total)

@app.route("/detalle/<id>")
def detalleReceta2(id):
    global logeado
    if logeado==False:
        return redirect("/login")
    diccionarioServicios = funciones.lee_diccionario_servicios('servicios.csv')
    cita = "/cita/"+id
    atencion = "/atencion/"+id
    if diccionarioServicios[id]['tipo'] == "cita":
        return redirect(cita)
    elif diccionarioServicios[id]['tipo'] == "atencion":
        return redirect(atencion)


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
            precio = request.form['precio']
            try:
                medicamento=[codigo, nombre_medicamento, formula, administracion, presentacion, tipo_animal, precio]
                funciones.escribir_archivo("medicamentos.csv", medicamento)
                return render_template("agregarMedicina.html", mensaje= "Medicamento agregado con exito!!!")
            except:
                return render_template("agregarMedicina.html", mensaje= "Ha ocurrido un error, intente mas tarde o solicite asistencia.")
                pass
            pass
    pass

@app.route("/agregar_receta", methods=['GET','POST'])
def agregarReceta():
    diccionarioCitas=funciones.lee_diccionario_citas("citas.csv")
    diccionarioServicios = funciones.lee_diccionario_servicios('servicios.csv')
    diccionarioMedicamentos = funciones.lee_diccionario_medicamentos('medicamentos.csv')
    if logeado==False:
        return redirect("/login")
    if tipo == "cliente":
        return redirect("/acceso_restringido")
    if request.method=="GET":
        return render_template("agregarReceta.html",dictCitas=diccionarioCitas,dictMedicamentos=diccionarioMedicamentos)
        pass
    else:
        if request.method=="POST":
            id= funciones.generar_id(diccionarioServicios)
            id_cita=request.form['id_cita']
            medicamentosRecetados=request.form['medicamentosRecetados']
            print(medicamentosRecetados)
            medicamentosRecetados=medicamentosRecetados.replace("\"","")
            medicamentosRecetados=medicamentosRecetados.replace(",","☺")
            print(medicamentosRecetados)
            detalles=request.form['detalles']
            detalles=detalles.replace("\"","")
            detalles=detalles.replace(",","☺")
            fecha=request.form['fecha']
            subTotal=request.form['subTotal']
            receta = [id,id_cita,medicamentosRecetados,detalles,fecha]
            servicio = [id,"receta",fecha,subTotal]
            try:
                funciones.escribir_archivo("servicios.csv",servicio)
                funciones.escribir_archivo("recetas.csv",receta)
                #return render_template("agregarReceta.html",dictCitas=diccionarioCitas, mensaje="Receta registrada con exito!!!")
                url = "/pdf/R"+id
                return redirect(url)
            except:
                return render_template("agregarReceta.html",dictCitas=diccionarioCitas, mensaje="Ha ocurrido un error, intente mas tarde o solicite asistencia.")

@app.route("/historial_recetas")
def historialRecetas():
    if logeado==False:
        return redirect("/login")
    if tipo == "cliente":
        url = "/historial_recetas/"+usuarioActivo.id
        return redirect(url)
    else:
        return redirect("/buscar_recetas_usuario")

@app.route("/buscar_recetas_usuario", methods=['GET','POST'])
def buscarRecetasUsuario():
    if logeado==False:
        return redirect("/login")
    if tipo == "cliente":
        url = "/historial_recetas/"+usuarioActivo.id
        return redirect(url)
    if request.method == "GET":
        dictUsuarios = funciones.lee_diccionario_usuarios("usuarios.csv")
        return render_template("historialRecetasGenerico.html", dictClientes=dictUsuarios)
    else:
        if request.method == "POST":
            url = "/historial_recetas/"+request.form['id_cliente']
            return redirect(url)

@app.route("/historial_recetas/<id>")
def historialRecetasCliente(id):
    if logeado==False:
        return redirect("/login")
    diccrecetas = {}
    diccRecetas=funciones.lee_diccionario_recetas("recetas.csv")
    diccCitas = funciones.lee_diccionario_citas("citas.csv")
    try:
        for receta in diccRecetas:
            for cita in diccCitas:
                if diccRecetas[receta]['id_cita']==diccCitas[cita]['id'] and diccCitas[cita]['idCliente']==id:
                    diccrecetas[diccRecetas[receta]['id_receta']]=diccRecetas[receta]
        if len(diccrecetas)==0:
            return render_template("historialRecetas.html", mensaje="El usuario no tiene ninguna receta registrada.")    
        return render_template("historialRecetas.html",diccrecetas=diccrecetas)
    except:
        return render_template("historialRecetas.html", mensaje="Ha ocurrido un error, intentelo mas tarde o solicite asistencia.")
    


@app.route("/historial_atencion")
def historialAtencion():
    if logeado==False:
        return redirect("/login")
    if tipo == "cliente":
        url = "/historial_atencion/"+usuarioActivo.id
        return redirect(url)
    else:
        return redirect("/buscar_atencion_usuario")

@app.route("/buscar_atencion_usuario", methods=['GET','POST'])
def buscarAtencionUsuario():
    if logeado==False:
        return redirect("/login")
    if tipo == "cliente":
        url = "/historial_atencion/"+usuarioActivo.id
        return redirect(url)
    if request.method == "GET":
        dictUsuarios = funciones.lee_diccionario_usuarios("usuarios.csv")
        return render_template("historialAtencionGenerico.html", dictClientes=dictUsuarios)
    else:
        if request.method == "POST":
            url = "/historial_atencion/"+request.form['id_cliente']
            return redirect(url)

@app.route("/historial_atencion/<id>")
def historialAtencionCliente(id):
    if logeado==False:
        return redirect("/login")
    diccatencion = {}
    diccCitas = funciones.lee_diccionario_citas("citas.csv")
    diccservicios=funciones.lee_diccionario_servicios("servicios.csv")
    try:
        for cita in diccCitas:
            if diccCitas[cita]['idCliente']==id:
                print(id)
                print(diccCitas[cita]['idCliente'])
                diccatencion[diccCitas[cita]['id']]=diccCitas[cita]
        if len(diccatencion)==0:
            return render_template("historialAtencion.html",mensaje="El usuario no tiene ninguna cita o atencion registrada.")    
        return render_template("historialAtencion.html",servicios=diccservicios,diccCitas=diccatencion)
    except:
        return render_template("historialAtencion.html",mensaje="Ha ocurrido un error, intentelo mas tarde o solicite asistencia.")

@app.route("/acceso_restringido")
def accesoRestringido():
    return render_template("sinpermiso.html",log = logeado)

@app.route("/ventas_diarias", methods=['GET','POST'])
def ventasDiarias():
    global tipo
    global logeado
    if logeado==False:
        return redirect("/login")
    if tipo != "administrador":
        return redirect("/acceso_restringido")
    if request.method=="GET":
        return render_template("formInformeDia.html")
    else:
        if request.method=="POST":
            try:
                diccionarioServicios=funciones.lee_diccionario_servicios("servicios.csv")
                diccServicio = {}
                diccIVA = {}
                diccTotal = {}
                subTotal2=0
                iva2=0
                totalNeto=0
                for servicio in diccionarioServicios:
                    if diccionarioServicios[servicio]['fecha']==request.form['fecha']:
                        print(diccionarioServicios[servicio])
                        diccServicio[servicio]=diccionarioServicios[servicio]
                        diccIVA[servicio]=float(diccionarioServicios[servicio]['subTotal'])*0.16
                        diccTotal[servicio]=float(diccionarioServicios[servicio]['subTotal'])+float(diccIVA[servicio])
                        subTotal2+=float(diccionarioServicios[servicio]['subTotal'])
                        iva2+=diccIVA[servicio]
                        totalNeto+=diccTotal[servicio]
                        print(diccServicio[servicio])
                return render_template("informeDia.html",diccServicio = diccServicio, diccIVA =diccIVA, diccTotal = diccTotal,subTotal2 = subTotal2, IVA2=iva2, totalNeto=totalNeto, fecha = request.form['fecha'])
            except:
                return render_template("formInformeDia.html", mensaje = "Error.")

@app.route("/informe_diario/<id>")
def informe_diario(id):
    global tipo
    global logeado
    if logeado==False:
        return redirect("/login")
    if tipo != "administrador":
        return redirect("/acceso_restringido")
    try:
        diccionarioServicios=funciones.lee_diccionario_servicios("servicios.csv")
        diccServicio = {}
        diccIVA = {}
        diccTotal = {}
        subTotal2=0
        iva2=0
        totalNeto=0
        for servicio in diccionarioServicios:
            if diccionarioServicios[servicio]['fecha']==id:
                print(diccionarioServicios[servicio])
                diccServicio[servicio]=diccionarioServicios[servicio]
                diccIVA[servicio]=float(diccionarioServicios[servicio]['subTotal'])*0.16
                diccTotal[servicio]=float(diccionarioServicios[servicio]['subTotal'])+float(diccIVA[servicio])
                subTotal2+=float(diccionarioServicios[servicio]['subTotal'])
                iva2+=diccIVA[servicio]
                totalNeto+=diccTotal[servicio]
                print(diccServicio[servicio])
                x = datetime.datetime.now()
                fecha2 = x.strftime("%A")+", "+  x.strftime("%d")+" de "+x.strftime("%B") + " del " + x.strftime("%y")+"."
        return render_template("informeDiaI.html",diccServicio = diccServicio, diccIVA =diccIVA, diccTotal = diccTotal,subTotal2 = subTotal2, IVA2=iva2, totalNeto=totalNeto, fecha = id, fecha2 = fecha2)
    except:
        return render_template("formInformeDia.html", mensaje = "Error.")

@app.route("/ventas_mensuales", methods=['GET','POST'])
def ventasMensuales():
    global tipo
    global logeado
    if logeado==False:
        return redirect("/login")
    if tipo != "administrador":
        return redirect("/acceso_restringido")
    if request.method == "GET":
        return render_template("formInformeMes.html")
    else:
        if request.method == "POST":
            x = datetime.datetime.now()
            fecha = x.strftime("%d")+"-"+x.strftime("%M")+"-"+x.strftime("%Y")
            anioC = x.strftime("%Y")
            if int(request.form['anio']) < 2022 or int(request.form['anio']) > int(anioC):
                return render_template("formInformeMes.html", mensaje = "El año ingresado no esta dentro del periodo que lleva en servicio la veternaria, ingrese un valor valido.")
            if request.form['mes'] == "Enero":
                mes = "01"
            elif request.form['mes'] == "Febrero":
                mes = "02"
            elif request.form['mes'] == "Marzo":
                mes = "03"
            elif request.form['mes'] == "Abril":
                mes = "04"
            elif request.form['mes'] == "Mayo":
                mes = "05"
            elif request.form['mes'] == "Junio":
                mes = "06"
            elif request.form['mes'] == "Julio":
                mes = "07"
            elif request.form['mes'] == "Agosto":
                mes = "08"
            elif request.form['mes'] == "Septiembre":
                mes = "09"
            elif request.form['mes'] == "Octubre":
                mes = "10"
            elif request.form['mes'] == "Noviembre":
                mes = "11"
            elif request.form['mes'] == "Diciembre":
                mes = "12"
            anio = request.form['anio']
            anioMes = str(anio)+"-"+str(mes)
            print(anioMes)
            try:
                diccionarioServicios=funciones.lee_diccionario_servicios("servicios.csv")
                diccServicio = {}
                diccIVA = {}
                diccTotal = {}
                subTotal2=0
                iva2=0
                totalNeto=0
                for servicio in diccionarioServicios:
                    print(diccionarioServicios[servicio]['fecha'][:7])
                    if diccionarioServicios[servicio]['fecha'][:7]==anioMes:
                        print(diccionarioServicios[servicio])
                        diccServicio[servicio]=diccionarioServicios[servicio]
                        diccIVA[servicio]=float(diccionarioServicios[servicio]['subTotal'])*0.16
                        diccTotal[servicio]=float(diccionarioServicios[servicio]['subTotal'])+float(diccIVA[servicio])
                        subTotal2+=float(diccionarioServicios[servicio]['subTotal'])
                        iva2+=diccIVA[servicio]
                        totalNeto+=diccTotal[servicio]
                        print(diccServicio[servicio])
                return render_template("informeMes.html",diccServicio = diccServicio, diccIVA =diccIVA, diccTotal = diccTotal, subTotal2 = subTotal2, IVA2=iva2, totalNeto=totalNeto, anio = anio, mes = request.form['mes'] , anioMes=anioMes, fecha=fecha)
            except:
                return render_template("formInformeMes.html", mensaje = "Error.")
        
@app.route("/informe_mensual/<id>")
def informe_mensual(id):
    global tipo
    global logeado
    if logeado==False:
        return redirect("/login")
    if tipo != "administrador":
        return redirect("/acceso_restringido")
    anioMes=id
    anioC = anioMes[:4]
    mes = anioMes[5:]
    try:
        diccionarioServicios=funciones.lee_diccionario_servicios("servicios.csv")
        diccServicio = {}
        diccIVA = {}
        diccTotal = {}
        subTotal2=0
        iva2=0
        totalNeto=0
        for servicio in diccionarioServicios:
            print(diccionarioServicios[servicio]['fecha'][:7])
            if diccionarioServicios[servicio]['fecha'][:7]==anioMes:
                print(diccionarioServicios[servicio])
                diccServicio[servicio]=diccionarioServicios[servicio]
                diccIVA[servicio]=float(diccionarioServicios[servicio]['subTotal'])*0.16
                diccTotal[servicio]=float(diccionarioServicios[servicio]['subTotal'])+float(diccIVA[servicio])
                subTotal2+=float(diccionarioServicios[servicio]['subTotal'])
                iva2+=diccIVA[servicio]
                totalNeto+=diccTotal[servicio]
                print(diccServicio[servicio])
        return render_template("informeMesI.html",diccServicio = diccServicio, diccIVA =diccIVA, diccTotal = diccTotal, subTotal2 = subTotal2, IVA2=iva2, totalNeto=totalNeto, anio = anioC, mes = mes)
    except:
        return render_template("formInformeMes.html", mensaje = "Error.")

@app.route("/modificar_usuario/<user>", methods=['GET', 'POST'])
def modificarUsuarioAdmin(user):
    global tipo
    global logeado
    if logeado==False:
        return redirect("/login")
    if tipo != "administrador":
        return redirect("/acceso_restringido")
    dictUsuarios = funciones.lee_diccionario_usuariosID("usuarios.csv")
    if request.method=="GET":
        usuario = dictUsuarios[user]
        return render_template("modUsuario.html",usuario = usuario)
        pass
    else:
        if request.method=="POST":
            try:
                usuario = dictUsuarios[user]
                usuario['usuario'] = request.form['user']
                usuario['nombreCompleto'] = request.form['nombreCompleto']
                usuario['password'] = usuario['password']
                usuario['correo'] = request.form['correo']
                usuario['tipo'] = request.form['tipo']
                usuario['tipo'] = usuario['tipo'].lower()
                funciones.modificarUsuario("usuarios.csv",usuario=usuario)
                return render_template("modUsuario.html",usuario = usuario, mensaje="Usuario modificado con exito!!!")
            except:
                return render_template("modUsuario.html",usuario = usuario, mensaje="Ha ocurrido un error, intentelo de nuevo o solicite asistencia.")
                pass
            pass

@app.route("/pdf/<documento>", methods=['GET'])
def imprimir(documento):
    diccDocumentos={
        'r':'recibo_cita',
        'a':'recibo_atencion',
        'R':'receta',
        'i':'informe_diario',
        'I':'informe_mensual'
    }
    tipoDocumento= documento[0]
    docID=documento[1:]
    if tipoDocumento=='r':
        url="/citarecibo/"+docID
    if tipoDocumento=='R':
        url="/recetarecibo/"+docID
    if tipoDocumento=='A':
        url="/atencionrecibo/"+docID
    if tipoDocumento=='i':
        url="/informe_diario/"+docID
    if tipoDocumento=='I':
        url="/informe_mensual/"+docID
    if request.method=="GET":
        return render_pdf(url)
        pass


if __name__ == "__main__":
    logeado = False
    #s = funciones.generar_id(funciones.lee_diccionario_servicios("servicios.csv"))
    #print(s)
    app.run(debug=True)
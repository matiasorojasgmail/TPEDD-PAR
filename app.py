## 1. EXTRUCTURA
#### 1.1 MODULOS UTILIZADOS
#####################################   MODULOS UTILIZADOS   ##############################################################################
from flask import Flask, render_template, session, request, redirect , url_for ,flash 
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, InputRequired, Length
from flask_wtf.csrf import CSRFProtect, CSRFError
from flask_script import Manager
import csv
#####################################   MODULOS UTILIZADOS   ##############################################################################

#### 1.2 CLASES GENERADAS
#####################################   CLASES   ##############################################################################
# Generada para que Iniciar sesion.
class Mi_Login(FlaskForm):
		usuario = StringField('Usuario:', validators=[DataRequired()])
		contraseña = PasswordField('Contraseña:', validators=[DataRequired()])
		submit = SubmitField('Ingresar')

# Generada para registrase como usuarios.
class Registro(FlaskForm):
    usuario = StringField('Usuario' , validators=[DataRequired()]) 
    clave0 = PasswordField('Contraseña',validators=[DataRequired()])
    clave1 = PasswordField(' Validar Contraseña',validators=[DataRequired()])
    submit = SubmitField('Registrar')   

# Generada para CONSULTAS, que el usuario ingrese un cliente y le liste los productos que compro el cliente ingresado.
class Cliente_Productos(FlaskForm):
    clientes = StringField('Cliente' , validators=[DataRequired()]) 
    submit = SubmitField('Buscar')  

# Generada para CONSULTAS, que el usuario ingrese un producto y le liste los clientes que compraron dicho producto.
class Producto_Cliente(FlaskForm):
    producto = StringField('Producto' , validators=[DataRequired()]) 
    submit = SubmitField('Buscar') 

# Generada para validar archivo CSV
class Validar_Csv(FlaskForm):
    submit = SubmitField('Validar Base de DatosCSV') 
#####################################   CLASES   ##############################################################################



app = Flask(__name__)
bootstrap = Bootstrap(app)
manager = Manager(app)


# Seguridad de Contraseña Secreta
app.config['SECRET_KEY'] = "matiasrojasmatiasrojasmatiasrojas"
csrf = CSRFProtect(app)


#Inicio web, se define url default y url /index
@app.route('/', methods=['GET', 'POST'])
@app.route('/index')
def index():
    if 'username' in session:
        return render_template('inicio.html')
    return render_template('inicio.html')

# Inicio donde el usuario podra validar sus credenciales y tener acceso a validar base de datos y panel de consultas.
@app.route('/ingresar', methods=['GET', 'POST'])
def iniciodesesion():
    inicio = Mi_Login()
    if inicio.validate_on_submit():
        nombre_archivo = "usuarios"   
        with open(nombre_archivo) as archivo:
            archivo_csv = csv.reader(archivo)
            for linea in archivo_csv:
                valores = linea
                user = valores[0]
                con = valores[1]
                if user == inicio.usuario.data and con == inicio.contraseña.data:
                    session['username'] = inicio.usuario.data
                    return redirect('/validarcsv')
            else:
                flash('Usuario y/o Contrasña No Validos')               
    return render_template('iniciarsesion.html', login=inicio)


# Cerrar sesion donde el usuario podra cerrar su sesion activa.
@app.route('/cerrarsesion')
def logout():
    if 'username' in session:
        session.pop('username')
        return redirect('/ingresar')
    else:
        return redirect('/ingresar')


# Registrar donde el usuario podra generar sus datos de acceso a la web.
@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    reg = Registro()
    if reg.validate_on_submit():
        if reg.clave0.data == reg.clave1.data:
            nombre_archivo = "usuarios" 
            with open('csv', 'a') as archivo:
                archivo_csv = csv.writer(archivo)
                registro = [reg.usuario.data, reg.clave1.data]
                archivo_csv.writerow(registro)
                flash('Registrado Correctamente')
                return redirect('/ingresar')
        else:
            flash('Error al validar Contraseña, No son iguales')
    return render_template('registrarse.html', datos=reg)

# ValidarCSV una vez que el usuario inicie sesion debera validar la base de datos.
@app.route('/validarcsv', methods=['GET','POST'])
def validarcsv():
    validarbasededatos = Validar_Csv()
    if validarbasededatos.validate_on_submit():
        nombre_archivo = "ventas"
        with open(nombre_archivo) as archivo:
            archivo_csv = csv.DictReader(archivo)
            listadic = list(archivo_csv)
            #valida la cantidad de columnas
            campos = 5
            for item in listadic:
                if len(item) != campos:  
                  flash('·ERROR· Verificar Cantidad de CAMPOS en BASE DE DATOS')   
                  flash('Contacte al administrador')        
                  return render_template('validarcsv.html', dato=validarbasededatos)
            for item in listadic:             
               if (item['CODIGO']) == "" or (item['CODIGO']) == " ":
                  flash('·ERROR· Verificar Columna CODIGO en BASE DE DATOS')   
                  flash('Contacte al administrador')        
                  return render_template('validarcsv.html', dato=validarbasededatos)
            for item in listadic:             
               if (item['PRODUCTO']) == "" or (item['PRODUCTO']) == " ":
                  flash('·ERROR· Verificar Columna PRODUCTO en BASE DE DATOS') 
                  flash('Contacte al administrador')            
                  return render_template('validarcsv.html', dato=validarbasededatos)
            for item in listadic:             
               if (item['CLIENTE']) == "" or (item['CLIENTE']) == " ":
                  flash('·ERROR· Verificar Columna CLIENTE en BASE DE DATOS') 
                  flash('Contacte al administrador')            
                  return render_template('validarcsv.html', dato=validarbasededatos)
            for item in listadic:             
               if (item['CANTIDAD']) == "" or (item['CANTIDAD']) == " " or float(item['CANTIDAD']) % 1 != 0 :
                  flash('·ERROR· Verificar Columna CANTIDAD en BASE DE DATOS') 
                  flash('Contacte al administrador')            
                  return render_template('validarcsv.html', dato=validarbasededatos)
        flash('BASE DE DATOS APROBADA CORRECTAMENTE')          
        #return render_template('val_07_verificadooko.html')
        return redirect('/paneldeconsultas')
    return render_template('validarcsv.html', dato=validarbasededatos)




# Panel de Consultas donde usuario que inicio sesion podra realizar consultas segun necesidad.
@app.route('/paneldeconsultas',methods=['GET' , 'POST'])
def paneldeconsultas():
    if 'username' in session:
        nombre_archivo = 'ventas' 
        with open(nombre_archivo) as archivo:
            listar = csv.reader(archivo)
            return render_template('paneldeconsultas.html',listar=listar)
    else:
        flash('Debe Iniciar Sesion para acceder al PANEL DE CONSULTAS')
        return redirect('/ingresar')

#####################################   CONSULTAS   ##############################################################################
# Consulta Cliente donde podra realizar consultas de productos que compro x cliente.
@app.route('/consultacliente', methods=['GET','POST'])
def consultacliente():
    if 'username' in session:
        ingresarcliente = Cliente_Productos()
        if ingresarcliente.validate_on_submit():
            nombre_archivo = "ventas"
            with open(nombre_archivo) as archivo:
                reader = csv.reader(archivo)
                clientequeingreso = ingresarcliente.clientes.data
                producto1 = []   
                listaproductosfinal = []
                for line in reader:
                    if line [2] == clientequeingreso:
                        producto1.append(line[1])
                for i in producto1:
                    if i not in listaproductosfinal:
                        listaproductosfinal.append(i)
                if len(listaproductosfinal) == 0:
                    flash('CLIENTE NO ENCONTRADO') 
                    return render_template('consultacliente.html', dato=ingresarcliente)
            return render_template('productoquecomprocliente.html', listaproductosfinal=listaproductosfinal, clientequeingreso=clientequeingreso)
        return render_template('consultacliente.html', dato=ingresarcliente)
    else:
        flash('Debe Iniciar Sesion para acceder a esta Informacion')
        return redirect('/ingresar')

# Consulta Producto donde podra realizar consultas de clientes que compraron x productos.
@app.route('/consultaproducto', methods=['GET','POST'])
def consultaproducto():
    if 'username' in session:
        ingresarproducto = Producto_Cliente()
        if ingresarproducto.validate_on_submit():
            nombre_archivo = "ventas"  
            with open(nombre_archivo) as archivo:
                reader = csv.reader(archivo)
                productoqueingreso = ingresarproducto.producto.data
                cliente1 = [] 
                listaclientesfinal = []       
                for line in reader:
                    if line [1] == productoqueingreso:
                        cliente1.append(line[2])
                for i in cliente1:
                    if i not in listaclientesfinal:
                        listaclientesfinal.append(i)
                if len(listaclientesfinal) == 0:
                    flash('PRODUCTO NO ENCONTRADO') 
                    return render_template('consultaproducto.html', dato=ingresarproducto)
            return render_template('clientequecomproproducto.html', listaclientesfinal=listaclientesfinal, productoqueingreso=productoqueingreso)
        return render_template('consultaproducto.html', dato=ingresarproducto)
    else:
        flash('Debe Iniciar Sesion para acceder a esta Informacion')
        return redirect('/ingresar')

# Producto mas Vendido donde listara clientes que compraron x productos y los ordenara segun cantidad.
@app.route('/productosmasvendidos', methods=['GET','POST'])
def mejorproducto():
    if 'username' in session:
        nombre_archivo = "ventas"
        with open(nombre_archivo) as archivo:
            archivo_csv = csv.DictReader(archivo)
            farmase = list(archivo_csv)
            listado = []
            dictado = []       
            lista3 = []
            for t in farmase:
                if t["PRODUCTO"] not in listado: 
                    listado.append(t["PRODUCTO"])
                    dictado.append(t["CODIGO"])
            for p in range(len(listado)):            
                lista3.append([listado[p],dictado[p],0])       
            for c in farmase:
                for z in range(len(listado)):
                    if c["PRODUCTO"] == lista3[z][0]:
                        cantidad = lista3[z][2]
                        unidades = float(c["CANTIDAD"])                     
                        cantidad += unidades
                        lista3[z][2] = cantidad
            lista3.sort(key=lambda x:x[2], reverse=True)
        return render_template('productosmasvendidos.html', lista3=lista3)
    else:
        flash('Debe Iniciar Sesion para acceder a esta Informacion')
        return redirect('/ingresar')

# Mejor Cliente donde listara clientes que gastaron mas dinero y lo ordenara segun quien gasto mas.
@app.route('/mejoresclientes', methods=['GET','POST'])
def mejoresclientes():
    if 'username' in session:
        nombre_archivo = "ventas"
        with open(nombre_archivo) as archivo:
            archivo_csv = csv.DictReader(archivo)
            farmase = list(archivo_csv)
            listado = []
            dictado = []       
            for t in farmase:
                if t["CLIENTE"] not in listado: 
                    listado.append(t["CLIENTE"])
            for p in range(len(listado)):            
                dictado.append([listado[p],0])       
            for c in farmase:
                for z in range(len(listado)):
                    if c["CLIENTE"] == listado[z]:
                        precio = dictado[z][1]
                        unidades = float(c["CANTIDAD"]) 
                        valor = float(c["PRECIO"])
                        precio += valor * unidades
                        dictado[z][1] = precio
            dictado.sort(key=lambda x:x[1], reverse=True)
        return render_template('mejoresclientes.html', dictado=dictado)
    else:
        flash('Debe Iniciar Sesion para acceder al Panel de esta Informacion')
        return redirect('/ingresar')

#####################################   CONSULTAS   ##############################################################################





#####################################   ERRORES   ##############################################################################

@app.errorhandler(404)
def no_encontrado(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def error_interno(e):
    return render_template('500.html'), 500

#####################################   ERRORES   ##############################################################################

if __name__ == "__main__":
    app.run(debug=True)
    manager.run()

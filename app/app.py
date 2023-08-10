from flask import Flask, render_template, url_for, request, redirect, flash, make_response
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect

from werkzeug.security import check_password_hash as checkph
from werkzeug.security import generate_password_hash as genph
import bcrypt
import pdfkit

import calendar
from flask_login import LoginManager, login_user, logout_user, login_required

from Models.ModelUser import ModuleUser
from Models.entities.user import User




app=Flask(__name__)


csrf=CSRFProtect()

#inicio de programa

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='anbar'


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
ruta=app.config['UPLOAD_FOLDER']='./app/static/img/productos'


db=MySQL(app)
app.secret_key='mysecretkey'

Login_manager_app=LoginManager(app)

@Login_manager_app.user_loader
def load_user(idusuarios):
    return ModuleUser.get_by_id(db,idusuarios)

@app.route('/logout')
def logout():
    logout_user()
    return render_template('login.html')

#archivos jpg
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#Generar PDF de producto en otra ventana
@app.route('/alumno/PDF')
def ver_producto_PDF():
    print(id)
    cur=db.connection.cursor()
    sql="SELECT * FROM productos"
    cur.execute(sql)
    productos=cur.fetchall()
    cur.close()
    config = pdfkit.configuration(wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')
    # Renderizar el template HTML con los datos obtenidos
    options  ={
        'page-size' : 'Letter',
        'margin-top' : '0px',
        'margin-right' : '0px',
        'margin-bottom' : '0px',
        'margin-left' : '0px',
        'encoding': "UTF-8",
    }
    html = render_template('productosPDF.html', productos=productos)
    pdf = pdfkit.from_string(html, False, configuration=config, options=options)
    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "inline; filename=ProductoPDF.pdf"
    return response
    # Generar el PDF a partir del HTML renderizado
    #pdfkit.from_string(html, 'alumnoVer.pdf', configuration=config, options=options)

    #return 'Reporte generado correctamente'

    #return render_template('alumnoVer.html', alumno=alumno[0])


# inicio de clases


@app.route("/inicio")
def index():
    cur=db.connection.cursor()
    sql="select * from productos AS P INNER JOIN categorias AS C ON P.id_cat=C.id WHERE C.nombre LIKE '%favoritos%' ORDER BY P.id desc"
    cur.execute(sql)
    productos=cur.fetchall()
    print(productos)
    
    cur2=db.connection.cursor()
    sql2="SELECT * FROM comentarios"
    cur2.execute(sql2)
    comentarios=cur2.fetchall()



    return render_template('index.html', productos=productos,comentarios=comentarios)



@app.route("/admin")
@login_required
def admin():
    cur=db.connection.cursor()
    sql="select * from productos order by precio desc"
    cur.execute(sql)
    productos=cur.fetchall()
    print(productos)
    return render_template('administrador.html', productos=productos)


@app.route("/registro2")
def registro2():
    cur=db.connection.cursor()
    sql="select * from productos order by precio desc"
    cur.execute(sql)
    productos=cur.fetchall()
    print(productos)
    return render_template('registro2.html', productos=productos)


@app.route("/registro")
def registrar():
    cur=db.connection.cursor()
    sql="select * from productos order by precio desc"
    cur.execute(sql)
    productos=cur.fetchall()
    print(productos)
    return render_template('registro.html', productos=productos)

@app.route("/terminos")
def terminos():
    cur=db.connection.cursor()
    sql="select * from productos order by precio desc"
    cur.execute(sql)
    productos=cur.fetchall()
    print(productos)
    return render_template('tyc.html', productos=productos)


@app.route("/cont")
def conta():
    cur=db.connection.cursor()
    sql="select * from productos order by precio desc"
    cur.execute(sql)
    productos=cur.fetchall()
    print(productos)
    return render_template('contacto.html', productos=productos)


@app.route("/inf")
def info():
    cur=db.connection.cursor()
    sql="select * from productos order by precio desc"
    cur.execute(sql)
    productos=cur.fetchall()
    print(productos)
    return render_template('pagina inf.html', productos=productos)

@app.route("/of")
def ofe():
    cur=db.connection.cursor()
    sql="select * from productos AS P INNER JOIN categorias AS C ON P.id_cat=C.id WHERE C.nombre LIKE '%fiestas%' ORDER BY P.id desc"
    cur.execute(sql)
    productos=cur.fetchall()
    print(productos)
    return render_template('ofertas.html', productos=productos)


@app.route("/blanc")
def blanco():
    cur=db.connection.cursor()
    sql="select * from productos order by precio desc"
    cur.execute(sql)
    productos=cur.fetchall()
    print(productos)
    return render_template('blanca.html', productos=productos[0])



@app.route("/papa")
def papas():
    cur=db.connection.cursor()
    sql="select * from productos AS P INNER JOIN categorias AS C ON P.id_cat=C.id WHERE C.nombre LIKE '%papa%' ORDER BY P.id desc"
    cur.execute(sql)
    productos=cur.fetchall()
    print(productos)
    return render_template('papa.html', productos=productos)

@app.route("/mama")
def mamas():
    cur=db.connection.cursor()
    sql="select * from productos AS P INNER JOIN categorias AS C ON P.id_cat=C.id WHERE C.nombre LIKE '%mama%' ORDER BY P.id desc"
    cur.execute(sql)
    productos=cur.fetchall()
    print(productos)
    return render_template('mama.html', productos=productos)

@app.route("/carrito")
def carrito():
    cur=db.connection.cursor()
    sql="select * from productos AS P INNER JOIN categorias AS C ON P.id_cat=C.id WHERE C.nombre LIKE '%cajas%' ORDER BY P.id desc"
    cur.execute(sql)
    productos=cur.fetchall()
    print(productos)
    return render_template('carroo.html', productos=productos)




#Apartado CRUD de Productos
#Create (Crear)
@app.route('/alumno/nuevo')
@login_required
def alumno_Crear():
    return render_template('alumnoCrear.html',)

@app.route('/alumno/agregar', methods=['POST'])
def producto_Agregar():
    if request.method == 'POST':
        Nombre=request.form['Nombre']
        precio=request.form['precio']
        cat=request.form['cate']
        disponibilidad=request.form['disponobilidad']
        imagen=request.form['imagen']
        imagen2=request.form['imagen2']
        descripcion=request.form['desc']
        cur=db.connection.cursor()
        sql="INSERT INTO productos (nombre, precio, id_cat, disponibilidad, imagen, imagen2, descripcion) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        valores=(Nombre, precio, cat, disponibilidad, imagen, imagen2, descripcion)
        cur.execute(sql,valores)
        db.connection.commit()

        flash('¡Producto agregado exitosamente!')

        return redirect(url_for('producto_Ver'))

        #Read (Leer)
@app.route('/alumnos')
def producto_Ver():
    cur=db.connection.cursor()
    sql="SELECT * FROM productos ORDER BY id desc"
    cur.execute(sql)
    productos=cur.fetchall()
    print(productos) 
    return render_template('alumnos.html', productos=productos)

@app.route('/alumno/<string:id>')

def ver_producto(id):
    print(id)
    cur=db.connection.cursor()
    sql="SELECT * FROM productos WHERE id={0}".format(id)
    cur.execute(sql)
    producto=cur.fetchall()
    print(producto[0])
    return render_template('alumnoVer.html', producto=producto[0])

#vistas descripcion
@app.route('/vistas/<string:id>')
def detalles_productos(id):
    print(id)
    cur=db.connection.cursor()
    sql="SELECT * FROM productos WHERE id={0}".format(id)
    cur.execute(sql)
    producto=cur.fetchall()
    print(producto[0])
    return render_template('blanca.html', producto=producto[0])

#Update (Actualizar)
@app.route('/cliente/editar/<string:id>')

def editar_producto(id):
    print(id)
    cur=db.connection.cursor()
    sql="SELECT * FROM productos WHERE id={0}".format(id)
    cur.execute(sql)
    producto=cur.fetchall()
    print(producto[0])
    cur.close()
    return render_template('alumnoEditar.html', producto=producto[0])

@app.route('/alumno/actualizar/<string:id>', methods=['POST'])

def producto_actualizar(id):
    if request.method == 'POST':
        Nombre=request.form['Nombre']
        cat=request.form['categoria']
        precio=request.form['precio']
        disponobilidad=request.form['disponobilidad']
        imagen=request.form['imagen']
        imagen2=request.form['imagen2']
        descripcion=request.form['desc']
        cur=db.connection.cursor()
        sql="UPDATE productos SET nombre=%s, id_cat=%s, precio=%s, disponibilidad=%s, imagen=%s, imagen2=%s, descripcion=%s WHERE id=%s"        
        valores=(Nombre,cat, precio, disponobilidad, imagen, imagen2, descripcion, id)
        cur.execute(sql,valores)
        db.connection.commit()
        cur.close()
        flash('¡Producto modificado exitosamente!')
    return redirect(url_for('producto_Ver'))

#Delete (Borrar)
@app.route('/alumno/eliminar/<string:id>')
def eliminar_producto(id):
    print(id)
    cur=db.connection.cursor()
    sql="DELETE FROM productos WHERE id={0}".format(id)
    cur.execute(sql)
    db.connection.commit()
    flash('¡producto eliminado correctamente!')
    return redirect(url_for('producto_Ver'))




#CRUD para categorias
#crear
@app.route('/categorias')

def categorias_Crear():
    return render_template('categoriasCrear.html')

@app.route('/categorias/agregar', methods=['POST'])

def categoria_Agregar():
    if request.method == 'POST':
        Nombre=request.form['Nombre']
        descripcion=request.form['descripcion']
        cur=db.connection.cursor()
        sql="INSERT INTO categorias (nombre, descripcion) VALUES (%s, %s)"
        valores=(Nombre, descripcion)
        cur.execute(sql,valores)
        db.connection.commit()

        flash('¡categoria agregada exitosamente!')

        return redirect(url_for('categorias_Ver'))

#leer
@app.route('/cate')
def categorias_Ver():
    cur=db.connection.cursor()
    sql="SELECT * FROM categorias ORDER BY id desc"
    cur.execute(sql)
    productos=cur.fetchall()
    print(productos) 
    return render_template('categorias.html', productos=productos)

@app.route('/categorias/<string:id>')
def ver_categorias(id):
    print(id)
    cur=db.connection.cursor()
    sql="SELECT * FROM categorias WHERE id={0}".format(id)
    cur.execute(sql)
    producto=cur.fetchall()
    print(producto[0])
    return render_template('categoriaVer.html', producto=producto[0])

#Update (Actualizar)
@app.route('/categ/editar/<string:id>')
def editar_categoria(id):
    print(id)
    cur=db.connection.cursor()
    sql="SELECT * FROM categorias WHERE id={0}".format(id)
    cur.execute(sql)
    alumno=cur.fetchall()
    print(alumno[0])
    return render_template('categoriaEditar.html', alumno=alumno[0])

@app.route('/cate/actualizar/<string:id>', methods=['POST'])
def categoria_actualizar(id):
    if request.method == 'POST':
        Nombre=request.form['Nombre']
        Matricula=request.form['Matricula']

        cur=db.connection.cursor()
        sql="UPDATE categorias SET nombre=%s, descripcion=%s WHERE id=%s"        
        valores=(Nombre, Matricula, id)
        cur.execute(sql,valores)
        db.connection.commit()

        flash('¡categoria modificado exitosamente!')
    return redirect(url_for('categorias_Ver'))



#Delete (Borrar)
@app.route('/categoria/eliminar/<string:id>')
def eliminar_categoria(id):
    print(id)
    cur=db.connection.cursor()
    sql="DELETE FROM categorias WHERE id={0}".format(id)
    cur.execute(sql)
    db.connection.commit()
    flash('¡producto eliminado correctamente!')
    return redirect(url_for('categorias_Ver'))



#CRUD para usuarios
#crear
@app.route('/usuarios')
def usuarios_Crear():
    return render_template('registro.html')

@app.route('/usuarios/agregar', methods=['POST'])
def usuario_Agregar():
    if request.method == 'POST':
        Nombre=request.form['Nombre']
        ap=request.form['email']
        am=request.form['pass']
        
        
        cur=db.connection.cursor()
        
        pwd=genph(am)
        
        sql="INSERT INTO clientes (nombre, email, contrasena) VALUES (%s, %s, %s)"
        valores=(Nombre, ap, pwd,)
        cur.execute(sql,valores)
        db.connection.commit()

        flash('¡Usuario agregada exitosamente!')

        return redirect(url_for('index'))

       


#Read (Leer)
@app.route('/usu')
def usuarios_Ver():
    cur=db.connection.cursor()
    sql="SELECT * FROM clientes ORDER BY id desc"
    cur.execute(sql)
    productos=cur.fetchall()
    print(productos) 
    return render_template('usuarios.html', productos=productos)

@app.route('/usuario/<string:id>')
def ver_usuario(id):
    print(id)
    cur=db.connection.cursor()
    sql="SELECT * FROM clientes WHERE id={0}".format(id)
    cur.execute(sql)
    producto=cur.fetchall()
    print(producto[0])
    return render_template('usuariosVer.html', producto=producto[0])



#Update (Actualizar)
@app.route('/usuario/editar/<string:id>')
def editar_usuario(id):
    print(id)
    cur=db.connection.cursor()
    sql="SELECT * FROM clientes WHERE id={0}".format(id)
    cur.execute(sql)
    alumno=cur.fetchall()
    print(alumno[0])
    return render_template('usuarioEditar.html', alumno=alumno[0])

@app.route('/usuario/actualizar/<string:id>', methods=['POST'])
def usuario_actualizar(id):
    if request.method == 'POST':
        Nombre=request.form['Nombre']
        ap=request.form['email']
        am=request.form['contrasena']
        cur=db.connection.cursor()
        sql="UPDATE clientes SET nombre=%s, email=%s, contraseña=%s  WHERE id=%s"        
        valores=(Nombre, ap, am, id)
        cur.execute(sql,valores)
        db.connection.commit()

        flash('¡categoria modificado exitosamente!')
    return redirect(url_for('usuarios_Ver'))


#Delete (Borrar)
@app.route('/usuario/eliminar/<string:id>')
def eliminar_usuario(id):
    print(id)
    cur=db.connection.cursor()
    sql="DELETE FROM clientes WHERE id={0}".format(id)
    cur.execute(sql)
    db.connection.commit()
    flash('¡producto eliminado correctamente!')
    return redirect(url_for('usuarios_Ver'))


#crud administradores

@app.route('/usuarios2')
def admin_Crear():
    return render_template('registro2.html')

@app.route('/admin/agregar', methods=['POST'])
def admin_Agregar():
    if request.method == 'POST':
        Nombre=request.form['Nombre']
        ap=request.form['email']
        am=request.form['pass']
        
        cur=db.connection.cursor()
        
        pwd=genph(am)
        
        sql="INSERT INTO admin (nombre, email, contrasena) VALUES (%s, %s, %s)"
        valores=(Nombre, ap, pwd,)
        cur.execute(sql,valores)
        db.connection.commit()

        flash('¡Usuario agregada exitosamente!')

        return redirect(url_for('admin')) 

#CRUD Comentarios 
#crear


@app.route('/comentarios/agregar', methods=['POST'])
def comentario_Agregar():
    if request.method == 'POST':
        Nombre=request.form['Nombre']
        comentario=request.form['comentario']
        correo=request.form['correo']
        cur=db.connection.cursor()
        sql="INSERT INTO comentarios (nombre, comentario, correo) VALUES (%s, %s, %s)"
        valores=(Nombre, comentario, correo)
        cur.execute(sql,valores)
        db.connection.commit()

        flash('¡comentario agregado exitosamente!')

        return redirect(url_for('index'))



#leer
@app.route('/coment')
def comentarios_Ver():
    cur=db.connection.cursor()
    sql="SELECT * FROM comentarios ORDER BY id desc"
    cur.execute(sql)
    productos=cur.fetchall()
    print(productos) 
    return render_template('comentarios.html', productos=productos)

@app.route('/comentario/<string:id>')
def ver_comentarios(id):
    print(id)
    cur=db.connection.cursor()
    sql="SELECT * FROM comentarios WHERE id={0}".format(id)
    cur.execute(sql)
    producto=cur.fetchall()
    print(producto[0])
    return render_template('comentarioVer.html', producto=producto[0])


#Update (Actualizar)
@app.route('/comentario/editar/<string:id>')
def editar_comentario(id):
    print(id)
    cur=db.connection.cursor()
    sql="SELECT * FROM comentarios WHERE id={0}".format(id)
    cur.execute(sql)
    producto=cur.fetchall()
    print(producto[0])
    return render_template('alumnoEditar.html', producto=producto[0])

@app.route('/comentario/actualizar/<string:id>', methods=['POST'])
def comentario_actualizar(id):
    if request.method == 'POST':
        Nombre=request.form['Nombre']
        comentario=request.form['comentario']
        correo=request.form['correo']

        cur=db.connection.cursor()
        sql="UPDATE comentarios SET nombre=%s, comentario=%s, correo=%s, WHERE id=%s"        
        valores=(Nombre, comentario, correo, id)
        cur.execute(sql,valores)
        db.connection.commit()
        cur.close()
        flash('¡comentario modificado exitosamente!')
    return redirect(url_for('comentarios_Ver'))


#Delete (Borrar)
@app.route('/comentario/eliminar/<string:id>')
def eliminar_comentario(id):
    print(id)
    cur=db.connection.cursor()
    sql="DELETE FROM comentarios WHERE id={0}".format(id)
    cur.execute(sql)
    db.connection.commit()
    flash('¡comentario eliminado correctamente!')
    return redirect(url_for('comentario_Ver'))



# Apartado Login

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/loguear', methods=['POST'])
def loguear():
    if request.method == 'POST':
        Username=request.form['Username']
        Password=request.form['Password']
        user=User(0,Username,Password)
        loged_user=ModuleUser.login(db,user)
        
        if loged_user!= None:
            if loged_user.contrasena:
                login_user(loged_user)
                return redirect(url_for('index'))
            else:
                flash('Nombre de usuario y/o Contraseña incorrecta.')
                return render_template('login.html')
        else:
            flash('Nombre de usuario y/o Contraseña incorrecta.')
            return render_template('login.html')
    else:
            flash('Nombre de usuario y/o Contraseña incorrecta.')
            return render_template('login.html')


# Apartado Login administrador

@app.route('/login2')
def login2():
    return render_template('login2.html')

@app.route('/loguearse', methods=['POST'])
def loguearse():
    if request.method == 'POST':
        Username=request.form['Username']
        Password=request.form['Password']
        user=User(0,Username,Password)
        loged_user=ModuleUser.login(db,user)
        
        if loged_user!= None:
            if loged_user.contrasena:
                login_user(loged_user)
                return redirect(url_for('admin'))
            else:
                flash('Nombre de usuario y/o Contraseña incorrecta.')
                return render_template('login.html')
        else:
            flash('Nombre de usuario y/o Contraseña incorrecta.')
            return render_template('login.html')
    else:
            flash('Nombre de usuario y/o Contraseña incorrecta.')
            return render_template('login.html')

if __name__=='__main__':
    csrf.init_app(app)
    app.run(debug=True)
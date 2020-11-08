from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy 

#SQLite conexión
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' #Locación de la base de datos
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #Quitar WARNING
db = SQLAlchemy(app)

#Configuraciones
app.secret_key = "mysecretkey"

#Modelo de la Base de Datos
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    email = db.Column(db.String)

    def __repr__(self):
        return "<Contact %r" % self.id


@app.route('/', methods=['GET'])
def index():
    #Obtenemos y ordenamos los datos de los contactos para mostrarlos
    if request.method == 'GET':
        contacts = Contact.query.order_by(Contact.fullname).all()
        return render_template('index.html', contacts=contacts)

@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        #Sacamos la info del form"
        fullname = request.form['fullname'] # Ej: Sacamos la info del form en index.html con name="fullname"
        phone = request.form['phone']
        email = request.form['email']
        #Creamos el nuevo contacto
        new_contact = Contact(fullname=fullname,phone=phone,email=email)
        
        #Agregamos el nuevo contacto a la BD
        try:
            db.session.add(new_contact)
            db.session.commit()
            flash("Contact successfully added")
            return redirect('/')
        except:
            return "Something went wrong adding the new contact :( "

@app.route('/edit/<int:id>', methods=['POST', 'GET'])
def edit(id):
    contact_to_edit = Contact.query.get_or_404(id) #Obtenemos el contacto por medio del id

    if request.method == 'POST':
        #Actualizamos los datos a los nuevo datos
        contact_to_edit.fullname = request.form['fullname']
        contact_to_edit.phone = request.form['phone']
        contact_to_edit.email = request.form['email']
        #Persistimos los nuevo datos en la base de datos
        try:
            db.session.commit()
            flash("Contact edited sucessfully")
            return redirect('/')
        except:
            return "Something went wrong editing the contact :("
    else:
        #Rendereizamos el template y recibe los datos del contacto a editar 
        return render_template('edit.html', contact_to_edit=contact_to_edit)


@app.route('/delete/<int:id>')
def delete(id):
    contact_to_delete = Contact.query.get_or_404(id) #Obtenemos al contacto por medio del id
    #Eliminamos el contacto
    try:
        db.session.delete(contact_to_delete)
        db.session.commit()
        flash("Contact deleted successfully")
        return redirect('/')
    except:
        return "Something went wrong deleting the contact :("


if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask ,jsonify ,request
# del modulo flask importar la clase Flask y los métodos jsonify,request
from flask_cors import CORS       # del modulo flask_cors importar CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
app=Flask(__name__)  # crear el objeto app de la clase Flask
CORS(app) #modulo cors es para que me permita acceder desde el frontend al backend


# configuro la base de datos, con el nombre el usuario y la clave
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://mauriciom_824:Bianca#824Irina@localhost/proyecto_back'
# URI de la BBDD                          driver de la BD  user:clave@URLBBDD/nombreBBDD
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False #none
db= SQLAlchemy(app)   #crea el objeto db de la clase SQLAlquemy
ma=Marshmallow(app)   #crea el objeto ma de de la clase Marshmallow


#—---


# defino las tablas
class Libro(db.Model):   # la clase Libro hereda de db.Model de SQLAlquemy   
    id=db.Column(db.Integer, primary_key=True)   #define los campos de la tabla
    nombre=db.Column(db.String(100))
    autor=db.Column(db.String(100))
    genero=db.Column(db.String(100))
    prestados=db.Column(db.Integer)
    stock=db.Column(db.Integer)
    imagen=db.Column(db.String(400))
    
    def __init__(self,nombre,autor,genero,prestados,stock,imagen): #crea el  constructor de la clase
        self.nombre=nombre # no hace falta el id porque lo crea sola mysql por ser auto_incremento
        self.autor=autor
        self.genero=genero
        self.prestados=prestados
        self.stock=stock
        self.imagen=imagen




    #  si hay que crear mas tablas , se hace aqui

class Login(db.Model):   # la clase Usuario hereda de db.Model de SQLAlquemy   
    email=db.Column(db.String(30), primary_key=True)   #define los campos de la tabla
    password=db.Column(db.String(12))
    isAdmin=db.Column(db.Integer)
    
    
    def __init__(self,email,password,isAdmin): #crea el  constructor de la clase
        self.email=email # no hace falta el id porque lo crea sola mysql por ser auto_incremento
        self.password=password
        self.isAdmin=isAdmin



with app.app_context():
    db.create_all()  # aqui crea todas las tablas si es que no estan creadas
#  ************************************************************






class LibroSchema(ma.Schema):
    class Meta:
        fields=('id','nombre','autor','genero''prestados''stock','imagen')


libro_schema=LibroSchema()  # El objeto libro_schema es para traer un libro
libros_schema=LibroSchema(many=True)  # El objeto libros_schema es para traer multiples registros de libro

class LoginSchema(ma.Schema):
    class Meta:
        fields=('email','password','isAdmin')


login_schema=LoginSchema()  # El objeto login_schema es para traer un usuario
logins_schema=LoginSchema(many=True)  # El objeto logins_schema es para traer multiples registros de usuario



# crea los endpoint o rutas (json)
@app.route('/libros',methods=['GET'])
def get_Libros():
    all_libros=Libro.query.all() # el metodo query.all() lo hereda de db.Model
    result=libros_schema.dump(all_libros)  #el metodo dump() lo hereda de ma.schema y
                                                 # trae todos los registros de la tabla
    return jsonify(result)     # retorna un JSON de todos los registros de la tabla

@app.route('/logins',methods=['GET'])
def get_Logins():
    all_logins=Login.query.all() # el metodo query.all() lo hereda de db.Model
    result=logins_schema.dump(all_logins)  #el metodo dump() lo hereda de ma.schema y
                                                 # trae todos los registros de la tabla
    return jsonify(result)     # retorna un JSON de todos los registros de la tabla




@app.route('/libros/<id>',methods=['GET'])
def get_libro(id):
    libro=Libro.query.get(id)
    return libro_schema.jsonify(libro)   # retorna el JSON de un libro recibido como parametro

@app.route('/logins/<email>',methods=['GET'])
def get_login(email):
    login=Login.query.get(email)
    return login_schema.jsonify(login)   # retorna el JSON de un login recibido como parametro


@app.route('/libros/<id>',methods=['DELETE'])
def delete_libro(id):
    libro=Libro.query.get(id)
    db.session.delete(libro)
    db.session.commit()                     # confirma el delete
    return libro_schema.jsonify(libro) # me devuelve un json con el registro eliminado

@app.route('/logins/<email>',methods=['DELETE'])
def delete_login(email):
    login=Login.query.get(email)
    db.session.delete(login)
    db.session.commit()                     # confirma el delete
    return login_schema.jsonify(login) # me devuelve un json con el registro eliminado


@app.route('/libros', methods=['POST']) # crea ruta o endpoint
def create_libro():
    #print(request.json)  # request.json contiene el json que envio el cliente
    nombre=request.json['nombre']
    autor=request.json['autor']
    genero=request.json['genero']
    prestados=request.json['prestados']
    stock=request.json['stock']
    imagen=request.json['imagen']
    new_libro=Libro(nombre,autor,genero,prestados,stock,imagen)
    db.session.add(new_libro)
    db.session.commit() # confirma el alta
    return libro_schema.jsonify(new_libro)

@app.route('/logins', methods=['POST']) # crea ruta o endpoint
def create_login():
    #print(request.json)  # request.json contiene el json que envio el cliente
    email=request.json['email']
    password=request.json['password']
    isAdmin=request.json['isAdmin']
    new_login=Login(email,password,isAdmin)
    db.session.add(new_login)
    db.session.commit() # confirma el alta
    return login_schema.jsonify(new_login)


@app.route('/libros/<id>' ,methods=['PUT'])
def update_libro(id):
    libro=Libro.query.get(id)
 
    libro.nombre=request.json['nombre']
    libro.autor=request.json['autor']
    libro.genero=request.json['genero']
    libro.prestamos=request.json['prestamos']
    libro.stock=request.json['stock']
    libro.imagen=request.json['imagen']


    db.session.commit()    # confirma el cambio
    return libro_schema.jsonify(libro)    # y retorna un json con el libro

@app.route('/logins/<email>' ,methods=['PUT'])
def update_login(email):
    login=Login.query.get(email)
 
    login.email=request.json['email']
    login.password=request.json['password']
    login.isAdmin=request.json['isAdmin']


    db.session.commit()    # confirma el cambio
    return login_schema.jsonify(login)    # y retorna un json con el usuario


@app.route('/')
def bienvenida():
    return "Bienvenidos al backend"   # retorna el JSON de un usuario recibido como parametro


# programa principal *******************************
if __name__=='__main__':  
    app.run(debug=True, port=5000)   # ejecuta el servidor Flask en el puerto 5000
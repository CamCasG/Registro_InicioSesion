from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
from flask_bcrypt import Bcrypt
from datetime import date, datetime       



EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
REGEX_PASSWORD = re.compile(r"^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])[a-zA-Z\d]{7,16}$")  #contraseña debe contener mayúsculas, minúsculas y números, y un mínimo de 7 caracteres
NAME_REGEX = re.compile(r'^([A-Za-z\D]){3,}$')   #solo debe contener letras y un mínimo de 3 caracteres

class Usuario:
    def __init__(self,data):
        self.id = data['id']
        self.nombre = data['nombre']
        self.apellido = data['apellido']
        self.email = data['email']
        self.password = data['password']
        self.nacimiento = data['nacimiento']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM sesiones;"
        resultado =  connectToMySQL('esquema_sesiones').query_db(query)
        sesiones = []
        for x in resultado:
            sesiones.append(cls(x))
        return sesiones

    @classmethod
    def save(cls,data):
        query = "INSERT INTO sesiones (nombre, apellido, email, password, nacimiento) VALUES (%(nombre)s,%(apellido)s,%(email)s,%(password)s,%(nacimiento)s);"
        resultado = connectToMySQL('esquema_sesiones').query_db(query,data)
        print(resultado)
        return resultado

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM sesiones WHERE email = %(email)s;"
        result = connectToMySQL("esquema_sesiones").query_db(query,data)
        # no se encontró un usuario coincidente
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM sesiones WHERE id = %(id)s;"
        results = connectToMySQL("esquema_sesiones").query_db(query,data)
        return cls(results[0])

    @staticmethod
    def validar_usuario(usuario):
        today = date.today() 
        #age = today.year - Birthday.year - ((Birthday.month, today.day) <  (Birthday.month, today.day))
        is_valid = True
        query = "SELECT * FROM sesiones WHERE email = %(email)s;"
        resultado = connectToMySQL('esquema_sesiones').query_db(query,usuario)
        hoy = today.strftime("%Y-%m-%d")
        edad = datetime.strptime(hoy,'%Y-%m-%d').date()
        print(hoy)
        # cumpleanos = datetime.strftime(usuario['nacimiento'],"%Y/%m/%d")
        # print(cumpleanos)
        nacimiento = usuario['nacimiento']
        cumpleanos = datetime.strptime(nacimiento,'%Y-%m-%d').date()
        print(cumpleanos)

        if len(resultado) >= 1:
            is_valid = False
            flash("Este correo ya existe en nuestra BD", "registro")
        if not NAME_REGEX.match(usuario['nombre']):
            is_valid = False
            flash("El nombre debe tener por lo menos 3 caracteres y no contener números","registro")
        if not NAME_REGEX.match(usuario['apellido']):
            is_valid = False
            flash("El apellido debe tener por lo menos 3 caracteres y no contener números","registro")
        if not EMAIL_REGEX.match(usuario['email']):
            is_valid = False
            flash("Correo electrónico inválido, volver a intentar.","registro")
        if not REGEX_PASSWORD.match(usuario['password']):
            is_valid = False
            flash("Tu contraseña debe contener mayúsculas, minúsculas, números y un mínimo de 7 caracteres","registro")
        if usuario['password'] != usuario['confirmar']:
            is_valid = False
            flash("¡Las contraseñas no coinciden!","registro")
        if edad.year - cumpleanos.year - ((cumpleanos.month, edad.day) <  (cumpleanos.month, edad.day)) < 14:
            is_valid = False
            flash("No tienes la edad suficiente para registrarte", "registro")

        return is_valid






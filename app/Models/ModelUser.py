from .entities.user import User

class ModuleUser():
    @classmethod
    def login(self, db, user):
        try:
            cur=db.connection.cursor()
            sql="SELECT id, email, contrasena FROM clientes WHERE email='{}'".format(user.email)
            cur.execute(sql)
            row=cur.fetchone()
            if row != None:
                user=User(row[0],row[1],user.check_password(row[2],user.contrasena))
                return user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_by_id(self, db, id):
        try:
            cur=db.connection.cursor()
            sql="SELECT id, email FROM clientes WHERE id='{}'".format(id)
            cur.execute(sql)
            row=cur.fetchone()
            if row != None:
                return User(row[0], row[1], None)
            else:
                return None
        except Exception as ex:
            raise Exception(ex)



#administradores

class ModuleUser():
    @classmethod
    def login(self, db, user):
        try:
            cur=db.connection.cursor()
            sql="SELECT id, email, contrasena FROM admin WHERE email='{}'".format(user.email)
            cur.execute(sql)
            row=cur.fetchone()
            if row != None:
                user=User(row[0],row[1],user.check_password(row[2],user.contrasena))
                return user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_by_id(self, db, id):
        try:
            cur=db.connection.cursor()
            sql="SELECT id, email FROM admin WHERE id='{}'".format(id)
            cur.execute(sql)
            row=cur.fetchone()
            if row != None:
                return User(row[0], row[1], None)
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
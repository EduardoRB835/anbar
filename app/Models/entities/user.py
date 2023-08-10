from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin

class User(UserMixin):

    def get_id(self):
        return(self.id)

    def __init__(self,id,email, contrasena) -> None:
        self.id=id
        self.email=email
        self.contrasena=contrasena

    @classmethod
    def check_password(self, hashed_password, contrasena):
        return check_password_hash(hashed_password, contrasena)

#print(generate_password_hash("1234"))
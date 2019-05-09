from models.base_model import BaseModel
import peewee as pw
import re
from flask_login import UserMixin

class User(BaseModel, UserMixin):
    username = pw.CharField(unique=True, null=False)
    email = pw.CharField(unique=True, null=False)
    password = pw.CharField(null=False)
    profile_picture = pw.CharField(null=True, default=None)

    def validate(self):
        duplicate_user = User.get_or_none(
            User.username == self.username
            )

        if duplicate_user:
            self.errors.append('Name taken')

        duplicate_email = User.get_or_none(User.email == self.email)

        if duplicate_email:
            self.errors.append('An account with that email already exists')

    @classmethod
    def validate_password(self, password):
        valid_password = True
        while valid_password:
            if (len(password) < 6 or len(password) > 12):
                break
            # elif not re.search("[a-z]", password):
            #     break
            # elif not re.search("[0-9]", password):
            #     break
            # elif not re.search("[A-Z]", password):
            #     break
            # elif not re.search("[$#@]", password):
            #     break
            else:
                valid_password = False
                break

        return not valid_password
    
# class Images(BaseModel):
#     user = pw.ForeignKeyField(User, backref='images')
#     URL = pw.CharField(null=False)
#     caption = pw.CharField(null=True, default=None)
#     likes = pw.IntegerField(default=0)
#     donation = pw.IntegerField(default=0)
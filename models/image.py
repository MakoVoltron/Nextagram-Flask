from models.base_model import BaseModel
from models.user import User
import peewee as pw


class Image(BaseModel):
    user = pw.ForeignKeyField(User, backref='images')
    URL = pw.CharField(null=False)
    caption = pw.CharField(null=True, default=None)
    likes = pw.IntegerField(default=0)
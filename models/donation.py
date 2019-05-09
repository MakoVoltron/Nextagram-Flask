from models.base_model import BaseModel
from models.user import User
import peewee as pw


class Donation(BaseModel):
    image = pw.ForeignKeyField(User, backref='donation')
    donor = pw.CharField(null=False)
    donation_amount = pw.IntegerField(default=0)

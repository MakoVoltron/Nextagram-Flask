from models.base_model import BaseModel
from models.image import Image
from models.user import User
import peewee as pw


class Donation(BaseModel):
    image = pw.ForeignKeyField(Image, backref='donations')
    donor = pw.ForeignKeyField(User, backref='donations')
    donation_amount = pw.DecimalField(default=0, decimal_places=2)

import peewee as pw 
from models.base_model import BaseModel
from models.user import User
from playhouse.hybrid import hybrid_property

class FollowerFollowing(BaseModel):
    fan = pw.ForeignKeyField(User, backref='idols')
    idol = pw.ForeignKeyField(User, backref='fans')
    approved = pw.BooleanField(default=False)

    # Checks for unique relationship between Follower-Followed (you can follow a person only once)
    class Meta:
        indexes = (
            (('fan', 'idol'), True),
        )

    @hybrid_property
    def is_approved(self):
        return True if self.approved else False
from board import *
from marshmallow_sqlalchemy import field_for

# Using marshmallow-sqlalchemy will make your life a lot easier
#   Do some research into this!!
class BoardSchema(ModelSchema):
  class Meta(ModelSchema.Meta):
    model = Board

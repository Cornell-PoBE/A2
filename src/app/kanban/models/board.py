from . import *

class Board(Base):
  __tablename__ = 'boards'
  id             = db.Column(db.Integer, primary_key=True)
  title          = db.Column(db.String(256), unique=True, nullable=False)

  def __init__(self, **kwargs):
    """
    Constructor
    """
    self.title = kwargs.get('title', None)

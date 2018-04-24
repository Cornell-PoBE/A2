from app.constants import *
from . import *

"""
Add more methods below!!!
"""

def board_by_id(board_id):
  """
  Get board by ID
  """
  return Board.query.filter_by(id=board_id).first()

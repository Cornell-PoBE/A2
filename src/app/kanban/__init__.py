from flask import Blueprint
from app import *

# Kanban Blueprint
kanban = Blueprint('kanban', __name__, url_prefix='/kanban')

# Import all endpoints
from controllers.boards_controller import *

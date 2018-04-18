from flask import Blueprint

fiction = Blueprint(name='fiction', import_name=__name__)

from . import views

from flask import Blueprint
from project.controllers.index import index_page

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    return index_page()
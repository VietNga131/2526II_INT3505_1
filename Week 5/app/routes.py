from flask import Blueprint, jsonify, request
from .models import Book, db

main_bp = Blueprint('main', __name__)

from flask import Blueprint

bp = Blueprint('api', __name__)

from app.api import auth, usuarios, pacientes, sessoes, relatorios, qr, ia

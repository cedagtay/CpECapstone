from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from facerecogweb import db

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/', methods=['GET'])
def dashboard():
    return render_template('admin/index.html')

@bp.route('/subject', methods=['GET', 'POST'])
def subject():
    return render_template('admin/subject.html')


@bp.route('/schedule', methods=['GET', 'POST'])
def schedule():
    return render_template('admin/schedule')

@bp.route('/reports', methods=['GET', 'POST'])
def reports():
    return render_template('admin/report.html'):

from flask import render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.notifications.models import Notification
from app.notifications import bp
from app.users.models import User



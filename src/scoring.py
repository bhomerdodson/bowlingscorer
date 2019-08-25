import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from src.db import get_db

bp = Blueprint('scoring', __name__, url_prefix='/scoring')
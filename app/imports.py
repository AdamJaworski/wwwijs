from flask import Flask, request, jsonify, render_template, url_for, redirect, flash, make_response
from flask_jwt_extended import (JWTManager, create_access_token, get_jwt_identity, set_access_cookies,
                                unset_jwt_cookies, verify_jwt_in_request, create_refresh_token, set_refresh_cookies,
                                jwt_required)
from werkzeug.security import generate_password_hash, check_password_hash
import managers.database as database
from sqlite3 import IntegrityError
from functools import wraps
from data_struct.task import id_list, table_list

from flask import Blueprint, render_template


def jwt_required_redirect(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
        except Exception:
            return redirect(url_for('get.login'))
        return fn(*args, **kwargs)
    return wrapper


def jwt_required_redirect_json(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
        except Exception:
            return jsonify({'status': False, 'redirect': url_for('get.login')})
        return fn(*args, **kwargs)
    return wrapper

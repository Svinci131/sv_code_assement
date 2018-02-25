# app.py

import boto3
from botocore.exceptions import ClientError
import decimal, simplejson
import hashlib
import logging
import os
import simplejson as json
import time
import uuid


from flask import Flask, jsonify, request, redirect

app = Flask(__name__)

USER_TABLE = os.environ['USER_TABLE']
dynamodb = boto3.resource('dynamodb')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

table = dynamodb.Table(os.environ['USER_TABLE'])


@app.route("/")
def hello():
    return "Welcome!"

@app.route("/ping")
def ping():
    return "pong"

@app.route("/users", methods=["POST"])
def create_user():
    """
        Creates a new user with a unique email address.
    """
    try:
        payload = _validatePayload(request)
        timestamp = int(time.time() * 1000)

        user = {
            'name': payload.get('name'),
            'email': payload.get('email'),
            'password': _encodePassword(payload.get('password')),
            'createdAt': timestamp,
            'updatedAt': timestamp,
        }

        resp = table.put_item(
            Item=user,
            Expected={'email':{'Exists': False}}
        )

        return jsonify(user), 200
    except BaseException as e:
        return _customizeErrorMessage(e) 

def _validatePayload(request):
    """
        Check that all expected fields are in payload and
        have valid values.

        :type request: dict
        :rtype: dict
    """
    return {
        'name': _validateField(request, 'name'),
        'email': _validateField(request, 'email'),
        'password': _validateField(request, 'password'),
    }


def _validateField(request, field):
    """
        Check that all field is a string
        with one or more characters.

        :type request: dict
        :type field: string
        :rtype: string
    """
    val = request.json.get(field, '')

    if (type(val) is not str or len(val) < 1):
        raise Exception('Invalid {}'.format(field))
    else:
        return val

def _encodePassword(password):
    stringifyPW = str.encode(password)
    return hashlib.sha224(stringifyPW).hexdigest()

def _customizeErrorMessage(e):
    err = str(e)

    logger.info('ERROR', err)

    if (e.response['Error']['Code'] == "ConditionalCheckFailedException"):
        err = "User already exists"

    return jsonify({'error': err }), 400


@app.route("/users", methods=["GET"])
def list():
    """
     This route is here to make testing user
     creatation easier.

     Since, it's a demo project we assume
     every user is an admin.
    """
    try:
        data = table.scan()
        users = data.get('Items', None)
        if users is None:
            return jsonify({'error': 'Error fetching users'}), 400

        resp = {
            'count': len(users),
            'users': users
        }
        return jsonify(resp)
    except BaseException as e:
        logger.info('ERROR', str(e))
        return jsonify({'error': str(e)}), 400
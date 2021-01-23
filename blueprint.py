from flask import Flask, jsonify,request
from jsonschema import validate,exceptions
from functools import wraps

from time import time
import requests
import json

from app.controller.blockchain import Blockchain

from app.schemas.schemas import *
from uuid import uuid4

app = Flask(__name__)

blockchain = Blockchain()
node_identifier = str(uuid4()).replace('-', '')

def logger_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except exceptions.ValidationError as ve:
            return jsonify({'Desc': 'Invalid json data'}),400
        except ValueError as e:
            return jsonify({'Desc': 'Invalid URL'}), 400            
        except Exception as e:
            return jsonify({'Desc': 'There was an error'}), 500
    return wrapper

@app.route('/chain/mine', methods=['PUT'])
@logger_decorator
def mine():
    if(blockchain.get_pending_transactions()):
        last_block = blockchain.last_block
        proof = blockchain.proof_of_work(last_block)
        previous_hash = blockchain.hash(last_block)
        
        block = blockchain.new_block(proof, previous_hash)

        response = {
            'message': "New Block Forged",
            'index': block['index'],
            'transactions': block['transactions'],
            'proof': block['proof'],
            'previous_hash': block['previous_hash'],
        }
        return jsonify({'Data': response}), 200
    else:
        return jsonify({'Desc': "There are no transactions"}), 200
    

@app.route('/transaction', methods=['POST'])
@logger_decorator
def new_transaction():
    values = request.get_json()
    validate(values, transaction_schema)
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

    return jsonify({'Desc': 'Transaction will be added to Block {0}'.format(index)}),200

@app.route('/transactions', methods=['GET'])
@logger_decorator
def get_pending_transactions():
    response = blockchain.get_pending_transactions()

    return jsonify({'Data': response}),200

@app.route('/chain', methods=['GET'])
@logger_decorator
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify({'Data': response}), 200

@app.route('/nodes/register', methods=['POST'])
@logger_decorator
def register_nodes():
    values = request.get_json()
    validate(values, nodes_schema)
    nodes = values.get('nodes')
    if len(nodes) == 0:
        return jsonify({'Desc': 'The list cannot be empty'}),400

    for node in nodes:         
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify({'Data': response}), 200

@app.route('/nodes/resolve', methods=['PUT'])
@logger_decorator
def consensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }

    return jsonify({'Desc': response}), 200



from flask import Flask, jsonify,request
from jsonschema import validate,exceptions
from functools import wraps

import time
import requests
import json

from app.controller.blockchain import Blockchain, Block
from app.resources.blockchain import *
from app.schemas.schemas import *

app = Flask(__name__)

blockchain = Blockchain()
blockchain.create_genesis_block()

peers = set()

def logger_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except exceptions.ValidationError as ve:
            return jsonify({'Desc': 'Invalid json data'}),400
        except Exception as e:
            return jsonify({'Desc': 'There was an error'}), 500
    return wrapper

#Submit a new transaction. 
@app.route('/new_transaction', methods=['POST'])
@logger_decorator
def new_transaction():
    tx_data = request.get_json()
    validate(tx_data, transaction_schema)

    tx_data["timestamp"] = time.time()
    blockchain.add_new_transaction(tx_data)

    return "Success", 201

#Return the node's copy of the chain.
@app.route('/chain', methods=['GET'])
def get_chain():
    chain_data = []
    for block in blockchain.chain:
        chain_data.append(block.__dict__)
    return json.dumps({"length": len(chain_data),
                       "chain": chain_data,
                       "peers": list(peers)})

#Request the node to mine the unconfirmed transactions
@app.route('/mine', methods=['GET'])
def mine_unconfirmed_transactions():
    result = blockchain.mine()
    if not result:
        return jsonify({'Desc': 'No transactions to mine'}), 404
    else:
        # Making sure we have the longest chain before announcing to the network
        chain_length = len(blockchain.chain)
        consensus(blockchain,peers)
        if chain_length == len(blockchain.chain):
            announce_new_block(blockchain.last_block,peers)
        return jsonify({'Desc': "Block #{} is mined.".format(blockchain.last_block.index)}), 200

#Add new peers to the network. [BETA]
@app.route('/register_node', methods=['POST'])
def register_new_peers():
    node_address = request.get_json()["node_address"]
    if not node_address:
        return jsonify({'Desc': 'Invalid json data'}),400

    peers.add(node_address)
    return get_chain()

#Register new peers to the network. [BETA]
@app.route('/register_with', methods=['POST'])
def register_with_existing_node():
    node_address = request.get_json()["node_address"]
    if not node_address:
        return jsonify({'Desc': 'Invalid json data'}),400

    data = {"node_address": request.host_url}
    headers = {'Content-Type': "application/json"}

    response = requests.post(node_address + "/register_node",
                             data=json.dumps(data), headers=headers)

    if response.status_code == 200:
        global blockchain
        global peers

        chain_dump = response.json()['chain']
        blockchain = create_chain_from_dump(chain_dump)
        peers.update(response.json()['peers'])
        return jsonify({'Desc': "Registration successful"}), 200
    else:
        return jsonify({'Desc': response.content}), response.status_code        

#Add a block mined by someone else to the node's chain.
@app.route('/add_block', methods=['POST'])
def verify_and_add_block():
    block_data = request.get_json()
    block = Block(block_data["index"],
                  block_data["transactions"],
                  block_data["timestamp"],
                  block_data["previous_hash"],
                  block_data["nonce"])

    proof = block_data['hash']
    added = blockchain.add_block(block, proof)

    if not added:
        return jsonify({'Desc': 'The block was discarded by the node'}), 500

    return jsonify({'Desc': 'Block added to the chain'}), 201

#See unconfirmed transactions
@app.route('/pending_tx')
def get_pending_tx():
    return jsonify({'Data': blockchain.unconfirmed_transactions})
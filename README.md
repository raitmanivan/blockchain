# Blockchain Proyect

#### Ivan Raitman

## Instructions to run

Clone the project,

```sh
$ git clone ...
```

Install the dependencies,

```sh
$ pip install -r requirements.txt
```

Start a blockchain node server,

```sh
$ export FLASK_APP=blueprint.py
$ flask run --port 8000
```

One instance of our blockchain node is now up and running at port 8000.

The application should be up and running at [http://localhost:8000](http://localhost:8000).

To play around by spinning off multiple custom nodes, use the `register_with/` endpoint to register a new node. 

If you want to add more nodes to this network:

```sh
$ export FLASK_APP=blueprint.py
$ flask run --port 8001
```

Now a new application should be up and running at [http://localhost:8001](http://localhost:8001).

## Endpoints

* [Get chain](#get-chain)
* [Mine](#mine)

* [Get transactions](#get-transactions)
* [New transaction](#new-transaction)

* [New node](#new-node)
* [Consensus](#consensus)

## Get chain
  A json list with the blockchain.

* **URL**

  /chain

* **Method:**

  `GET`

* **Success Response:**

    **Code:** 200 <br />
    **Content:**
```
          {
            "Data": {
              "chain": [
                {
                  "index": 1,
                  "previous_hash": "1",
                  "proof": 100,
                  "timestamp": 1611431289.167938,
                  "transactions": []
                }
              ],
              "length": 1
            }
          }
```
* **Error Response:**

  * **Code:** 500 INTERNAL SERVER ERROR <br />
    **Content:** `{ "Desc" : "There was an error" }`

* **Sample Call:**

  ```
    curl 'http://localhost:8000/chain'
  ```

## Mine
  Mine the chain
* **URL**

  /chain/mine

* **Method:**

  `PUT`

* **Success Response:**

    **Code:** 200 <br />
    **Content:**
    ```
        {
          "Data": {
            "index": 2,
            "message": "New Block Forged",
            "previous_hash": "dcd3e7d639a7dd671ca08ac87667763567819f16e9a4f9ef7f451eac3eb80375",
            "proof": 65898,
            "transactions": [
              {
                "amount": "100000",
                "recipient": "ivanokey",
                "sender": "ivan"
              }
            ]
          }
        }
    ```

    **Code:** 200 <br />
    **Content:**
    ```
      {
        "Desc": "There are no transactions"
      }
    ```

* **Error Response:**

  * **Code:** 500 INTERNAL SERVER ERROR <br />
    **Content:** `{ "Desc" : "There was an error" }`

* **Sample Call:**

  ```
  curl -XPUT 'http://localhost:8000/chain/mine'
  ```

## Get transactions
  A json list with all pending transactions.

* **URL**

  /transactions

* **Method:**

  `GET`

* **Success Response:**

    **Code:** 200 <br />
    **Content:**
```
      {
        "Data": [
          {
            "amount": "100000",
            "recipient": "ivanokey",
            "sender": "ivan"
          }
        ]
      }
```
* **Error Response:**

  * **Code:** 500 INTERNAL SERVER ERROR <br />
    **Content:** `{ "Desc" : "There was an error" }`

* **Sample Call:**

  ```
    curl 'http://localhost:8000/transactions'
  ```

## New transaction
  Create a new transaction to add to a block.
* **URL**

  /transaction

* **Method:**

  `POST`

* **Data Params**

 ```
	{
		"sender": "ivan",
		"recipient": "ivanokey",
		"amount": "100000"
	}
```

* **Success Response:**

    **Code:** 200 <br />
    **Content:**
    ```
      {
        "Desc": "Transaction will be added to Block 3"
      }
    ```

* **Error Response:**

  * **Code:** 400 BAD REQUEST <br />
    **Content:** `{ "Desc" : "Invalid json data" }`
  * **Code:** 500 INTERNAL SERVER ERROR <br />
    **Content:** `{ "Desc" : "There was an error" }`

* **Sample Call:**
 ```
  curl -XPOST -H "Content-type: application/json" -d '{
	"sender": "ivan",
	"recipient": "ivanokey",
	"amount": "100000"
}' 'http://localhost:8000/transaction'
  ```

## New node
  Create a new node to add to the blockchain.
* **URL**

  /nodes/register

* **Method:**

  `POST`

* **Data Params**

  ```
    {
      "nodes": [
        "http://127.0.0.1:8001"
      ]
    }
  ```

* **Success Response:**

    **Code:** 200 <br />
    **Content:**
    ```
        {
          "Data": {
            "message": "New nodes have been added",
            "total_nodes": [
              "127.0.0.1:8001"
            ]
          }
        }
    ```

* **Error Response:**

  * **Code:** 400 BAD REQUEST <br />
    **Content:** `{ "Desc" : "Invalid json data" }`
  * **Code:** 400 BAD REQUEST <br />
    **Content:** `{ "Desc" : "The list cannot be empty" }`  
  * **Code:** 400 BAD REQUEST <br />
    **Content:** `{ "Desc" : "Invalid URL" }`        
  * **Code:** 500 INTERNAL SERVER ERROR <br />
    **Content:** `{ "Desc" : "There was an error" }`

* **Sample Call:**

  ```
  curl -XPOST -H "Content-type: application/json" -d '{
      "nodes": [
        "http://127.0.0.1:8001"
      ]
    }' 'http://localhost:8000/nodes/register'
  ```

## Consensus
  Solve the problem of a long chain when there are multiple nodes.
* **URL**

  /nodes/resolve

* **Method:**

  `PUT`

* **Success Response:**

    **Code:** 200 <br />
    **Content:**
    ```
      {
        "Desc": {
          "chain": [
            {
              "index": 1,
              "previous_hash": "1",
              "proof": 100,
              "timestamp": 1611432411.3887239,
              "transactions": []
            }
          ],
          "message": "Our chain is authoritative"
        }
      }
    ```

    **Code:** 200 <br />
    **Content:**
    ```
      {
        "Desc": {
          "chain": [
            {
              "index": 1,
              "previous_hash": "1",
              "proof": 100,
              "timestamp": 1611432411.3887239,
              "transactions": []
            }
          ],
          "message": "Our chain was replaced"
        }
      }
    ```

* **Error Response:**

  * **Code:** 500 INTERNAL SERVER ERROR <br />
    **Content:** `{ "Desc" : "There was an error" }`

* **Sample Call:**

  ```
  curl -XPUT 'http://localhost:8000/nodes/resolve'
  ```







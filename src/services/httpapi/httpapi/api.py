from flask import Flask, request
from flasgger import Swagger, swag_from
from nameko.standalone.rpc import ClusterRpcProxy

app = Flask(__name__)
Swagger(app)
CONFIG = {'AMQP_URI': "amqp://guest:guest@localhost"}


@app.route('/player', methods=['POST'])
@swag_from('player.yml')
def player():
    operation = request.json.get('operation')
    value = request.json.get('value')
    other = request.json.get('other')
    email = request.json.get('email')
    msg = "Please wait the calculation, you'll receive an email with results"
    subject = "API Notification"
    with ClusterRpcProxy(CONFIG) as rpc:
        # asynchronously spawning and email notification
        rpc.mail.send.async(email, subject, msg)
        # asynchronously spawning the player task
        result = rpc.player.create.async(operation, value, other, email)
        return msg, 200


class Player(Resource):
    def get(self, name):
       """
       This examples uses FlaskRESTful Resource
       It works also with swag_from, schemas and spec_dict
       ---
       parameters:
         - in: path
           name: username
           type: string
           required: true
       responses:
         200:
           description: A single user item
           schema:
             id: User
             properties:
               name:
                 type: string
                 description: The name of the user
                 default: Chris Franklin
        """
        with ClusterRpcProxy(CONFIG) as rpc:
            # asynchronously spawning and email notification
            # rpc.mail.send.async(email, subject, msg)

            # synchronously spawning the player task
            result = rpc.player.get(name)
            # TODO: handle errors here
            return result, 200


api.add_resource(Player, '/players/<username>')


if __name__ == '__main__':
    app.run(debug=True)
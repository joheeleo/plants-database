# Import your dependencies
#from urllib import request
#from os import abort
from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from models import setup_db, Plant
# Define the create_app function
def create_app(test_config=None):

    # Create and configure the app
    # Include the first parameter: Here, __name__is the name of the current Python module.
    app = Flask(__name__)
    setup_db(app)
    cors = CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    @app.route('/plants', methods=['GET'])
    def get_plants():
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * 10
        end = start + 10
        plants = Plant.query.all()
        formatted_plants = [plant.format() for plant in plants]

        return jsonify({
            'success':True,
            'plants': formatted_plants[start:end],
            'total plants': len(formatted_plants)
        })

    @app.route('/plants/<int:plant_id>')
    def get_specfic_plant(plant_id):
        plant = Plant.query.filter(Plant.id == plant_id).one_or_none()

        if plant is None:
            abort(404)
        else:
            return jsonify({
                'success':True,
                'plant': plant.format()
            })



    # Return the app instance
    return app

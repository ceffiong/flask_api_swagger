from flask import Flask, jsonify, request
from flask_cors import CORS
from data import USERS
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

# Swagger-UI config
SWAGGER_URL = "/api/docs"
API_URL = "/static/users.json"

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'Users API'
    }
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)


# define api routes
@app.route('/api/users', methods=['GET'])
def get_users():
    return jsonify(USERS), 200


@app.route('/api/user', methods=["POST"])
def create_user():
    new_user = request.get_json()
    if "name" not in new_user or new_user["name"] == "":
        return jsonify({"Error": "Name is required"}), 400
    # generate new user id
    user_id = max(user["id"] for user in USERS) + 1
    new_user["id"] = user_id
    USERS.insert(0, new_user)
    return jsonify(new_user), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)

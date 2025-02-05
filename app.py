import logging
from flask import Flask, request, jsonify
from models import OpenVPNModel

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

@app.route("/create_client", methods=["POST"])
def create_client():
    app.logger.info("Creating client...")
    data = request.get_json()
    if not data or "client_name" not in data:
        return jsonify({"error": "Missing 'client_name' in request data."}), 400

    client = data["client_name"]
    app.logger.info(client)
    if OpenVPNModel.client_exists(client):
        try:
            ovpn_config = OpenVPNModel.generate_client_config(client)
            return jsonify({"config": ovpn_config}), 200
        except Exception as e:
            app.logger.error(f"Error generating OpenVPN config: {str(e)}")
            return jsonify({"error": f"Error generating OpenVPN config: {str(e)}"}), 500

    try:
        OpenVPNModel.create_client_certificate(client)
        ovpn_config = OpenVPNModel.generate_client_config(client)
        return jsonify({"config": ovpn_config}), 200
    except Exception as e:
        app.logger.error(f"Error generating OpenVPN config: {str(e)}")
        return jsonify({"error": f"Error generating OpenVPN config: {str(e)}"}), 500

@app.route("/delete_client", methods=["POST"])
def delete_client():
    app.logger.info("Deleting client...")
    data = request.get_json()
    client_name = data.get("client_name")
    app.logger.info(client_name)
    if not client_name:
        return jsonify({"error": "Missing client_name"}), 400

    try:
        OpenVPNModel.revoke_client(client_name)
        return jsonify({"message": f"Client {client_name} deleted"}), 200
    except Exception as e:
        app.logger.error(f"Error deleting client: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/monitor_clients", methods=["GET"])
def monitor_clients():
    app.logger.info("Monitoring clients...")
    # This function can be improved further for better logging and monitoring
    pass

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
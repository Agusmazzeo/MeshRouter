from flask import jsonify, redirect, url_for

from app.containers import ApplicationContainer

from config.classes import Config


def create_app():
    """
    Creates a Flask app instance, defining its api routes.

    """
    container = ApplicationContainer()
    app = container.app()
    app.container = container
    app.config['DEBUG'] = Config.get("debug")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    @app.route("/")
    def index():
        return redirect(url_for("alive"))

    @app.route("/api/alive")
    def alive():

        return jsonify({"status": 200, "alive": True})

    @app.route("/api/test")
    def test():
        return jsonify({"status": 200})
    return app

app = create_app()

if __name__ == "__main__":
    app.logger.info(f"Registered bluprints:{app.url_map}")
    app.run(host="0.0.0.0", port="8001", debug=True, use_reloader=True)

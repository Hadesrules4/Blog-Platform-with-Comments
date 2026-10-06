import os
from flask import Flask, jsonify, render_template, request
from dotenv import load_dotenv
from .extensions import bcrypt, cors, db, jwt, login_manager
from .models import User


def create_app(test_config=None):
    load_dotenv()
    app = Flask(__name__, instance_relative_config=True)
    os.makedirs(app.instance_path, exist_ok=True)

    from config.config import Config
    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    jwt.init_app(app)
    allowed_origins = os.getenv("CORS_ORIGINS", "http://127.0.0.1:5000,http://localhost:5000").split(",")
    cors.init_app(app, resources={r"/api/*": {"origins": allowed_origins}})

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    from .auth import auth_bp
    from .main import main_bp
    from .api.routes import api_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix="/api")

    @app.context_processor
    def inject_globals():
        return {"app_name": "BlogSphere"}

    @app.errorhandler(404)
    def not_found(error):
        if request.path.startswith("/api/"):
            return jsonify(error="resource not found"), 404
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def server_error(error):
        if request.path.startswith("/api/"):
            return jsonify(error="internal server error"), 500
        return render_template("500.html"), 500

    with app.app_context():
        db.create_all()

    return app

# app.py
import os
from flask import Flask, render_template
from auth.routes import auth_bp
from tickets.routes import tickets_bp
from db import init_engine

def create_app():
    
    app = Flask(__name__, template_folder='.')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'change-me')


    db_url = os.getenv('DATABASE_URL', 'sqlite:////home/vicki888blue/mydatabase.db')
    if not os.path.exists('/home/vicki888blue/mydatabase.db'):
        db_url = 'sqlite:///mydatabase.db'
    app.config['DATABASE_URL'] = db_url
    init_engine(db_url)

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(tickets_bp)  # url_prefix can be inside the blueprint

    @app.get("/")
    def home():
        return render_template("home.html")

    return app

# WSGI entrypoint (keeps local dev working too)
application = create_app()

if __name__ == "__main__":
    application.run(debug=True)
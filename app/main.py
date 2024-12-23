from flask import Flask

from app.controllers.stat_blueprint import stat_blueprint

app = Flask(__name__)

app.register_blueprint(stat_blueprint, url_prefix='/api/stat')
if __name__ == '__main__':
    app.run()
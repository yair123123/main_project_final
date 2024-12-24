from flask import Flask
from flask_cors import CORS

from app.controllers.elastic_blueprint import elastic_blueprint
from app.controllers.relation_blueprint import relation_blueprint
from app.controllers.stat_blueprint import stat_blueprint

app = Flask(__name__)
CORS(app)
app.register_blueprint(stat_blueprint, url_prefix='/api/stat')
app.register_blueprint(relation_blueprint,url_prefix="/api/relation")
app.register_blueprint(elastic_blueprint, url_prefix="/api/elastic")
if __name__ == '__main__':
    app.run()
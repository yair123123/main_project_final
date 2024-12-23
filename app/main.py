from flask import Flask

from app.controllers.relation_blueprint import relation_blueprint
from app.controllers.stat_blueprint import stat_blueprint

app = Flask(__name__)

app.register_blueprint(stat_blueprint, url_prefix='/api/stat')
app.register_blueprint(relation_blueprint,url_prefix="/api/relation")
if __name__ == '__main__':
    app.run()
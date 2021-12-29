from flask import Flask, request
from flask_restful import Api
from PersistanceLayer.SingletonDataBase import Singleton
from BusinessLayer.ChainRouter import *

if __name__ == "__main__":
    app = Flask(__name__)
    api = Api(app)
    @app.route("/get_products/", methods=['GET', 'POST', 'DELETE', 'PUT'])
    def get_prod():
        post = PostHandler()
        get = GetHandler()
        delet = DeleteHandler()
        put = PutHandler()
        post.set_next(get).set_next((delet)).set_next(put)
        return post.handle(request.method)
    app.run(debug=True)
    Singleton().conn.close()


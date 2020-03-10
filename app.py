from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import psycopg2
import db_util
import datetime

con = psycopg2.connect(dbname='entry_exam', user='silvio', host='localhost')
cur = con.cursor()

app = Flask(__name__)
api = Api(app)


class Product(Resource):
    def get(self, product_id):
        cur.execute(f"select * from PRODUCT where id = {product_id}")
        return {'test': f'got "{cur.fetchall()}"'}


class Products(Resource):
    def get(self):
        cur.execute(f"select * from PRODUCT")
        return {'test': f'got "{cur.fetchall()}"'}

    def post(self):
        pass


class OrderEnquiries(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('from', type=str)
        parser.add_argument('to', type=str)
        args = parser.parse_args()
        return {'from': args['from'], 'to': args['to']}

    def post(self):
        return {'got': request.get_json()}


class OrderEnquiry(Resource):
    def get(self, enquiry_id):
        pass


class Finances(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('report', type=str)
        args = parser.parse_args()


api.add_resource(Product, '/api/v1/product/<int:product_id>')
api.add_resource(Products, '/api/v1/product')
api.add_resource(OrderEnquiries, '/api/v1/orderEnquiries')
api.add_resource(OrderEnquiry, '/api/v1/orderEnquiry/<int:enquiry_id>')
api.add_resource(Finances, '/api/v1/finances')

if __name__ == '__main__':
    app.run(host="127.0.0.1",port=3456)

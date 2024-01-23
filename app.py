from flask import Flask, render_template, redirect, request, session, url_for, jsonify
import shopify
import requests
import binascii
import os
#import render_template
import json
from pprint import pprint

app = Flask(__name__)

# Generate a random key for signing the session:
app.secret_key = binascii.hexlify(os.urandom(16))

# API credentials are sourced from enviroment variables:
API_KEY = 'f50445604b27c0b9c25e16a841349a34' #os.getenv("API_KEY")
API_SECRET = '7f50227b7a6b4c5379d6c829291a855f' #os.getenv("API_SECRET")
API_VERSION = '2022-10'
shopify.Session.setup(api_key=API_KEY, secret=API_SECRET)

@app.route("/")
def hello():
  return "Hello World!"

@app.route("/api/auth", methods=['GET'])
def auth():
    #return "aurth"
    # API_KEY = 'f50445604b27c0b9c25e16a841349a34'
    # SHARED_SECRET = '7f50227b7a6b4c5379d6c829291a855f'
    # shopify.Session.setup(api_key=API_KEY, secret=SHARED_SECRET)

    shop_url = "srvgeta.myshopify.com"
    api_version = '2022-10'
    state = binascii.b2a_hex(os.urandom(15)).decode("utf-8")
    
    redirect_uri = "http://127.0.0.1:5000/api/auth/redirect"
    #scopes = "read_products" #['read_products', 'read_orders']
    # aurhorize_code = requests.get(auth_url, params={'client_id':API_KEY, 'scope':scopes})
    # print(aurhorize_code)

    newSession = shopify.Session(shop_url, api_version)
    scopes = ['read_products','read_all_orders', 'read_orders','read_customers']
    auth_url = newSession.create_permission_url(scopes,redirect_uri, state)
    return redirect(auth_url, code=302)
    #return auth_url

    # accesstoke_url = "https://srvgeta.myshopify.com/admin/oauth/access_token"

    # requests.get(accesstoke_url, client_id=API_KEY, client_secret=SHARED_SECRET, code=aurhorize_code)
@app.route("/api/auth/redirect", methods=['GET','POST'])
def auth_redirect():
    args = request.args
    #return code
    shop_url = args['shop']
    api_version = '2022-10'
    shopify_session = shopify.Session(shop_url, api_version)
    #params = {'client_id':API_KEY, 'client_secret':SHARED_SECRET, 'code':code}
    #params = {'code':code,'hmac':hmac,'timestamp':timestamp}
    access_token = shopify_session.request_token(request.args)
    #return access_token
    session['shop'] = shop_url
    session['access_token'] = access_token

    return redirect(url_for('product'))

@app.route("/productlist", methods=['GET'])
def product():
    api_session = shopify.Session(
        session['shop'],
        API_VERSION,
        session['access_token'])
    shopify.ShopifyResource.activate_session(api_session)
    shop = shopify.Shop.current() # Get the current shop
    #return shop
    #print(shop.to_json())
    orders =  shopify.Order.find(limit=10)
    ordersJSON=[]
    for order in orders:
        ordersJSON.append(order.to_dict())

    return jsonify(ordersJSON)
    products = shopify.Product.find(limit=10)
    
    
    print(len(products))
    #pprint(vars(products))
    print(type(products))
    productsJSON=[]
    for product in products:
        productsJSON.append(product.to_dict())
        #print(product.title)
    #print(productsJSON)
    #pprint(vars(products))
    response = app.response_class(
        response=json.dumps(productsJSON),
        status=200,
        mimetype='application/json'
    )
    return jsonify(productsJSON)
    #return render_template('products.html', api_key=API_KEY, products=products)
@app.route("/cart")
def cart():
    api_session = shopify.Session(
        session['shop'],
        API_VERSION,
        session['access_token'])
    print(api_session)
    shopify.ShopifyResource.activate_session(api_session)
    # shop = shopify.Shop.current() # Get the current shop
    # #return shop
    # print(shop.to_json())

if __name__ == "__main__":
  app.run(debug=True)
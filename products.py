import shopify
API_KEY = 'aa2274f588e8334f92039f5d48d713b3'
API_SECRET = '1637d4f6b1659ffe13899224ddf329dd'
shopify.Session.setup(api_key=API_KEY, secret=API_SECRET)

shop_url = "srvgeta.myshopify.com"
api_version = '2020-10'
state = binascii.b2a_hex(os.urandom(15)).decode("utf-8")
redirect_uri = "http://myapp.com/auth/shopify/callback"
scopes = ['read_products', 'read_orders']

session = shopify.Session(shop_url, api_version)
access_token = session.request_token(request_params) # request_token will validate hmac and timing attacks
# you should save the access token now for future use.

session = shopify.Session(shop_url, api_version, access_token)
shopify.ShopifyResource.activate_session(session)

shop = shopify.Shop.current() # Get the current shop
product = shopify.Product.find(179761209) # Get a specific produc

newSession = shopify.Session(shop_url, api_version)
auth_url = newSession.create_permission_url(scopes, redirect_uri, state)

shop = "srvgeta.myshopify.com"
token = "shpua_27bc635bf791d47416087bf1551ab6e0"
session = shopify.Session(shop, token)
shopify.ShopifyResource.activate_session(session)
shop = shopify.Shop.current
print(shop)
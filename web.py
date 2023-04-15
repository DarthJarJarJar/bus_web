from flask import Flask
import time
from main import get_data, get_routes
from flask import request

app = Flask(__name__)


@app.route('/')
def hello():
    r = request.args.get('r')
    return get_data(time, r)

@app.route('/routes')
def there():
    return get_routes()
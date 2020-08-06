from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'e9asCL9Ro3adQmsD'

from clubquiz import routes

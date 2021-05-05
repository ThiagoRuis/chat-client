from flask import Flask

def init_app(app: Flask):
    from routes import identification
    from routes import chat
    from routes import command
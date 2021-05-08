from flask import Flask
from flask_rebar import Rebar, SwaggerV3Generator

from ext.auth import Authentication

rebar = Rebar()

api_v1 = rebar.create_handler_registry(
    prefix='/api',
    swagger_path='/swagger',
    swagger_ui_path='/docs',
    swagger_generator=SwaggerV3Generator(title='RUIS Chat API', description='') #TODO: put app description over here
)

authenticator = Authentication()

def init_app(app: Flask):
    rebar.init_app(app)
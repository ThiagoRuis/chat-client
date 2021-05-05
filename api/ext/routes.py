from flask import Flask
from flask_rebar import Rebar, SwaggerV3Generator

rebar = Rebar()

api_v1 = rebar.create_handler_registry(
    prefix='/v1',
    swagger_path='/swagger',
    swagger_ui_path='/docs',
    swagger_generator=SwaggerV3Generator(title='RUIS Chat API', description='') #TODO: put app description over here
)

def init_app(app: Flask):
    rebar.init_app(app)
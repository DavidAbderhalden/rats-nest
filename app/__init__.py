"""Application base package loading environments"""
from jinja2 import Environment, PackageLoader, select_autoescape

templates_environment = Environment(
    loader=PackageLoader(package_name='app', package_path='templates/email'),
    autoescape=select_autoescape(['html', 'xml'])
)

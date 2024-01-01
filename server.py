from waitress import serve
from TechAdminsProject.wsgi import application as app

if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=8000)
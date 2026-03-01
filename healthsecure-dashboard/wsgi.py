# WSGI config for HealthSecure backend on PythonAnywhere
import sys

# Add your project directory to the path
path = '/home/eh722783/healthsecure_backend'
if path not in sys.path:
    sys.path.insert(0, path)

# Run the FastAPI application with asgiref
def application(environ, start_response):
    from main import app
    from asgiref.wsgi import AsgiHandler
    handler = AsgiHandler(app)
    return handler(environ, start_response)

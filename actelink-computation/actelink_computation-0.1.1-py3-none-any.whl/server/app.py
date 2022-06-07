from actelink.config import settings
from actelink.logger import log
from actelink.server import create_app

def start():
    # start flask server
    app = create_app()
    log.debug(f"Starting app in {app.config['ENV']} environment on {settings.HOST}:{settings.PORT}")
    app.run(host=settings.HOST, port=settings.PORT, use_reloader=False)
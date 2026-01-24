from flask import Flask
from .config import app_config
from .models import db
from .views.people import people_api as people


def create_app(env_name: str) -> Flask:
    """
    Initializes the application registers

    Parameters:
        env_name: the name of the environment to initialize the app with

    Returns:
        The initialized app instance
    """
    app = Flask(__name__)
    app.config.from_object(app_config[env_name])
    db.init_app(app)

    app.register_blueprint(people, url_prefix="/")

    @app.route('/', methods=['GET'])
    def index():
        """
        Root endpoint for populating root route

        Returns:
            Greeting message
        """
        return """
        Welcome to the Titanic API
        """
# Health check endpoint for Docker and Kubernetes
    @app.route('/health', methods=['GET'])
    def health_check():
        """
        Health check endpoint for container orchestration
        Returns 200 if the application is healthy
        """
        try:
            # Check database connection
            db.session.execute('SELECT 1')
            return {
                'status': 'healthy',
                'database': 'connected',
                'service': 'titanic-api'
            }, 200
        except Exception as e:
            return {
                'status': 'unhealthy',
                'database': 'disconnected',
                'error': str(e)
            }, 503

    # Root endpoint
    @app.route('/', methods=['GET'])
    def api_index():
        """
        Root endpoint
        """
        return {
            'message': 'Welcome to Titanic API',
            'version': '1.0.0',
            'endpoints': {
                'health': '/health',
                'passengers': '/api/v1/passengers'
            }
        }, 200
    return app

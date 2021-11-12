from flask import Flask
from config import config_options
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet,configure_uploads,IMAGES
from flask_login import  LoginManager
from flask_mail import Mail



#database 
db = SQLAlchemy()
#login Hellper classes
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
#Upload files
photos = UploadSet('photos',IMAGES)

#send mail
mail = Mail()


def create_app(config_name):

    app = Flask(__name__)

    # Creating the app configurations
    app.config.from_object(config_options[config_name])   

    # Registering the blueprint
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint,url_prefix = '/authenticate')
    
    #Intializing flask extensions
    db.init_app(app)#databse
    login_manager.init_app(app)#login helper
    mail.init_app(app)#mail

    # configure UploadSet
    configure_uploads(app,photos)

     # setting config
 

    return app
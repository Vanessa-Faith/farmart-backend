from app import create_app
from dotenv import load_dotenv
import os

# Load .env
load_dotenv()

# Read env variables
SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = os.getenv("DEBUG") == "True"
PORT = int(os.getenv("PORT", 5000))

# Pass secret key to your app
app = create_app()
app.config['SECRET_KEY'] = SECRET_KEY  # <-- use it here

if __name__ == "_main_":
    app.run(debug=DEBUG, port=PORT)  # <-- use DEBUG and PORT
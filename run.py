from app import create_app
from dotenv import load_dotenv
import os

# Load .env
load_dotenv()

# Create app
app = create_app()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("DEBUG", "True") == "True"
    app.run(debug=debug, port=port, host='0.0.0.0')


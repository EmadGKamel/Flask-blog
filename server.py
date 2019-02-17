from blog import app
from os import getenv


port = int(getenv('PORT', 8000))
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)

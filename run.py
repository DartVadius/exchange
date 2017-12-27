#!/usr/bin/python3.4
from app import app

app.run(debug=True, host="127.0.0.1", port=8007, threaded=True)

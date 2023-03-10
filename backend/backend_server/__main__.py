import uvicorn
import backend_server.app as app
import os

uvicorn.run(app.app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

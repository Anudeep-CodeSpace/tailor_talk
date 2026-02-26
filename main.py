import uvicorn
from backend.app import app
import os

def main():
    print('Starting the backend Server....\n')
    uvicorn.run(app=app, host="0.0.0.0", port=os.getenv('PORT'))


if __name__ == "__main__":
    main()

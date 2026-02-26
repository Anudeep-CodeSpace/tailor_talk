import uvicorn
from backend.app import app

def main():
    print('Starting the backend Server....\n')
    uvicorn.run(app=app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()

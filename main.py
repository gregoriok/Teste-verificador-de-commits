from fastapi import FastAPI

app = FastAPI()

@app.get("/hello")
def hello():
    return {"message": "hello world"}

@app.post("/users")
def create_user(name: str):
    return {"user": name}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,host="localhost", port=8000)
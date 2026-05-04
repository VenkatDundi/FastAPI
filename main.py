from fastapi import FastAPI


app = FastAPI(title="First FastAPI Application", version="1.0")

# Endpoint 1 - Health Check (GET)

@app.get("/")
def root():
    return {"message": "Fast API is up and running!"}


# Endpoint 2 - Simple Hello (GET)

@app.get("/hello/{name}")
def request_hello(name: str):
    return {"message": f"Hello, {name}!"}

# Endpoint 3 - Add Two Numbers (GET)
@app.get("/add/{a}+{b}")
def add_numbers(a: int, b: int):
    result = a + b
    return {"result": result}
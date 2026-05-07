from fastapi import FastAPI

from schemas import LoanApplication, LoanResponse


app = FastAPI(title="First FastAPI Application", version="1.0")

# Endpoint 1 - Health Check (GET)

@app.get("/")
def root():
    return {"message": "Fast API is up and running!"}


# Endpoint 2 - Simple Hello (GET)

@app.get("/hello/{name}")
def request_hello(name: str):
    return {"message": f"Hello, {name}!"}


# Endpoint 3 - Apply for a Loan (POST)

@app.post("/apply-loan", response_model=LoanResponse)
def apply_loan(application: LoanApplication):

    return LoanResponse(
        applicant_name = application.applicant_name,
        age = application.age,
        annual_income = application.annual_income,
        loan_amount = application.loan_amount,
        credit_score = application.credit_score,
        status = "Received",
        message = "Application received and validated successfully"
    )
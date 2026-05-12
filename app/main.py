from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas import LoanApplication, LoanResponse
from ml.model import predict_loan_approval
from app.auth import verify_password, create_token, get_current_user, USERS_DB

app = FastAPI(title="Loan Prediction API", version="3.0")


# ── Public endpoints — no auth required ──────────────────────
@app.get("/")
def root():
    return {"message": "Loan Prediction API", "version": "3.0"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


# ── Login endpoint — issues JWT token ─────────────────────────
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = USERS_DB.get(form_data.username)

    if not user or not verify_password(form_data.password,
                                       user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )

    token = create_token({
        "sub":  user["username"],
        "role": user["role"]
    })

    return {"access_token": token, "token_type": "bearer"}


# ── Protected endpoint — JWT required ─────────────────────────
@app.post("/predict", response_model=LoanResponse)
def predict_loan(
    application: LoanApplication,
    current_user: dict = Depends(get_current_user)  # ← auth enforced
):
    print(f"Request from: {current_user['username']} "
          f"| Role: {current_user['role']}")

    result = predict_loan_approval(
        age              = application.age,
        annual_income    = application.annual_income,
        loan_amount      = application.loan_amount,
        credit_score     = application.credit_score
    )

    message = (
        f"Congratulations {application.applicant_name}! Approved."
        if result["approved"]
        else f"Sorry {application.applicant_name}. Not approved."
    )

    return LoanResponse(
        applicant_name = application.applicant_name,
        loan_amount    = application.loan_amount,
        decision       = result["decision"],
        approved       = result["approved"],
        confidence     = result["confidence"],
        message        = message
    )
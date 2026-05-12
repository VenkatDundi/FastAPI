from pydantic import BaseModel, Field, model_validator

class LoanApplication(BaseModel):
    
    applicant_name: str = Field(min_length=3, max_length = 100, description="Name of the applicant")
    age: int = Field(ge=18, le=100, description="Age of the applicant - Must be between 18 and 100 ")
    annual_income: float = Field(gt=1000, lt = 1_000_000, description="Annual income of the applicant - Must be greater than 1000 and less than 1 million")
    loan_amount: float = Field(gt=500, lt=500_000, description="Loan amount must be between 500 and 500,000")
    credit_score: int = Field(ge=575, lt=850, description="Credit score must be between 575 and 850")


    # Cross-field business logic validator
    @model_validator(mode="after")
    def loan_must_not_exceed_income_multiple(self):
        income = self.annual_income
        loan   = self.loan_amount

        if income and loan and loan > income * 10:
            raise ValueError(
                f"Loan amount ${loan:,.0f} cannot exceed "
                f"10x annual income ${income:,.0f}"
            )
        return self

class LoanResponse(BaseModel):
    applicant_name: str
    loan_amount:    float
    decision:       str
    approved:       bool
    confidence:     float
    message:        str
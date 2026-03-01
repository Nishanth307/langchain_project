from pydantic import BaseModel, Field
from typing import Literal, Optional

class Address(BaseModel):
      """Address information."""
      street: Optional[str] = Field(default="", description="Street address if known")
      city: str = Field(description="City name")
      country: str = Field(description="Country name")
      
class Company(BaseModel):
      """Company information with nested address."""
      name :str = Field(description="Company name")
      industry: Literal["Technology", "Finance","HealthCare","Retail","Other"] = Field(
            description = "Industry sector"
      )
      employee_count: int = Field(description="Number of employees")
      headquarters: Address = Field(description="Company headquarters location")
      is_public: bool = Field(description="Whether the company is publicly traded")
      
class PydanticPrompting:
      def __init__(self,model):
            self.model = model
      
      def pydantic_schema(self):
            structured_model = self.model.with_structured_output(Company)
            text = """
                  Microsoft Corporation is a technology giant headquartered in Redmond, Washington, USA.
                  The company has approximately 220,000 employees worldwide and is publicly traded on NASDAQ.
            """
            prompt = (
                  f"Extract company information from the text below. "
                  f"You must include: name, industry, employee_count, headquarters (with street, city, country), and is_public. "
                  f"Text: {text}"
            )
            result = structured_model.invoke(prompt)
            print(result)
            
      
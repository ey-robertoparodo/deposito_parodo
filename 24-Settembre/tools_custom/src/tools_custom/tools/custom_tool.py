from typing import Type

from crewai.tools import BaseTool
from pydantic import BaseModel, Field

class SumToolInput(BaseModel):
    """Input schema for SumTool."""
    a: int = Field(..., description="the first integer number")
    b: int = Field(..., description="the second integer number")

class SumTool(BaseTool):
    name: str = "Sum Tool"
    description: str = (
        "Calculates the sum of numbers in a simple addition expression (e.g. '2+2+5')."
    )
    args_schema: Type[BaseModel] = SumToolInput

    def _run(self, a: int, b: int) -> str:
        return a+b
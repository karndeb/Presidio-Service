from pydantic import BaseModel
from typing import List, Optional, Union, Dict, Any


class AnonymizeRequest(BaseModel):
    text: str
    anonymizers: Optional[Dict]
    analyzer_results: Optional[List[Dict]]


class DeanonymizeRequest(BaseModel):
    text: str
    deanonymizers: Optional[Dict]
    anonymizer_results: Optional[List[Dict]]


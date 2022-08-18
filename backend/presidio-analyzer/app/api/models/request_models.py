from pydantic import BaseModel
from typing import List, Optional, Union, Dict


class AnalyzeRequest(BaseModel):
    text: str
    language: str
    entities: Optional[List[str]]
    correlation_id: Optional[str]
    score_threshold: Optional[float]
    return_decision_process: Optional[bool]
    ad_hoc_recognizers: Optional[Dict]
    context: Optional[List[str]]
    allow_list: Optional[List[str]]
    # nlp_artifacts: Optional[List]


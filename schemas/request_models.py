from pydantic import BaseModel, Field
from typing import List, Optional, Any, Dict

class OCRRequest(BaseModel):
    data: Dict[str, Any]
    image_field: str = "image"
    max_num: Optional[int] = 6
    
    class Config:
        schema_extra = {
            "example": {
                "data": {
                    "id": "123",
                    "image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQ...",
                    "other_field": "some_value"
                },
                "image_field": "image",
                "max_num": 6
            }
        }

class OCRResult(BaseModel):
    original_data: dict
    ocr_text: str
    description: Optional[str] = None 

class OCRResponse(BaseModel):
    results: List[OCRResult]
    
    class Config:
        schema_extra = {
            "example": {
                "results": [
                    {
                        "original_data": {"id": "123", "other_field": "value"},
                        "ocr_text": "Extracted text from image..."
                    }
                ]
            }
        }

class ImageAnalysisRequest(BaseModel):
    question: str = Field(..., description="Câu hỏi cần phân tích")
    max_num: int = Field(default=6, description="Số lượng kết quả tối đa")
    
    model_config = {
        "json_schema_extra": { 
            "example": {
                "question": "Trích xuất toàn bộ text từ tài liệu này",
                "max_num": 6
            }
        }
    }

class AnalysisResult(BaseModel):
    description: str
    confidence: float = 0.0

class ImageAnalysisResponse(BaseModel):
    results: List[AnalysisResult]
    timestamp: str
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "results": [
                    {
                        "description": "Text được trích xuất từ tài liệu",
                        "confidence": 0.95
                    }
                ],
                "timestamp": "2025-09-15T10:00:00Z"
            }
        }
    }
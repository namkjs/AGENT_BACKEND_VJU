from transformers import AutoModelForCausalLM, AutoTokenizer
import json
import re
from typing import Dict, Any, List

class Agent:
    def __init__(self):
        self.model_path = "phamhai/Llama-3.2-1B-Instruct-Frog"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
        self.model = AutoModelForCausalLM.from_pretrained(self.model_path)
        
    async def check_document_approval(self, ocr_text: str) -> Dict[str, Any]:
        """Kiểm tra tài liệu có được approve không dựa trên OCR text"""
        
        system_prompt = """Bạn là một chuyên gia đánh giá tài liệu. Nhiệm vụ của bạn là phân tích nội dung tài liệu và quyết định có nên phê duyệt (approve) hay từ chối (reject) tài liệu này.

Hãy đánh giá dựa trên các tiêu chí sau:
1. Tính đầy đủ của thông tin
2. Tính rõ ràng và dễ hiểu
3. Tính hợp lệ của nội dung
4. Có chứa thông tin nhạy cảm hay không phù hợp không

Trả lời CHÍNH XÁC theo định dạng JSON sau:
{
    "approve": "accept" hoặc "reject",
    "description": "Giải thích chi tiết lý do quyết định"
}"""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Hãy đánh giá tài liệu sau:\n\n{ocr_text}"}
        ]
        
        try:
            tokenized_chat = self.tokenizer.apply_chat_template(
                messages, 
                tokenize=True, 
                add_generation_prompt=True, 
                return_tensors="pt"
            )
            
            outputs = self.model.generate(
                tokenized_chat, 
                max_new_tokens=1024,
                do_sample=False,
                temperature=0.1
            )
            
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            generated_text = self._extract_generated_response(response, messages)
            approval_result = self._parse_approval_response(generated_text)
            
            return approval_result
            
        except Exception as e:
            print(f"❌ Error in document approval check: {str(e)}")
            return {
                "approve": "reject",
                "description": f"Lỗi trong quá trình đánh giá tài liệu: {str(e)}"
            }
    
    def _extract_generated_response(self, full_response: str, messages: List[Dict]) -> str:
        """Trích xuất phần response được generate từ model"""
        try:
            user_content = messages[-1]["content"]
            parts = full_response.split(user_content)
            if len(parts) > 1:
                generated_part = parts[-1].strip()
                return generated_part
            return full_response
        except Exception as e:
            print(f"Warning: Could not extract generated response: {e}")
            return full_response
    
    def _parse_approval_response(self, response_text: str) -> Dict[str, Any]:
        """Parse JSON response từ model"""
        try:
            json_match = re.search(r'\{[^{}]*"approve"[^{}]*\}', response_text)
            if json_match:
                json_str = json_match.group(0)
                result = json.loads(json_str)
                
                if "approve" in result:
                    if result["approve"] not in ["accept", "reject"]:
                        result["approve"] = "reject"
                        result["description"] = "Invalid approval status from model"
                    
                    if "description" not in result:
                        result["description"] = "Không có mô tả chi tiết"
                    
                    return result
            
            # If no valid JSON found, try to parse manually
            if "accept" in response_text.lower():
                approve_status = "accept"
            else:
                approve_status = "reject"
            
            return {
                "approve": approve_status,
                "description": response_text.strip()
            }
            
        except json.JSONDecodeError:
            return {
                "approve": "reject",
                "description": f"Không thể phân tích phản hồi từ model: {response_text}"
            }
        except Exception as e:
            return {
                "approve": "reject",
                "description": f"Lỗi trong quá trình phân tích phản hồi: {str(e)}"
            }
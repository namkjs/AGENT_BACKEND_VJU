import torch
from transformers import AutoModel, AutoTokenizer
from utils.image_processor import ImageProcessor
import asyncio

class VisionModel:
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.image_processor = ImageProcessor()
        self.model_name = "5CD-AI/Vintern-1B-v3_5"
        self.generation_config = {
            "max_new_tokens": 512,
            "do_sample": False,
            "num_beams": 3,
            "repetition_penalty": 3.5
        }
    
    async def load_model(self):
        """Load the vision model asynchronously"""
        def _load():
            try:
                model = AutoModel.from_pretrained(
                    self.model_name,
                    torch_dtype=torch.bfloat16,
                    low_cpu_mem_usage=True,
                    trust_remote_code=True,
                    use_flash_attn=False,
                ).eval().cuda()
            except:
                model = AutoModel.from_pretrained(
                    self.model_name,
                    torch_dtype=torch.bfloat16,
                    low_cpu_mem_usage=True,
                    trust_remote_code=True
                ).eval().cuda()
            
            tokenizer = AutoTokenizer.from_pretrained(
                self.model_name, 
                trust_remote_code=True, 
                use_fast=False
            )
            
            return model, tokenizer
        
        # Run model loading in thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        self.model, self.tokenizer = await loop.run_in_executor(None, _load)
    
    async def analyze_image(self, image, question: str, max_num: int = 6):
        """Analyze image asynchronously"""
        if self.model is None or self.tokenizer is None:
            raise RuntimeError("Model not loaded")
        
        def _analyze():
            pixel_values = self.image_processor.load_image_from_pil(
                image, max_num=max_num
            ).to(torch.bfloat16).cuda()
            
            response = self.model.chat(
                self.tokenizer, 
                pixel_values, 
                question, 
                self.generation_config
            )
            return response
        
        # Run inference in thread pool
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, _analyze)
        return result
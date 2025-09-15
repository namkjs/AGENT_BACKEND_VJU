import asyncio
from models.vision_model import VisionModel
from models.agent import Agent
from PIL import Image
import os

async def test_local_image(image_path: str):
    """Test pipeline với ảnh local"""
    
    # Kiểm tra file có tồn tại không
    if not os.path.exists(image_path):
        print(f"❌ File không tồn tại: {image_path}")
        return
    
    print(f"🖼️ Đang test với ảnh: {image_path}")
    print(f"📁 File size: {os.path.getsize(image_path)} bytes")
    
    try:
        # Load models
        vision_model = VisionModel()
        agent = Agent()
        
        print("🔄 Đang load vision model...")
        await vision_model.load_model()
        
        # Load và display ảnh
        image = Image.open(image_path).convert("RGB")
        print(f"🖼️ Kích thước ảnh: {image.size}")
        
        # Chạy OCR
        print("🔍 Đang chạy OCR...")
        analysis_response = await vision_model.analyze_image(
            image, 
            question="Trích xuất toàn bộ text từ tài liệu này một cách chi tiết và chính xác.",
            max_num=6
        )
        
        # Debug: Kiểm tra kiểu dữ liệu của response
        print(f"🔍 Type of analysis_response: {type(analysis_response)}")
        print(f"🔍 Analysis response: {analysis_response}")
        
        # Lấy text từ OCR - sửa lại logic này
        ocr_text = ""
        if hasattr(analysis_response, 'results') and analysis_response.results:
            # Nếu response có thuộc tính results
            for result in analysis_response.results:
                if hasattr(result, 'description'):
                    ocr_text += result.description + "\n"
                else:
                    ocr_text += str(result) + "\n"
        elif isinstance(analysis_response, str):
            # Nếu response là string
            ocr_text = analysis_response
        elif isinstance(analysis_response, dict) and 'results' in analysis_response:
            # Nếu response là dict có key results
            for result in analysis_response['results']:
                if isinstance(result, dict) and 'description' in result:
                    ocr_text += result['description'] + "\n"
                else:
                    ocr_text += str(result) + "\n"
        else:
            # Fallback: convert to string
            ocr_text = str(analysis_response)
        
        print("📄 Kết quả OCR:")
        print("-" * 50)
        print(ocr_text)
        print("-" * 50)
        
        # Chạy Agent để kiểm tra approval
        print("🤖 Đang kiểm tra với Agent...")
        approval_result = await agent.check_document_approval(ocr_text)
        
        # Hiển thị kết quả
        print("\n✅ KẾT QUẢ CUỐI CÙNG:")
        print(f"📋 Quyết định: {approval_result.get('approve', 'unknown')}")
        print(f"💬 Lý do: {approval_result.get('description', 'Không có mô tả')}")
        
        return {
            "ocr_text": ocr_text.strip(),
            "approval": approval_result,
            "image_path": image_path,
            "image_size": image.size
        }
        
    except Exception as e:
        print(f"❌ Lỗi trong quá trình test: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

# Tạo một script test đơn giản hơn
async def simple_test(image_path: str = "static/1.jpg"):
    """Test đơn giản với debug chi tiết"""
    
    print(f"🚀 Starting simple test with: {image_path}")
    
    try:
        # Load models
        print("📦 Loading VisionModel...")
        vision_model = VisionModel()
        await vision_model.load_model()
        
        print("📦 Loading Agent...")
        agent = Agent()
        
        # Load image
        print("🖼️ Loading image...")
        image = Image.open(image_path).convert("RGB")
        print(f"Image size: {image.size}, mode: {image.mode}")
        
        # Test OCR
        print("🔍 Running OCR...")
        try:
            response = await vision_model.analyze_image(
                image, 
                "Extract all text from this document in detail",
                max_num=6
            )
            
            print(f"✅ OCR completed. Response type: {type(response)}")
            
            # Handle different response types
            if hasattr(response, 'results'):
                ocr_text = "\n".join([r.description for r in response.results])
            elif isinstance(response, str):
                ocr_text = response
            else:
                ocr_text = str(response)
                
            print(f"📄 Extracted text (first 200 chars): {ocr_text[:200]}...")
            
        except Exception as ocr_error:
            print(f"❌ OCR Error: {ocr_error}")
            import traceback
            traceback.print_exc()
            return None
        
        # Test Agent
        print("🤖 Running Agent approval check...")
        try:
            approval = await agent.check_document_approval(ocr_text)
            print(f"✅ Agent completed. Result: {approval}")
            
            return {
                "ocr_text": ocr_text,
                "approval": approval,
                "image_path": image_path
            }
            
        except Exception as agent_error:
            print(f"❌ Agent Error: {agent_error}")
            import traceback
            traceback.print_exc()
            return None
            
    except Exception as e:
        print(f"❌ General Error: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    print("🚀 BẮT ĐẦU TEST LOCAL IMAGE")
    print("=" * 60)
    
    # Test với ảnh có sẵn
    test_images = ["static/1.jpg", "static/2.jpg"]
    
    for image_path in test_images:
        if os.path.exists(image_path):
            print(f"\n📸 Testing with simple_test: {image_path}")
            print("-" * 40)
            
            result = asyncio.run(simple_test(image_path))
            
            if result:
                print("✅ Test thành công!")
                print(f"📋 Approve: {result['approval'].get('approve', 'unknown')}")
                print(f"💬 Description: {result['approval'].get('description', 'N/A')}")
            else:
                print("❌ Test thất bại!")
                
            print("\n" + "=" * 60)
        else:
            print(f"⚠️ File không tồn tại: {image_path}")
    
    # Test custom image
    custom_image_path = input("\n🎯 Nhập đường dẫn ảnh để test (Enter để bỏ qua): ").strip()
    if custom_image_path and os.path.exists(custom_image_path):
        print(f"\n📸 Testing custom image: {custom_image_path}")
        result = asyncio.run(simple_test(custom_image_path))
        
        if result:
            print("✅ Custom test thành công!")
            print(f"📋 Approve: {result['approval'].get('approve', 'unknown')}")
            print(f"💬 Description: {result['approval'].get('description', 'N/A')}")
        else:
            print("❌ Custom test thất bại!")
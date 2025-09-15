from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any, Dict, List
import httpx
import asyncio
from database.database import get_pending_proposal_ids, get_pending_document_proposals
from pipeline.run_pipeline import run_full_pipeline
import time
app = FastAPI(title="Vision AI API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ProposalRequest(BaseModel):
    data: Any  # Accept any data from FE
    
class ProposalResponse(BaseModel):
    status: str
    message: str
    pending_proposal_ids: List[int] = []  # Add pending IDs to response

async def send_to_another_server(result_data: dict):
    """Gửi kết quả đến server khác"""
    try:
        # URL server khác - thay đổi theo server của bạn
        target_server_url = "http://13.238.116.61:3001/review/ai/send"
        
        # Prepare data to send
        # payload = {
        #     "result": result_data,
        # }
        
        # Gửi request đến server khác
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                target_server_url,
                json=result_data,
                headers={
                    "Content-Type": "application/json",
                }
            )
            print(response)
            if response.status_code == 200 or response.status_code == 201:
                print(f"✅ Successfully sent result to another server")
                print(f"Response: {response.json()}")
            else:
                print(f"❌ Failed to send to another server: {response.status_code}")
                print(f"Error: {response.text}")
                
    except httpx.TimeoutException:
        print("⏰ Timeout when sending to another server")
    except Exception as e:
        print(f"❌ Error sending to another server: {str(e)}")

@app.post("/check_proposal")
async def check_proposal():
    print(1)
    """Endpoint để FE đánh thức server"""
    try:
        print("🚀 Server has been awakened by FE!")
        
        pending_ids = await get_pending_proposal_ids()
        print(f"📋 Found {len(pending_ids)} pending proposals: {pending_ids}")
        
        for pending_id in pending_ids:
            document_proposals = await get_pending_document_proposals(pending_id)
            print("Document:", document_proposals)
            
            if len(document_proposals) == 0:
                continue
            
            for document_proposal in document_proposals:
                print(f"📄 Processing: {document_proposal['attachment_path']}")
                print(f"📊 Document proposal ID: {document_proposal['id']}")
                print(f"📊 Proposal ID: {document_proposal['proposal_id']}")
                
                result_data = await run_full_pipeline(document_proposal['attachment_path'])
                print(f"🔍 Pipeline result: {result_data}")
                
                # Format theo yêu cầu của server đích
                merged_result = {
                    "proposal_id": str(document_proposal['proposal_id']),  # UUID string (required)
                    "approve": result_data.get("approve") == "accept",     # Boolean (required) - convert "accept"/"reject" thành True/False
                    "respond": result_data.get("description", "")          # String (required)
                }
                
                print(f"📋 Sending to server: {merged_result}")
                await send_to_another_server(merged_result)
        
        return ProposalResponse(
            status="success",
            message=f"Server is awake! Found {len(pending_ids)} pending proposals.",
            pending_proposal_ids=pending_ids
        )
        
    except Exception as e:
        print(f"❌ Error in check_proposal: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/pending-proposals")
async def get_pending_proposals():
    """Endpoint để lấy danh sách proposal PENDING"""
    try:
        pending_ids = await get_pending_proposal_ids()
        return {
            "status": "success",
            "count": len(pending_ids),
            "pending_proposal_ids": pending_ids
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
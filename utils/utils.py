from pydantic import BaseModel
class DocumentProposal(BaseModel):
    id: str
    proposal_id: str
    document_id: str
    attachment_path:str
    mimetype: str
    created_at: str
    updated_at: str
    approve: bool

class Proposal(BaseModel):
    id:str
    activity_id:str
    code:str
    security_code:str
    full_name:str
    email:str
    phone:str
    address:str
    note:str
    respond:str
    status:str
    completed_at:str
    created_at:str
    updated_at:str


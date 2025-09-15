import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_pending_proposal_ids():
    """Tìm các id của proposal có status PENDING"""
    try:
        db = SessionLocal()
        
        # Query để tìm các proposal có status PENDING
        query = text("SELECT id FROM \"Proposal\" WHERE status = 'PENDING'")
        result = db.execute(query)
        
        # Lấy tất cả id
        pending_ids = [row[0] for row in result.fetchall()]
        
        db.close()
        return pending_ids
        
    except Exception as e:
        print(f"❌ Error querying database: {str(e)}")
        return []
    
async def get_pending_document_proposals(proposal_id):
    """Lấy tất cả document_proposals cho một proposal_id cụ thể"""
    try:
        db = SessionLocal()

        # Query để lấy tất cả documents của proposal này
        query = text("""
            SELECT *
            FROM \"DocumentProposal\" 
            WHERE proposal_id = :proposal_id
        """)
        result = db.execute(query, {"proposal_id": proposal_id})

        # Convert to list of dictionaries với column mapping
        columns = result.keys()
        if result is not None or result.rowcount > 0:
            document_proposals = [dict(zip(columns, row)) for row in result.fetchall()]
        
        db.close()
        return document_proposals
        
    except Exception as e:
        print(f"❌ Error querying document proposals for proposal_id {proposal_id}: {str(e)}")
        return []


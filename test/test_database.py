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

async def get_all_tables():
    """Lấy danh sách tất cả các bảng trong database"""
    try:
        db = SessionLocal()
        
        # Query để lấy tất cả tên bảng
        query = text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        result = db.execute(query)
        
        tables = [row[0] for row in result.fetchall()]
        
        db.close()
        return tables
        
    except Exception as e:
        print(f"❌ Error querying tables: {str(e)}")
        return []

async def get_pending_proposal_ids():
    """Tìm các id của proposal có status PENDING"""
    try:
        db = SessionLocal()

        try:
            query = text(f"SELECT id FROM \"Proposal\" WHERE status = 'PENDING' LIMIT 1")
            print(query)
            result = db.execute(query)
            print(f"✅ Found table: \"Proposal\"")

            # Nếu query thành công, lấy tất cả id
            query = text(f"SELECT id FROM \"Proposal\" WHERE status = 'PENDING'")
            result = db.execute(query)
            pending_ids = [row[0] for row in result.fetchall()]
            
            db.close()
            return pending_ids
            
        except Exception as table_error:
            print(f"❌ Table '\"Proposal\"' not found: {table_error}")
        db.close()
        return []
        
    except Exception as e:
        print(f"❌ Error querying database: {str(e)}")
        return []

async def get_pending_document_proposals(pending_ids):
    """Lấy tất cả document_proposals có status PENDING"""
    try:
        db = SessionLocal()
        
        if not pending_ids:
            return []

        # Thử các tên bảng có thể có
        possible_table_names = ["DocumentProposal", "document_proposals", "document_proposal", "DocumentProposals"]
        
        for table_name in possible_table_names:
            try:
                query = text(f"SELECT * FROM {table_name} WHERE proposalid = ANY(:pending_ids)")
                result = db.execute(query, {"pending_ids": pending_ids})
                
                print(f"✅ Found table: {table_name}")
                document_proposals = [dict(row._mapping) for row in result.fetchall()]
                
                db.close()
                return document_proposals
                
            except Exception as table_error:
                print(f"❌ Table '{table_name}' not found: {table_error}")
                continue
        
        db.close()
        return []
        
    except Exception as e:
        print(f"❌ Error querying database: {str(e)}")
        return []
    
import asyncio

if __name__ == "__main__":
    print(asyncio.run(get_all_tables()))
    print(asyncio.run(get_pending_proposal_ids()))
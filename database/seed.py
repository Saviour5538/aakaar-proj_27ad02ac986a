import uuid
from datetime import datetime, timedelta
from sqlalchemy.exc import SQLAlchemyError
from database.models import (
    engine,
    SessionLocal,
    User,
    Session,
    Document,
    DocumentChunk,
    Query,
    QuerySource,
)

def seed_database():
    session = SessionLocal()
    try:
        # Create sample users
        user1 = User(
            id=uuid.uuid4(),
            email="user1@example.com",
            hashed_password="hashed_password_1",
            created_at=datetime.utcnow(),
        )
        user2 = User(
            id=uuid.uuid4(),
            email="user2@example.com",
            hashed_password="hashed_password_2",
            created_at=datetime.utcnow(),
        )
        user3 = User(
            id=uuid.uuid4(),
            email="user3@example.com",
            hashed_password="hashed_password_3",
            created_at=datetime.utcnow(),
        )
        session.add_all([user1, user2, user3])
        session.commit()

        # Create sample sessions
        session1 = Session(
            id=uuid.uuid4(),
            user_id=user1.id,
            token="token1",
            created_at=datetime.utcnow(),
            expires_at=datetime.utcnow() + timedelta(days=1),
        )
        session2 = Session(
            id=uuid.uuid4(),
            user_id=user2.id,
            token="token2",
            created_at=datetime.utcnow(),
            expires_at=datetime.utcnow() + timedelta(days=1),
        )
        session.add_all([session1, session2])
        session.commit()

        # Create sample documents
        document1 = Document(
            id=uuid.uuid4(),
            user_id=user1.id,
            session_id=session1.id,
            filename="file1.pdf",
            file_type="pdf",
            status="processed",
            uploaded_at=datetime.utcnow(),
            processed_at=datetime.utcnow(),
            error_message=None,
        )
        document2 = Document(
            id=uuid.uuid4(),
            user_id=user2.id,
            session_id=session2.id,
            filename="file2.docx",
            file_type="docx",
            status="error",
            uploaded_at=datetime.utcnow(),
            processed_at=None,
            error_message="File format not supported",
        )
        session.add_all([document1, document2])
        session.commit()

        # Create sample document chunks
        chunk1 = DocumentChunk(
            id=uuid.uuid4(),
            document_id=document1.id,
            user_id=user1.id,
            session_id=session1.id,
            chunk_index=0,
            chunk_text="Sample text chunk 1",
            embedding=[0.1] * 1536,
            created_at=datetime.utcnow(),
        )
        chunk2 = DocumentChunk(
            id=uuid.uuid4(),
            document_id=document1.id,
            user_id=user1.id,
            session_id=session1.id,
            chunk_index=1,
            chunk_text="Sample text chunk 2",
            embedding=[0.2] * 1536,
            created_at=datetime.utcnow(),
        )
        session.add_all([chunk1, chunk2])
        session.commit()

        # Create sample queries
        query1 = Query(
            id=uuid.uuid4(),
            user_id=user1.id,
            session_id=session1.id,
            question="What is the content of file1?",
            answer="Sample text chunk 1",
            created_at=datetime.utcnow(),
        )
        session.add(query1)
        session.commit()

        # Create sample query sources
        query_source1 = QuerySource(
            id=uuid.uuid4(),
            query_id=query1.id,
            chunk_id=chunk1.id,
            similarity_score=0.95,
        )
        session.add(query_source1)
        session.commit()

    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error seeding database: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    seed_database()
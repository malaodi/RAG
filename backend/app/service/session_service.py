from sqlalchemy.orm import Session
from sqlalchemy import select
from utils.database import get_db
from models.message import Message  # 确保路径正确
import uuid
from datetime import datetime

class SessionService:
    def __init__(self, db: Session):
        self.db = db

    def create_session(self, user_id: str):
        try:
            session_id = str(uuid.uuid4()).replace("-", "")[:16]
            start_time = datetime.now()

            # 插入会话记录
            self.db.execute(
                """
                INSERT INTO sessions (session_id, user_id, start_time)
                VALUES (:session_id, :user_id, :start_time)
                """,
                {"session_id": session_id, "user_id": user_id, "start_time": start_time}
            )
            self.db.commit()

            return {
                "session_id": session_id,
                "status": "success",
                "message": "Session created successfully"
            }
        except Exception as e:
            self.db.rollback()
            raise e

# 服务实例化
def get_session_service(db: Session = next(get_db())):
    return SessionService(db)




def get_chat_history_from_db(db: Session, session_id: str, limit: int = 5):
    try:
        stmt = (
            select(Message)
            .where(Message.session_id == session_id)
            .order_by(Message.created_at.desc()) # <--- 改成 created_at
            .limit(limit)
        )
        results = db.execute(stmt).scalars().all()

        # 数据库是倒序取的（最近的在前面），我们需要反转回正序（先说的在前面）
        results.reverse()

        chat_history = []
        for msg in results:
            chat_history.append({"role": "user", "content": msg.user_question})
            chat_history.append({"role": "assistant", "content": msg.model_answer})

        return chat_history
    except Exception as e:
        # 记录日志，这里假设你已经定义了 logger
        print(f"Error fetching chat history: {e}")
        return []
from sqlalchemy import Column, Integer, ForeignKey, DateTime, func, UniqueConstraint
from app.db.session import Base


class Follower(Base):
    __tablename__ = "followers"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE")) # which user is followed
    follower_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE")) # who follows that user
    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (UniqueConstraint('user_id', 'follower_id', name='unique_user_follower'),)
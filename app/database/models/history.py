from datetime import datetime
from database.session import Base

from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship


class History(Base):
    id = Column(Integer, primary_key=True, nullable=False)
    vps_id = Column(Integer, ForeignKey("vps.id", ondelete="CASCADE"), nullable=False)
    status = Column(String, nullable=False)
    data = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.now, nullable=False)

    vps = relationship("Vps", back_populates="history")
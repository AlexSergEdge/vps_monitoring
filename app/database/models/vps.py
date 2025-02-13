from datetime import datetime
from sqlalchemy import Column, Integer, Text, String, Boolean, DateTime

from database.session import Base
from sqlalchemy.orm import relationship


class Vps(Base):
    id = Column(Integer, primary_key=True, nullable=False)
    hostname = Column(String, nullable=False)
    ip_address = Column(String, nullable=False)
    ssh_port = Column(Integer, nullable=True)
    ssh_user = Column(String, nullable=True)
    ssh_public_key_path = Column(String, nullable=True)
    country = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now, nullable=False)

    history = relationship("History", back_populates="vps")

from datetime import datetime
from sqlalchemy import Column, Integer, Text, String, Boolean, DateTime

from database.session import Base
from sqlalchemy.orm import relationship


class Module(Base):
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)

    vpses = relationship('Vps', secondary='vpsmodule', back_populates='modules')
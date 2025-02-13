from datetime import datetime
from sqlalchemy import Column, Integer, Text, String, Boolean, DateTime, ForeignKey

from database.session import Base
from sqlalchemy.orm import relationship


class VpsModule(Base):
    id = Column(Integer, primary_key=True)

    vps_id = Column(Integer, ForeignKey('vps.id'))
    module_id = Column(Integer, ForeignKey('module.id'))
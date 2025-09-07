from database import Base, engine
from sqlalchemy import Column,Integer,String,Float


class ExpenseModel(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String) 
    amount = Column(Float)


Base.metadata.create_all(bind=engine)

    



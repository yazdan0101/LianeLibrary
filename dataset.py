import getpass
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
import datetime
from engine import engine


Base = declarative_base()

class Author(Base):
    __tablename__ = "authors"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    books = relationship("Book", back_populates="author")


class Book(Base):
    __tablename__ = "books"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    author_id = Column(Integer, ForeignKey("authors.id"), nullable=True)
    genre=Column(String(50),nullable=True)
    copies_total = Column(Integer, default=1)             
    copies_available = Column(Integer, default=1)
    publisher = Column(String(100), nullable=True)
    language = Column(String(50), nullable=True)
    author = relationship("Author", back_populates="books")
    loans = relationship("Loan", back_populates="book")
class Borrower(Base):
    __tablename__ = "borrowers"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False) 
    phone = Column(String(20), nullable=True)           
    membership_date = Column(Date, default=datetime.date.today) 
    address = Column(String(200), nullable=True)      
    loans = relationship("Loan", back_populates="borrower")


class Loan(Base):
    __tablename__ = "loans"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    borrower_id = Column(Integer, ForeignKey("borrowers.id"), nullable=False)
    loan_date = Column(Date, default=datetime.date.today)
    due_date=Column(Date, nullable=False)
    return_date = Column(Date, nullable=True)
    status = Column(String(20), default="On Loan")  # On Loan / Returned
    book = relationship("Book", back_populates="loans")
    borrower = relationship("Borrower", back_populates="loans")

Base.metadata.create_all(engine)

import os
import datetime
from engine import engine
from dataset import Book,Loan,Borrower,Author




class LibraryManagement:
    def __init__(self,session):
        self.session=session


    def search_book(self,book_title:str):
        return self.session.query(Book).filter_by(title=book_title).first()

    def auto_complete_books(self, input: str):
        """Return up to 5 books whose titles contain the input string."""
        return (
            self.session.query(Book)
            .filter(Book.title.ilike(f"%{input}%"))  # case-insensitive match
            .limit(5)
            .all()
        )
    
    def add_book(self,book_title:str,author_name:str,genre:str,publisher:str,language:str,copies_total=1):
        book = self.session.query(Book).filter_by(title=book_title).first()
        author = self.session.query(Author).filter_by(name=author_name).first()
        if not author:
            author = Author(name=author_name)
            self.session.add(author)
            self.session.commit()
        if not book:
            book = Book(
                title=book_title,
                author=author,
                genre=genre,
                publisher=publisher,
                copies_total=copies_total,
                copies_available=copies_total,
                language=language,
            )
  
            self.session.add(book)
            self.session.commit()
    
    def loan_book(
        self,
        borrower_name: str,
        borrower_email: str,
        book_title: str,
        borrowe_phone:str=None,
        borrowe_address:str=None,
        loan_days: int = 14  # default 2 weeks loan
    ):
    
        # --- Borrower ---
        borrower = self.session.query(Borrower).filter_by(email=borrower_email).first()
        if not borrower:
            borrower = Borrower(
                name=borrower_name,
                email=borrower_email,
                membership_date=datetime.date.today()
            )
            self.session.add(borrower)
            self.session.commit()
    
        # --- Check Book Availability ---
        book = self.session.query(Book).filter_by(title=book_title).first()
        if book.copies_available < 1:
            raise Exception(f"No copies available for '{book_title}'.")
    
        # --- Loan ---
        today = datetime.date.today()
        due_date = today + datetime.timedelta(days=loan_days)
    
        loan = Loan(
            book=book,
            borrower=borrower,
            loan_date=today,
            due_date=due_date,
            status="On Loan"
        )
        self.session.add(loan)

        book.copies_available -= 1
        self.session.commit()

    def return_book(self,book_title:str):
        book = self.session.query(Book).filter_by(title=book_title).first()
        book.copies_available +=1
        loan = session.query(Loan).filter_by(book_id=book.id).first()
        today = datetime.date.today()
        loan.return_date=today
        loan.status='Returned'
        session.commit()
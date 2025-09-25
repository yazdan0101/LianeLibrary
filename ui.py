import streamlit as st
from sqlalchemy.orm import sessionmaker
import datetime
from library_management import LibraryManagement
from engine import engine

Session = sessionmaker(bind=engine)
session = Session()
lib=LibraryManagement(session)

st.set_page_config(page_title="📚 Library Management", layout="wide")
st.title("📚 Library Management System")

# Sidebar for navigation
menu = st.sidebar.radio("Choose Action", ["Search Book", "Add Book", "Loan Book", "Return Book"])


# --- Search Book ---
if menu == "Search Book":
    st.header("🔎 Search for a Book")
    book_title = st.text_input("Enter book title")
    if st.button("Search"):
        result = lib.search_book(book_title)
        if result:
            st.success(f"✅ Found: {result.title} by {result.author.name} ({result.language})")
            st.write(f"**Genre:** {result.genre}")
            st.write(f"**Publisher:** {result.publisher}")
            st.write(f"**Copies Available:** {result.copies_available}/{result.copies_total}")
        else:
            st.error("❌ Book not found.")


# --- Add Book ---
elif menu == "Add Book":
    st.header("➕ Add a New Book")

    with st.form("add_book_form"):
        book_title = st.text_input("Book Title")
        author_name = st.text_input("Author Name")
        genre = st.text_input("Genre")
        publisher = st.text_input("Publisher")
        language = st.text_input("Language")
        copies_total = st.number_input("Total Copies", min_value=1, value=1)

        submitted = st.form_submit_button("Add Book")
        if submitted:
            lib.add_book(book_title, author_name, genre, publisher, language, copies_total)
            st.toast(f"✅ Book added successfully.")


# --- Loan Book ---
elif menu == "Loan Book":
    st.header("📖 Loan a Book")

    with st.form("loan_book_form"):
        borrower_name = st.text_input("Borrower Name")
        borrower_email = st.text_input("Borrower Email")
        borrower_phone = st.text_input("Borrower Phone (optional)")
        borrower_address = st.text_area("Borrower Address (optional)")
        book_title = st.text_input("Book Title")
        loan_days = st.number_input("Loan Days", min_value=1, value=14)

        submitted = st.form_submit_button("Loan Book")
        if submitted:
            try:
                lib.loan_book(
                    borrower_name,
                    borrower_email,
                    book_title,
                    borrower_phone,
                    borrower_address,
                    loan_days
                )
                st.toast(f"✅ Book have been loaned successfully.")
            except Exception as e:
                st.toast(f"❌ {str(e)}")

# --- Return Book ---
elif menu == "Return Book":
    st.header("📦 Return a Book")

    book_title = st.text_input("Enter Book Title to Return")
    if st.button("Return Book"):
        try:
            lib.return_book(book_title)
            st.toast(f"✅ Book Returend successfully.")
        except Exception as e:
            st.toast(f"❌ {str(e)}")

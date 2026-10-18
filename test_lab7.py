import book
import pytest
import library
import user

@pytest.mark.system
def test_borrow_book():
    book1 = book.Book('Orgullo y prejuicio', 'Tenoch Moreno', 2026, 'ISBN001', )
    assert book1.title == 'Orgullo y prejuicio'
    book1.borrow()
    assert book1.borrowed == True

@pytest.mark.system
def test_borrow_two_times_book():
    book1 = book.Book('Orgullo y prejuicio', 'Tenoch Moreno', 2026, 'ISBN001', )
    assert book1.title == 'Orgullo y prejuicio'
    book1.borrow()
    assert book1.borrowed == True
    with pytest.raises(ValueError,match=" The book is already borrowed"):
        book1.borrow()

@pytest.mark.system
def test_return_book():
    book1 = book.Book('Orgullo y prejuicio', 'Tenoch Moreno', 2026, 'ISBN001', )
    assert book1.title == 'Orgullo y prejuicio'
    book1.borrow()
    assert book1.borrowed == True
    book1.return_book()
    assert book1.borrowed == False

@pytest.mark.unit
def test_borrow_and_try_except():#no funciono por try except  
    book1 = book.Book('Orgullo y prejuicio', 'Tenoch Moreno', 2026, 'ISBN001', )
    assert book1.title == 'Orgullo y prejuicio'
    book1.borrow()
    assert book1.borrowed == True
    with pytest.raises(ValueError,match=" The book is already borrowed"):
        book1.borrow()

@pytest.fixture
def lib_init():
    lib= library.Library()
    book_tenoch = book.Book('orgullo y prejuicio', 'tenoch m', 2026, 'ISBN001')
    lib.add_book(book_tenoch)
    Tenoch = user.User('Tenoch', 'ID0001')
    lib.add_user(Tenoch)
    return lib

@pytest.mark.system
def test_library_init(lib_init):
    lib= lib_init
    lib.borrow_book('ID0001', 'ISBN001')

    assert lib.books[0].borrowed == True

@pytest.mark.wip
def test_library_init_ID_not_registered(lib_init):
    lib= lib_init

    with pytest.raises(ValueError, match= 'User not found'):
        lib.borrow_book('ID0003', 'ISBN001')
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
    with pytest.raises(ValueError,match="The book is already borrowed"):
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
    with pytest.raises(ValueError,match="The book is already borrowed"):
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

@pytest.mark.unit
def test_loans_disabled(monkeypatch, lib_init, capsys):
    monkeypatch.setattr(library, 'settings',{'loans_enabled': False})
    lib = lib_init
    lib.borrow_book('ID0001', 'ISBN001')
    captured = capsys.readouterr()
    assert 'Loans are disabled' in captured.out
    assert lib.books[0].borrowed == False

@pytest.mark.unit
def test_book_without_borrow_method(monkeypatch):
    book1 = book.Book('Libro','Autor', 2025,'ISBN010')
    monkeypatch.delattr(book.Book, 'borrow')
    with pytest.raises(AttributeError):
        book1.borrow()

@pytest.mark.unit
def test_borrow_with_try_except():
    book1 = book.Book('Orgullo y prejuicio', 'Tenoch Moreno', 2026, 'ISBN001')
    book1.borrow()
    try:
        book1.borrow()
    except ValueError as error:
        assert str(error) == 'The book is already borrowed'
    else:
        assert False, 'Se esperaba un ValueError'

@pytest.mark.unit
@pytest.mark.parametrize(
    'title, author, year, isbn',
    [
        ('Libro 1', 'Autor 1', 2024, 'ISBN001'),
        ('Libro 2', 'Autor 2', 2025, 'ISBN002'),
        ('Libro 3', 'Autor 3', 2026, 'ISBN003')
    ]
)
def test_book_initialization(title, author, year, isbn):
    book1 = book.Book(title, author, year, isbn)
    assert book1.title == title
    assert book1.author == author
    assert book1.year == year
    assert book1.isbn == isbn
    assert book1.borrowed == False

@pytest.mark.unit
def test_return_book_not_borrowed():
    book1 = book.Book('Libro', 'Autor', 2025, 'ISBN010')
    with pytest.raises(
        ValueError,
        match='The book is not currently borrowed'
    ):
        book1.return_book()
import book
import pytest
import library
import user

# PRUEBA 1: Préstamo correcto de un libro.
# Tema: marcadores
@pytest.mark.system
def test_borrow_book():
    book1 = book.Book('Orgullo y prejuicio', 'Tenoch Moreno', 2026, 'ISBN001', )
    assert book1.title == 'Orgullo y prejuicio'
    book1.borrow()
    assert book1.borrowed == True

# PRUEBA 2: Intentar prestar dos veces el mismo libro.
# Tema: pytest.raises
@pytest.mark.system
def test_borrow_two_times_book():
    book1 = book.Book('Orgullo y prejuicio', 'Tenoch Moreno', 2026, 'ISBN001', )
    assert book1.title == 'Orgullo y prejuicio'
    book1.borrow()
    assert book1.borrowed == True
    with pytest.raises(ValueError,match="The book is already borrowed"):
        book1.borrow()

# PRUEBA 3: Devolver un libro que se encuentra prestado.
# Tema: marcadores
@pytest.mark.system
def test_return_book():
    book1 = book.Book('Orgullo y prejuicio', 'Tenoch Moreno', 2026, 'ISBN001', )
    assert book1.title == 'Orgullo y prejuicio'
    book1.borrow()
    assert book1.borrowed == True
    book1.return_book()
    assert book1.borrowed == False

# PRUEBA 4: Volver a prestar un libro que ya está prestado.
# Tema: marcador unit y pytest.raises.
@pytest.mark.unit
def test_borrow_and_try_except():#no funciono por try except  
    book1 = book.Book('Orgullo y prejuicio', 'Tenoch Moreno', 2026, 'ISBN001', )
    assert book1.title == 'Orgullo y prejuicio'
    book1.borrow()
    assert book1.borrowed == True
    with pytest.raises(ValueError,match="The book is already borrowed"):
        book1.borrow()

# PRUEBA 5: Preparar una biblioteca para reutilizarla en otras pruebas.
# Tema: Fixture.
@pytest.fixture
def lib_init():
    lib= library.Library()
    book_tenoch = book.Book('orgullo y prejuicio', 'tenoch m', 2026, 'ISBN001')
    lib.add_book(book_tenoch)
    Tenoch = user.User('Tenoch', 'ID0001')
    lib.add_user(Tenoch)
    return lib

# PRUEBA 6: Pedir prestado un libro mediante la biblioteca.
# Tema: uso de la Fixture
@pytest.mark.system
def test_library_init(lib_init):
    lib= lib_init
    lib.borrow_book('ID0001', 'ISBN001')

    assert lib.books[0].borrowed == True

# PRUEBA 7: Intentar pedir un libro con un usuario no registrado.
# Tema: pytest.raises
@pytest.mark.wip
def test_library_init_ID_not_registered(lib_init):
    lib= lib_init

    with pytest.raises(ValueError, match= 'User not found'):
        lib.borrow_book('ID0003', 'ISBN001')

# PRUEBA 8: Intentar prestar un libro cuando los préstamos están deshabilitados.
# Temas: monkeypatch.setattr y capsys
@pytest.mark.unit
def test_loans_disabled(monkeypatch, lib_init, capsys):
    monkeypatch.setattr(library, 'settings',{'loans_enabled': False})
    lib = lib_init
    lib.borrow_book('ID0001', 'ISBN001')
    captured = capsys.readouterr()
    assert 'Loans are disabled' in captured.out
    assert lib.books[0].borrowed == False

# PRUEBA 9: Simular que la clase Book no tiene el método borrow.
# Tema: monkeypatch.delattr y raises
@pytest.mark.unit
def test_book_without_borrow_method(monkeypatch):
    book1 = book.Book('Libro','Autor', 2025,'ISBN010')
    monkeypatch.delattr(book.Book, 'borrow')
    with pytest.raises(AttributeError):
        book1.borrow()

# PRUEBA 10: Capturar y comprobar una excepción usando try-except.
# Tema: try, except y else.
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

# PRUEBA 11: Comprobar la creación de libros con diferentes datos.
# Tema: pytest.mark.parametrize
@pytest.mark.unit
@pytest.mark.parametrize(
    'title, author, year, isbn',
    [
        ('Libro 1', 'Autor 1', 2024, 'ISBN001'),
        ('Libro 2', 'Autor 2', 2025, 'ISBN002'),
        ('Libro 3', 'Autor 3', 2026, 'ISBN003'),
        ('Libro 4', 'Autor 4', 2027, 'ISBN005')
    ]
)
def test_book_initialization(title, author, year, isbn):
    book1 = book.Book(title, author, year, isbn)
    assert book1.title == title
    assert book1.author == author
    assert book1.year == year
    assert book1.isbn == isbn
    assert book1.borrowed == False

# PRUEBA 12: Intentar devolver un libro que nunca se prestó.
# Tema: pytest.raises y cobertura de decisiones de return_book().
@pytest.mark.unit
def test_return_book_not_borrowed():
    book1 = book.Book('Libro', 'Autor', 2025, 'ISBN010')
    with pytest.raises(
        ValueError,
        match='The book is not currently borrowed'
    ):
        book1.return_book()

# Tema: monkeypatch.setitem()
@pytest.mark.unit
def test_loans_disabled_setitem(monkeypatch, lib_init, capsys):
    monkeypatch.setitem(
        library.settings,
        'loans_enabled',
        False
    )

    lib = lib_init
    lib.borrow_book('ID0001', 'ISBN001')

    captured = capsys.readouterr()

    assert 'Loans are disabled' in captured.out
    assert lib.books[0].borrowed == False
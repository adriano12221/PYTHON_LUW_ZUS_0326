from biblioteka import Book, Library
from czytelnik import Reader


def main():
    book1 = Book("Clean Code", "Robert Martin", 2008)
    book2 = Book("Python Tricks", "Dan Bader", 2017)

    library = Library("Central Library")
    library.add_book(book1)
    library.add_book(book2)

    reader1 = Reader("Jan", "Kowalski", "Warszawa", "Marszałkowska 10", "00-001")
    reader2 = Reader("Anna", "Nowak", "Kraków", "Długa 5", "30-001")

    # Jan wypożycza Clean Code
    ok = reader1.borrow_book(book1)
    print("Jan wypożycza Clean Code:", "OK" if ok else "NIE")

    # Anna próbuje wypożyczyć tę samą książkę (ma się nie udać)
    ok = reader2.borrow_book(book1)
    print("Anna wypożycza Clean Code:", "OK" if ok else "NIE (już wypożyczona)")

    # Stan biblioteki
    library.list_books()

    # Listy wypożyczeń
    reader1.list_borrowed_books()
    reader2.list_borrowed_books()

    # Jan oddaje książkę
    ok = reader1.return_book(book1)
    print("\nJan oddaje Clean Code:", "OK" if ok else "NIE")

    # Anna próbuje ponownie (teraz ma się udać)
    ok = reader2.borrow_book(book1)
    print("Anna wypożycza Clean Code po zwrocie:", "OK" if ok else "NIE")

    library.list_books()
    reader1.list_borrowed_books()
    reader2.list_borrowed_books()


if __name__ == "__main__":
    main()

from biblioteka import Book, Library
from czytelnik import Reader


def main():

    # --- tworzymy książki ---
    book1 = Book("Clean Code", "Robert Martin", 2008)
    book2 = Book("Python Tricks", "Dan Bader", 2017)
    book3 = Book("Fluent Python", "Luciano Ramalho", 2015)

    # --- tworzymy bibliotekę ---
    library = Library("Central Library")

    # --- agregacja: dodajemy książki do biblioteki ---
    library.add_book(book1)
    library.add_book(book2)
    library.add_book(book3)

    # --- tworzymy czytelnika (kompozycja Address w Reader) ---
    reader = Reader(
        "Jan",
        "Kowalski",
        "Warszawa",
        "Marszałkowska 10",
        "00-001"
    )

    # --- wyświetlenie danych ---
    print(reader)

    # --- lista książek ---
    library.list_books()


if __name__ == "__main__":
    main()

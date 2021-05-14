"""
    Sort books by title, authors, or copyright date.
    create a Books class, with an attribute of a list of books
    the books will only live while the program is running 
"""
class Book:
    def __init__(self):
        self._title = ''
        self._authors = list()
        self._ISBN = ''
        self._publisher = ''
        self._copyright = ''
        self._categories = list()
    
    @property
    def title(self):
        return self._title

    def fillListEntry(self,key):
        anotherKey = True
        inputs = list()
        while anotherKey:
            inputs.append(input(f'Enter {key}: '))
            anotherKey = askAgain(f'Do you want to enter another {key}?')
        return inputs

    def collectBookInformation(self):
        self._title = input('Enter title: ')
        self._authors = self.fillListEntry('author')
        self._ISBN = input('Enter ISBN: ')
        self._publisher = input('Enter publisher: ')
        self._copyright = input('Enter copyright: ')
        self._categories = self.fillListEntry('category')

    def convertToDictionary(self):
        return {
            'title': self._title,
            'authors': self._authors,
            'ISBN': self._ISBN,
            'publisher': self._publisher,
            'copyright': self._copyright,
            'categories': self._categories,
        }

class BookList:
    def __init__(self):
        self._book_list = list()

    @property
    def book_list(self):
        return self._book_list

    def append_book(self, book):
        self._book_list.append(book)

    def remove_book(self, book):
        self._book_list.pop(book)

    def save_book_list(self, format):
         #Sort books by title
        self._book_list.sort(key=lambda x: x.title, reverse=False)

        # Write each book data to file
        for book in self._book_list:
            FormatFactory.save_book_as(book, format)


from enum import Enum
class Formats(Enum):
    JSON = 1
    YAML = 2
    XML = 3

from abc import ABC, abstractmethod
class IFormat(ABC):
    @abstractmethod
    def write_to_text_file():
        """ Interface method """

class JSON(IFormat):
    def write_to_text_file(self, book):
        import json
        bookData = book.convertToDictionary()
        with open('savedBooks.txt', 'a+') as f:
            f.write('JSON format ' + '-'*10 + '\n')
            json.dump(bookData, f, indent=4, sort_keys=True)
            f.write('\n\n')

class YAML(IFormat):
    def write_to_text_file(self,book):
        import yaml
        bookData = book.convertToDictionary()
        with open('savedBooks.txt ', 'a+') as f:
            f.write('YAML format' + '-'*10 + '\n')
            yaml.dump(bookData, f)
            f.write('\n\n')
        

class XML(IFormat):
    def write_to_text_file(self,book):
        import xml.etree.ElementTree as ET
        bookData = book.convertToDictionary()

        root = ET.Element('root')
        title = ET.SubElement(root, 'title').text = bookData['title']

        authors = ET.SubElement(root, 'authors')
        for i in bookData['authors']:
            ET.SubElement(authors, "element").text = i

        ISBN = ET.SubElement(root, 'ISBN').text = bookData['ISBN']
        publisher = ET.SubElement(root, 'publisher').text = bookData['publisher']
        copyright = ET.SubElement(root, 'copyright').text = bookData['copyright']

        categories = ET.SubElement(root, 'categories')
        for i in bookData['categories']:
            ET.SubElement(categories, "element").text = i
        
        with open('savedBooks.txt', 'a+') as f:
            f.write('XML format ' + '-'*10 + '\n')
            f.write(XML.prettify(root))
            f.write('\n\n')

    @staticmethod
    def prettify(elem):
        """ Return a pretty-printed XML string for the element (normally "root") """
        import xml.etree.ElementTree as ET
        from xml.dom import minidom

        rough_string = ET.tostring(elem, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="\t")
    

class FormatFactory:
    @staticmethod
    def save_book_as(book, format_type):
        if format_type == 'JSON':
            return JSON().write_to_text_file(book)
        elif format_type == 'YAML':
            return YAML().write_to_text_file(book)
        elif format_type == 'XML':
            return XML().write_to_text_file(book)

def askAgain(question):
    answer = input(f'{question} (y/n): ')
    while answer.lower() != 'y' and answer.lower() != 'n':
        print("Please provide either 'y' or 'n'.")
        answer = input(f'{question} (y/n): ')
    if answer.lower() == 'y': return True
    else: return False

def selectFormatType():
    format_type = ''
    format_selected = False
    while not format_selected:
        print(f'Select the format you want to save the books in:', end=' ')
        formats = [ i.name for i in Formats ]
        for i in formats:
            print(i, end=' ')
        format_type = input('\nSelection> ')
        if format_type.upper() not in formats:
            print('Incorrect format')
        else:
            format_selected = True
    return format_type.upper()

def main():
    book_list = BookList()
    anotherBook = True
    while anotherBook:
        book = Book()
        book.collectBookInformation()
        save = askAgain('Would you like to save the entered information?')
        if save: 
            book_list.append_book(book)

        anotherBook = askAgain('Do you want to save another book?')

    format = selectFormatType()
    book_list.save_book_list(format) # book list sorted by title


    print('Bye!')

if __name__ == '__main__':
    main()





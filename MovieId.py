from bs4 import BeautifulSoup


class MovieId:
    def __init__(self, name: str):
        if len(name) != 9:
            raise ValueError('The input name has to consist of 9 characters')
        if not (name[0] == 't' and name[1] == 't'):
            raise ValueError('The first two characters have to be tt...')
        self.name = name


def fetch_rating(movie: MovieId):
    """
    Looks up the actual ration on imdb.com
    :param movie:
    """


def download_content(url: str) -> str:
    from urllib.request import Request, urlopen
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    resource = urlopen(req)
    html = resource.read().decode(resource.headers.get_content_charset())
    soup = BeautifulSoup(html, 'lxml')
    for script in soup(["script"]):
        script.extract()
    return soup.prettify()


def save_to_file(url: str, filename: str) -> None:
    file = open(get_full_path(filename), 'w')
    file.write(download_content(url))


def get_full_path(filename) -> str:
    if not filename.lower().endswith(".txt"):
        raise TypeError("The input fileName has to have a .txt ending")
    from os import path
    return path.join(r'C:\PythonTemp', filename)


def load_from_file(filename: str) -> str:
    """
    Looks up the html code in the buffered file.
    :param filename: file, that should be opened
    :return: returns a string containing the html code
    """
    file = open(get_full_path(filename), 'r')
    return file.read()


import unittest


class TestMovieId(unittest.TestCase):
    def test_tooShortId(self):
        with self.assertRaises(ValueError):
            MovieId("tooShort")
    def test_doesNotStartWithTT(self):
        with self.assertRaises(ValueError) as eMessage:
            MovieId("123456789")
        exceptionMessage = eMessage.exception
        self.assertEqual(eMessage.exception.args[0], "The first two characters have to be tt...")
    def test_withWorkingInputs(self):
        id = MovieId("tt1234567")
        self.assertEqual(id.name, "tt1234567")



if __name__ == "__main__":
    unittest.main()

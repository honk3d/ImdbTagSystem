from bs4 import BeautifulSoup, Tag
from MovieId import download_content


def build_link(page: int) -> str:
    return "http://www.movie-blog.org/category/hd/page/" + str(page) + "/"


def list_entries(rawHtml: str):
    soupContent = BeautifulSoup(rawHtml, 'lxml')
    for image in soupContent(["img"]):
        image.extract()
    for frame in soupContent(["iframe"]):
        frame.extract()
    return soupContent.find_all("div", {"class": "beitrag2"})


def get_date(result: Tag) -> str:
    try:
        return result.find("p", {"class": "date_x"}).text.strip()
    except:
        return ""


def get_title(result: Tag) -> str:
    try:
        return result.h1.a.text.strip()
    except:
        return ""


def get_movie_blog_link(result: Tag) -> str:
    try:
        return result.h1.a["href"]
    except:
        return ""


def get_imdb_link(result: Tag) -> str:
    try:
        for textBlock in result(["p"]):
            for link in textBlock(["a"]):
                if "imdb.com" in link["href"]:
                    return link["href"]
    except:
        return ""


def get_imdb_rating(result: Tag) -> str:
    try:
        for textBlock in result(["p"]):
            for link in textBlock(["a"]):
                if "imdb.com" in link["href"]:
                    return link.text.strip()
    except:
        return ""


def get_num_rating(rating: str) -> float:
    try:
        rating = rating.lower()
        rating = rating.replace("/10","")
        rating = rating.replace("imdb","")
        rating = rating.replace(":","")
        rating = rating.replace(",",".")
        rating = rating.strip()
        return float(rating)
    except:
        return 0


class MovieBlockEntry:
    def __init__(self, result: Tag):
        self.date = get_date(result)
        self.name = get_title(result)
        self.linkImdb = get_imdb_link(result)
        self.rating = get_imdb_rating(result)
        self.numRating = get_num_rating(self.rating)
        self.link = get_movie_blog_link(result)


def get_entries(page: int) -> MovieBlockEntry:
    result = []
    for rawContent in list_entries(download_content(build_link(page))):
        result.append(MovieBlockEntry(rawContent))
    return result


def look_up_links(pages: int):
    result = []
    for i in range(pages):
        tempList = get_entries(i)
        print("page " + str(i) + " of " + str(pages) + " pages done.")
        for movie in tempList:
            result.append(movie)

    output = []
    for movie in result:
        if movie.numRating > 8:
            output.append(movie)
    return output



results = look_up_links(10)

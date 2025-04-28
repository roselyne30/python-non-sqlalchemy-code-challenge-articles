class Author:
    def __init__(self, name):
        if not isinstance(name, str):
            raise Exception("Author name must be a string.")
        if len(name) == 0:
            raise Exception("Author name must be longer than 0 characters.")
        self._name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        # Ignore change to name, make it immutable
        pass

    def articles(self):
        return [article for article in Article.all if article.author == self]

    def magazines(self):
        magazines = list({article.magazine for article in self.articles()})
        return magazines if magazines else None

    def add_article(self, magazine, title):
        return Article(self, magazine, title)

    def topic_areas(self):
        topics = list({article.magazine.category for article in self.articles()})
        return topics if topics else None


class Magazine:
    all_magazines = []

    def __init__(self, name, category):
        if not isinstance(name, str) or not (2 <= len(name) <= 16):
            raise Exception("Magazine name must be a string between 2 and 16 characters.")
        if not isinstance(category, str) or len(category) == 0:
            raise Exception("Magazine category must be a non-empty string.")
        
        self._name = name
        self._category = category
        Magazine.all_magazines.append(self)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if isinstance(value, str) and 2 <= len(value) <= 16:
            self._name = value
        # if invalid input, just ignore and do nothing

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if isinstance(value, str) and len(value) > 0:
            self._category = value
        # if invalid input, just ignore and do nothing

    def articles(self):
        articles = [article for article in Article.all if article.magazine == self]
        return articles if articles else None

    def contributors(self):
        authors = list({article.author for article in Article.all if article.magazine == self})
        return authors if authors else None

    def article_titles(self):
        titles = [article.title for article in Article.all if article.magazine == self]
        return titles if titles else None

    def contributing_authors(self):
        authors = []
        for author in self.contributors() or []:
            count = sum(1 for article in Article.all if article.magazine == self and article.author == author)
            if count > 2:
                authors.append(author)
        return authors if authors else None

    @classmethod
    def top_publisher(cls):
        if not Article.all:
            return None
        magazine_articles = {magazine: len([article for article in Article.all if article.magazine == magazine]) for magazine in cls.all_magazines}
        return max(magazine_articles, key=magazine_articles.get) if magazine_articles else None


class Article:
    all = []

    def __init__(self, author, magazine, title):
        if not isinstance(author, Author):
            raise Exception("Author must be an instance of Author.")
        if not isinstance(magazine, Magazine):
            raise Exception("Magazine must be an instance of Magazine.")
        if not isinstance(title, str):
            raise Exception("Title must be a string.")
        if len(title) < 5 or len(title) > 50:
            raise Exception("Title must be between 5 and 50 characters.")
        
        self._title = title
        self.author = author
        self.magazine = magazine
        Article.all.append(self)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        # Ignore attempts to change the title
        pass

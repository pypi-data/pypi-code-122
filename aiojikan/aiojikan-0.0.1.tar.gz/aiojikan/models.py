"""
Copyright (c) 2022 Ben

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


from typing import Dict, List, Optional
from datetime import datetime


class Anime:
    """
    Anime Data Class

    Attributes
    ----------
    mal_id: str
        The myanimelist id given to the anime


    Methods
    -------
    """

    def __init__(self, data: dict) -> None:
        """
        Init

        data: dict
            Create the object using the given data
        """
        self.mal_id: str = data.get("mal_id")
        self.url: str = data.get("url")
        self.images: Optional[Dict[str, Image]] = {}
        if data.get("images"):
            for image, image_data in data.get("images").items():
                self.images[image] = Image(image_data)
        self.trailer: Trailer = Trailer(data.get("trailer"))
        self.title: str = data.get("title")
        self.title_english: str = data.get("title_english")
        self.title_japanese: str = data.get("title_japanese")
        self.title_synonyms: List[str] = data.get("title_synonyms")
        self.type: str = data.get("type")
        self.source: str = data.get("source")
        self.episodes: int = data.get("episodes")
        self.status: str = data.get("status")
        self.airing: bool = data.get("airing")
        self.aired: TimeFrame = TimeFrame(data.get("aired"))
        self.duration: str = data.get("duration")
        self.rating: str = data.get("rating")
        self.score: float = data.get("score")
        self.scored_by: int = data.get("scored_by")
        self.rank: int = data.get("rank")
        self.popularity: int = data.get("popularity")
        self.members: int = data.get("members")
        self.favorites: int = data.get("favorites")
        self.synopsis: str = data.get("synopsis")
        self.background: Optional[str] = data.get("background")
        self.season: str = data.get("season")
        self.year: int = data.get("year")
        self.broadcast: Broadcast = Broadcast(data.get("broadcast"))
        self.producers: Optional[List[Producer]] = []
        if data.get("producers"):
            for producer in data.get("producers"):
                self.producers.append(Producer(producer))
        self.licensors: List[Licensor] = []
        for licensor in data.get("licensors"):
            self.licensors.append(Licensor(licensor))
        self.studios: List[Studio] = []
        for studio in data.get("studios"):
            self.studios.append(Studio(studio))
        self.genres: List[Genre] = []
        for genre in data.get("genres"):
            self.genres.append(Genre(genre))
        self.explicit_genres: List[Genre] = []
        for explicit_genres in data.get("explicit_genres"):
            self.explicit_genres.append(Genre(explicit_genres))
        self.genres: List[Genre] = []
        for genre in data.get("genres"):
            self.genres.append(Genre(genre))
        self.explicit_genres: List[Genre] = []
        for explicit_genres in data.get("explicit_genres"):
            self.explicit_genres.append(Genre(explicit_genres))


class FullAnime(Anime):
    """
    An animes full data class
    """

    def __init__(self, data) -> None:
        """
        Init
        """
        super().__init__(data)
        self.themes: List[Theme] = []
        for theme in data.get("themes"):
            self.themes.append(Theme(theme))
        self.demographics: List[Demographic] = []
        for demographic in data.get("themes"):
            self.demographics.append(Demographic(demographic))
        self.relations: List[Relation] = []
        for relation in data.get("relations"):
            self.relations.append(Relation(relation))
        self.openings: List[str] = data.get("theme").get("openings")
        self.endings: List[str] = data.get("theme").get("endings")
        self.externals: List[External] = []
        for external in data.get("externals"):
            self.externals.append(External(external))


class TimeFrame:
    """
    Represents a timeframe that may be given
    """

    def __init__(self, data: dict) -> None:
        """
        Init

        data: dict
            Create the object using the given data
        """
        self.start: datetime = datetime.fromisoformat(data.get("from"))
        self.end: datetime = datetime.fromisoformat(data.get("to"))
        self.string: str = data.get("string")


class Trailer:
    """
    Trailer data class
    """

    def __init__(self, data: dict) -> None:
        """
        Init

        data: dict
            Create the object using the given data
        """
        self.youtube_id: str = data.get("youtube_id")
        self.url: str = data.get("url")
        self.embed_url: str = data.get("embed_url")
        self.images: Image = Image(data.get("images"))


class Broadcast:
    """
    Broadcast data class

    """

    def __init__(self, data: dict) -> None:
        """
        Init

        data: dict
            Create the object using the given data
        """
        self.day: str = data.get("data")
        self.time: str = data.get("time")
        self.timezone: str = data.get("timezone")
        self.tz = self.timezone
        self.string: str = data.get("string")


class MalData:
    """
    Many of the objects returned have 4 properties, mal_id, type, name and url, so we can just subclass this.
    """

    def __init__(self, data: dict) -> None:
        """
        Init

        data: dict
            Create the object using the given data
        """
        self.mal_id: int = data.get("mal_id")
        self.type: str = data.get("type")
        self.name: str = data.get("name")
        self.url: str = data.get("url")


class Producer(MalData):
    """
    Producer data class

    """

    def __init__(self, data: dict) -> None:
        """
        Init

        data: dict
            Create the object using the given data
        """
        super().__init__(data)


class Licensor(MalData):
    """
    Licensor data class

    """

    def __init__(self, data: dict) -> None:
        """
        Init

        data: dict
            Create the object using the given data
        """
        super().__init__(data)


class Studio(MalData):
    """
    Studio data class

    """

    def __init__(self, data: dict) -> None:
        """
        Init

        data: dict
            Create the object using the given data
        """
        super().__init__(data)


class Genre(MalData):
    """
    Genre data class

    """

    def __init__(self, data: dict) -> None:
        """
        Init

        data: dict
            Create the object using the given data
        """
        super().__init__(data)


class Theme(MalData):
    """
    Theme data class


    """

    def __init__(self, data: dict) -> None:
        """
        Init

        data: dict
            Create the object using the given data
        """
        super().__init__(data)


class Demographic(MalData):
    """
    Demographic data class


    """

    def __init__(self, data: dict) -> None:
        """
        Init

        data: dict
            Create the object using the given data
        """
        super().__init__(data)


class Relation:
    """
    Relation data class


    """

    def __init__(self, data: dict) -> None:
        """
        Init

        data: dict
            Create the object using the given data
        """
        super().__init__(data)
        self.relation = data.get("relation")
        self.entries: List[Entry] = []
        for entry in data.get("entries"):
            self.entries.append(Entry(entry))


class Entry:
    """
    Entry data class


    """

    def __init__(self, data: dict) -> None:
        """
        Init

        data: dict
            Create the object using the given data
        """
        super().__init__(data)


class External:
    """
    External Info Data Class

    """

    def __init__(self, data: dict) -> None:
        """
        Init
        """
        self.name: str = data.get("name")
        self.url: str = data.get("url")


class Image:
    """
    Data class for all images
    """

    def __init__(self, data: dict) -> None:
        """
        Init

        data: dict
            Create the object using the given data
        """
        self.img_type: str = data.get("image_url").split(".")[-1]
        self.image_url: str = data.get("image_url")
        self.small_image_url: str = data.get("small_image_url")
        self.large_image_url: str = data.get("large_image_url")
        self.medium_image_url: str = data.get("medium_image_url")
        self.maximum_image_url: str = data.get("maximum_image_url")

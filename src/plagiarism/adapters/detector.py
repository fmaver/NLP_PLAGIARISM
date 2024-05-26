from itertools import dropwhile

import spacy
from spacy import Language


class NameDetector:
    def __init__(
        self,
        nlp: Language = spacy.load("es_core_news_lg"),
        words_to_remove: list[str] | None = None,
        excluded_names: list[str] | None = None,
    ):
        self.nlp = nlp

        if words_to_remove is None:
            self.words_to_remove = [
                "LEGAJO",
                "ALUMNO",
                "ALUMNA",
                "ESTUDIANTE",
                "FECHA",
                "AYUDANTE",
                "SISTEMAS",
                "CARRERA",
                "EXPLIQUE",
                ".TXT",
                "EMAIL",
                "INDIQUE",
                "APELLIDO",
                "EJEMPLO",
                "LAIBINTRODUCCIÓN¿QUE",
            ]

        if excluded_names is None:
            self.excluded_names = [
                "Dr",
                "Ingeniero",
                "Ing",
                "Licenciado",
                "Lic",
                "MSc",
                "Mg",
                "Profesor",
                "Prof",
                "Borré",
                "Borre",
                "Hernán Borré",
                "Hernan Borré",
                "Hernán Borre",
                "Hernan Borre",
                "Maximiliano Bracho",
                "Alejandro Bracho",
                "Alejandro Prince",
                "Prince",
                "Anderson",
                "Newton",
            ]

    def find_out_author(self, page_text: str) -> str:
        """
        Finds out the author of the assignment.
        It supposes that the document contains a page with the author's name on it.

        Args:
            page_text: The first page of the assignment.

        Returns:
            str: The author's name.
        """
        page_text = page_text.replace("\n", " ")

        doc = self.nlp(page_text)

        names = [
            ent.text.title()
            for ent in doc.ents
            if (ent.label_ == "PER" and not any(name in ent.text for name in self.excluded_names))
        ]

        possible_name = next(dropwhile(lambda name: name == "UNKNOWN_AUTHOR", names), None)

        if not possible_name:
            return "UNKNOWN_AUTHOR"

        for noun in self.words_to_remove:
            possible_name = possible_name.upper().replace(noun, "").title()

        # if its empty, return UNKNOWN_AUTHOR
        if not possible_name.strip():
            return "UNKNOWN_AUTHOR"

        return possible_name.strip()

    def get_author(self, path: str, text: str) -> str:
        """
        Get the author of the document.

        Args:
            path: The path of the document.
            text: The text of the document.

        Returns:
            str: The author of the document.
        """
        author = self.find_out_author(path)
        if author == "UNKNOWN_AUTHOR":
            author = self.find_out_author(text)
        return author


class SentenceDetector:
    def __init__(self, nlp: Language = spacy.load("es_core_news_lg")):
        self.nlp = nlp

    def get_sentences(self, text: str) -> list[str]:
        """
        Get the sentences from the text.

        Args:
            text: The text to analyze.

        Returns:
            list[str]: The sentences of the text.
        """
        doc = self.nlp(text)
        return [sent.text for sent in doc.sents]

    def get_words(self, text: str) -> list[str]:
        """
        Get the words from the text.

        Args:
            text: The text to analyze.

        Returns:
            list[str]: The words of the text.
        """
        doc = self.nlp(text)
        return [token.text for token in doc]

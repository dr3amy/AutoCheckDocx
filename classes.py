import spacy


class Heading(object):
    """Класс для хранения раздела"""

    def __init__(self, head, type, content=[], parent=None):
        """Коснтруктор"""

        self.head = head
        self.type = type
        self.content = content
        self.parent = parent

    def __str__(self):
        return f"<{self.head}, '{self.type}', {self.content}>"

    def __repr__(self):
        return f"<{self.head}, '{self.type}', {self.content}>"


# class Model(object):
#     """Класс для хранения модели"""
#
#     def __init__(self, model_name):
#         self.md = spacy.load(model_name)
#
#     def nlp(self, text):
#         self.md.nlp(text)
#
#     def remove_stopwords_fast(self, text):
#         doc = self.md.nlp(text.lower())
#         result = [token.text for token in doc if token.text not in self.nlp.Defaults.stop_words]
#         return " ".join(result)


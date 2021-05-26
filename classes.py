class Heading(object):
    """Класс для хранения раздела"""

    def __init__(self, head, text_type, content=[], parent=None):
        """Коснтруктор"""

        self.head = head
        self.type = text_type
        self.content = content
        self.parent = parent

    def __str__(self):
        return f"<{self.head}, '{self.type}', {self.content}>"

    def __repr__(self):
        return f"<{self.head}, '{self.type}', {self.content}>"

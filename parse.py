from classes import *
import json


class Parser(object):
    def __init__(self, paragraphs=[], unwanted_chars=["\t"]):
        self.paragraphs = paragraphs
        self.unwanted_chars = unwanted_chars
        self.data = []

    def parse(self):
        """Функция парсинга документа"""

        level = 0
        curr_head = head = Heading("Main", "Main")
        for par in self.paragraphs:
            if par.text != "":
                par.text = ''.join([c for c in par.text if c not in self.unwanted_chars])
                if 'Normal' in par.style.name or 'List' in par.style.name:
                    curr_head.content.append(par.text)
                elif 'Heading' in par.style.name:
                    while int(par.style.name[-1]) <= level:
                        level -= 1
                        curr_head = curr_head.parent
                    curr_head.content.append(Heading(par.text, par.style.name, [], curr_head))
                    curr_head = curr_head.content[-1]
                    level += 1
        self.data = head.content
        return self.data

    @staticmethod
    def to_json(head):
        if isinstance(head, list):
            return list(map(Parser.to_json, head))
        elif isinstance(head, Heading):
            return {head.head: list(map(Parser.to_json, head.content))}
        else:
            return head

    def to_json_file(self, filename):
        with open(filename, mode='w', encoding='utf-8') as json_file:
            json.dump(Parser.to_json(self.data), json_file, indent=4, ensure_ascii=False)

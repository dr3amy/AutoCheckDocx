from functions import *
from processing import *
from parse import Parser


if __name__ == "__main__":
    filepath = ".\\Кафтанов_1_без_таблицы.docx"

    pattern = get_pattern('patterns\\right_pattern_1.json')
    print(pattern)
    doc = parse_doc(filepath, ".\\ParsedResults")
    print(doc, "\n")

    test_heads_path = "test\\test_headings_Кафтанов_1_без_таблицы.json"
    test_bodies_path = "test\\test_bodies_Кафтанов_1_без_таблицы.json"

    nlp = spacy.load('ru_core_news_lg')
    heads_check = check_headings(nlp, doc, pattern)
    print("~~~CHECKED HEADINGS~~~\n", heads_check, "\n")
    test_to_json(heads_check, test_heads_path)
    bodies_check = check_bodies(nlp, doc, pattern)
    print("~~~CHECKED BODIES~~~\n", bodies_check, "\n")
    test_to_json(bodies_check, test_bodies_path)

    print(calc_result(heads_check, bodies_check))

    # ПАРСИНГ ВСЕХ ФАЙЛОВ В ДИРЕКТОРИИ
    # paths = get_paths(".\\Тестовые документы_10шт\\1")
    # for path in paths:
    #     parse_doc(path, ".\\ParsedResults\\test_task_1")

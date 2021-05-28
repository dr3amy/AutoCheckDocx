from functions import *
from processing import *
from parse import Parser


if __name__ == "__main__":

    filepath = ".\\Кафтанов_1_без_таблицы.docx"
    # filepath = ".\\Чумаков_1_без_таблицы.docx"

    pattern = get_pattern('patterns\\right_pattern_1.json')
    print(pattern)
    doc = parse_doc(filepath, ".\\ParsedResults")
    print(doc, "\n")

    # nlp = spacy.load('ru_core_news_lg')
    # lst1 = [
    #     'Введение', 'Анализ рисков', 'Организация выполнения',
    #     'Необходимые ресурсы', 'Основные этапы и вехи',
    #     'Механизмы мониторинга и контроля', 'График работ'
    # ]
    # lst2 = [
    #     'Введение', 'Организация выполнения', 'Анализ рисков',
    #     'Необходимые ресурсы', 'Основные этапы и вехи',
    #     'График работ', 'Механизмы мониторинга и контроля'
    # ]

    test_heads_path = "test\\test_headings_Кафтанов_1_без_таблицы.json"
    test_bodies_path = "test\\test_bodies_Кафтанов_1_без_таблицы.json"
    # test_heads_path = "test\\test_headings_Чумаков_1_без_таблицы.json"
    # test_bodies_path = "test\\test_bodies_Чумаков_1_без_таблицы.json"

    # nlp = spacy.load('ru_core_news_lg')
    # heads_check = check_headings(nlp, doc, pattern)
    # print("~~~CHECKED HEADINGS~~~\n", heads_check, "\n")
    # test_to_json(heads_check, test_heads_path)
    # bodies_check = check_bodies(nlp, doc, pattern)
    # print("~~~CHECKED BODIES~~~\n", bodies_check, "\n")
    # test_to_json(bodies_check, test_bodies_path)

    heads_check = {
        'missing partitions': 0,
        'number of unordered partitions': 0,
        'Введение <-> Введение': 1.0,
        'Организация выполнения <-> Организация выполнения': 1.0,
        'Анализ рисков <-> Анализ рисков': 1.0,
        'Необходимые ресурсы <-> Необходимые ресурсы': 1.0,
        'Основные этапы и вехи <-> Основные этапы и вехи': 1.0,
        'График работ <-> График работ': 1.0,
        'Механизмы мониторинга и контроля <-> Механизмы мониторинга и контроля': 1.0
    }
    bodies_check = {
        'body #1': 1.0,
        'body #2': 0.35,
        'body #3': 0.22,
        'body #4': 0.28,
        'body #5': 0.0,
        'body #6': 0.2,
        'body #7': 0.1
    }
    res = calc_result(heads_check, bodies_check)
    print(res)

    # ПАРСИНГ ВСЕХ ФАЙЛОВ В ДИРЕКТОРИИ
    # paths = get_paths(".\\Тестовые документы_10шт\\1")
    # for path in paths:
    #     parse_doc(path, ".\\ParsedResults\\test_task_1")

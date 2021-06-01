from functions import *
from processing import *


if __name__ == "__main__":

    filepath = ".\\Кафтанов_1_без_таблицы.docx"
    pattern_path = "patterns\\right_pattern_1.json"
    pattern = get_pattern(pattern_path)
    doc = parse_doc(filepath, ".\\ParsedResults")

    test_heads_path = "test\\test_headings_Кафтанов_1_без_таблицы.json"
    test_bodies_path = "test\\test_bodies_Кафтанов_1_без_таблицы.json"

    nlp = spacy.load('ru_core_news_lg')
    heads_check = check_headings(nlp, doc, pattern)
    print("\nchecking partitions...")
    print("checked\n", heads_check)
    test_to_json(heads_check, test_heads_path)
    bodies_check = check_bodies(nlp, doc, pattern)
    print("\nchecking contents...")
    print("checked\n", bodies_check)
    test_to_json(bodies_check, test_bodies_path)

    result = calc_result(heads_check, bodies_check)
    print("similarity: ", result)
    result_file = ".\\Results" + filepath.split(".")[1] + ".txt"
    lines = [pattern_path.split("\\")[1], '\n', str(result)]
    with open(result_file, "w") as file:
        file.writelines(lines)

    # ПАРСИНГ ВСЕХ ФАЙЛОВ В ДИРЕКТОРИИ
    # paths = get_paths(".\\Тестовые документы_10шт\\1")
    # for path in paths:
    #     parse_doc(path, ".\\ParsedResults\\test_task_1")

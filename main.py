from functions import *
from processing import *
import argparse

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("folder", help="path to a folder with documents")
    arg_parser.add_argument("pattern", help="path to a pattern file")
    # arg_parser.add_argument("doc", help="path to a document file")
    args = arg_parser.parse_args()
    pattern = get_pattern(args.pattern)
    nlp = spacy.load('ru_core_news_lg')
    paths = get_paths(args.folder)
    results = []
    for path in paths:
        doc = parse_doc(path)

        heads_check = check_headings(nlp, doc, pattern)
        print("\nchecking section titles...")
        print("checked\n", heads_check)
        bodies_check = check_bodies(nlp, doc, pattern)
        print("\nchecking contents...")
        print("checked\n", bodies_check)

        result = calc_result(heads_check, bodies_check)
        print("similarity: ", result[1])
        json_result = {
            'pattern': args.pattern,
            'document': path,
            'similarity': result[1],
            'detailed info': result[0]
        }
        results.append(json_result)

    with open(args.folder + "\\results.json", 'w', encoding='utf-8') as outfile:
        json.dump(results, outfile, indent=4, ensure_ascii=False)

    # filepath = ".\\Кафтанов_1_без_таблицы.docx"
    # # filepath = ".\\Тестовые документы_10шт\\1\\Ideja_proekta_02.docx"
    # # filepath = ".\\Тестовые документы_10шт\\1\\Plan_proekta_01.docx"
    #
    # # test_heads_path = "test\\test_headings_Кафтанов_1_без_таблицы.json"
    # # test_bodies_path = "test\\test_bodies_Кафтанов_1_без_таблицы.json"
    #
    # test_heads_path = "test\\test_headings_" + filepath.split("\\")[-1].split(".")[0] + ".json"
    # test_bodies_path = "test\\test_bodies_" + filepath.split("\\")[-1].split(".")[0] + ".json"
    #
    # nlp = spacy.load('ru_core_news_lg')
    # heads_check = check_headings(nlp, doc, pattern)
    # print("\nchecking section titles...")
    # print("checked\n", heads_check)
    # test_to_json(heads_check, test_heads_path)
    # bodies_check = check_bodies(nlp, doc, pattern)
    # print("\nchecking contents...")
    # print("checked\n", bodies_check)
    # test_to_json(bodies_check, test_bodies_path)
    #
    # result = calc_result(heads_check, bodies_check)
    # print("similarity: ", str(int(result * 100)) + "%")
    # # result_file = ".\\Results" + filepath.split(".")[1] + ".txt"
    # result_file = ".\\Results\\test_results\\" + filepath.split("\\")[-1].split(".")[0] + ".txt"
    # lines = [pattern_path.split("\\")[1], '\n', str((int(result * 100))) + "%"]
    # with open(result_file, "w") as file:
    #     file.writelines(lines)

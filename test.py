from functions import *
from processing import *
from parse import Parser


# heads_check = {
#     'sections presence': 1.0,
#     'ordered sections': 1.0,
#     'Введение <-> Введение': 1.0,
#     'Организация выполнения <-> Организация выполнения': 1.0,
#     'Анализ рисков <-> Анализ рисков': 1.0,
#     'Необходимые ресурсы <-> Необходимые ресурсы': 1.0,
#     'Основные этапы и вехи <-> Основные этапы и вехи': 1.0,
#     'График работ <-> График работ': 1.0,
#     'Механизмы мониторинга и контроля <-> Механизмы мониторинга и контроля': 1.0
#     }
# bodies_check = {
#     'body #1': 0.1,
#     'body #2': 0.1,
#     'body #3': 0.1,
#     'body #4': 0.1,
#     'body #5': 0.1,
#     'body #6': 0.1,
#     'body #7': 0.1
# }
# res = calc_result(heads_check, bodies_check)
# print(res)

# test()
test_list = ["Введение", "Необходимые ресурсы", "Организация выполнения"]
sort_order = ["Введение", "Организация выполнения", "Анализ рисков", "Необходимые ресурсы"]
res = ["dummmy"] * len(sort_order)
# res = [elem for x in sort_order for elem in test_list if elem == x]

# for x in sort_order:
#     for elem in test_list:
#         if elem == x:
#             res[i] = elem
i = 0
for elem in test_list:
    i = sort_order.index(elem)
    res[i] = elem


print(test_list)
print(res)

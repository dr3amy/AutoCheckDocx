from classes import Heading
from operator import itemgetter
import spacy
import warnings
warnings.simplefilter("ignore")


def bodies_search(head):
    if isinstance(head, list):
        return list(map(bodies_search, head))
    elif isinstance(head, Heading):
        return list(map(bodies_search, head.content))
    else:
        return head


def reduce_list(lst):
    flat_list = []
    for sublist in lst:
        if isinstance(sublist, list):
            for item in sublist:
                flat_list.append(item)
    if len(flat_list) != 0:
        return flat_list
    else:
        return lst


def process_text(nlp, text):
    """Удаление стоп-слов, знаков пунктуации и пр."""

    doc = nlp(text.lower())
    result = []
    for token in doc:
        if token.text in nlp.Defaults.stop_words:
            continue
        if token.is_punct:
            continue
        if token.pos_ == 'VERB':
            continue
        if not token.has_vector:
            continue
        if token.lemma_ == '-PRON-':
            continue
        if token.lemma_ in result:
            continue
        if token.vector_norm:
            result.append(token.lemma_)
    return " ".join(result)


def process_doc(nlp, data, pattern):
    """Игнорирование разделов, которые не требуются в шаблоне"""

    # patt_headings = list(pattern.keys())
    fact_sections = []
    for head, patt in zip(data, pattern):
        if isinstance(head, Heading):
            # if head.head in patt_headings:
            #     fact_sections.append(head)
            if nlp(process_text(nlp, head.head)).similarity(nlp(process_text(nlp, patt))) != 0.0:
                fact_sections.append((head, patt))
    return fact_sections


def headings_sim(nlp, fact_headings, patt_headings):
    """Возвращает список лучших совпадений фактических разделов с разделами шаблона"""

    result = []
    for fact in fact_headings:
        sims = []
        nlp_fact = nlp(process_text(nlp, fact[0].head))
        for patt in patt_headings:
            nlp_patt = nlp(process_text(nlp, patt))
            sims.append((patt, round(nlp_fact.similarity(nlp_patt), 2)))
        result.append((fact[0].head,  max(sims, key=itemgetter(1))))
    return result


def check_headings(nlp, data, pattern):
    """Проверка заголовков на совпадение шаблону"""

    result = []
    patt_headings = list(pattern.keys())
    # оставляю только те разделы, которые присутствуют в шаблоне
    # ВАЖНО! в проверку на соответствие так же передаётся список без лишних заголовков
    # proc_data = process_doc(nlp, data, pattern)
    # fact_headings = [sect.head for sect in proc_data]
    fact_headings = process_doc(nlp, data, pattern)
    if len(fact_headings) > 0:
        present_headings = round(len(fact_headings) / len(patt_headings), 2)
    else:
        present_headings = 0
    result.append(("sections presence", present_headings))

    metric = 0
    # metric = 1.0
    transpositions = 0
    if len(fact_headings) > 1:
        p = 0
        q = 0
        for i in range(0, len(fact_headings) - 1):
            p = patt_headings.index(fact_headings[i][1])
            for j in range(i + 1, len(fact_headings)):
                q = patt_headings.index(fact_headings[j][1])
                if p > q:
                    transpositions += 1
        max_transpositions = len(fact_headings) * (len(fact_headings) - 1) / 2
        metric = 1 - transpositions / max_transpositions

    result.append(("sections order", round(metric, 2)))
    heads_sim = headings_sim(nlp, fact_headings, patt_headings)
    for pair in heads_sim:
        result.append((pair[0] + " <-> " + pair[1][0], pair[1][1]))

    return dict(result)


def order_sections(nlp, data, pattern):
    """Возвращает упорядоченный список разделов документа"""

    patt_headings = list(pattern.keys())
    proc_data = process_doc(nlp, data, pattern)
    ordered_data = ["dummy"] * len(patt_headings)
    for head in proc_data:
        ind = patt_headings.index(head[1])
        ordered_data[ind] = head[0]  # !!!!!!!!!!!!!
    return ordered_data


def check_bodies(nlp, data, pattern):
    """Проверка содержаний на совпадение шаблону"""

    result = []
    patt_bodies = list(pattern.values())
    ordered_data = order_sections(nlp, data, pattern)
    i = 0
    for section in ordered_data:
        f = False
        patt_lst = patt_bodies[i]
        if section != "dummy":
            body = reduce_list(bodies_search(section))  # из вложенных списков генерируется один общий
            for text in body:
                if f:
                    break
                proc_text = process_text(nlp, text)
                fact_lemmas = list(filter(None, [elem for elem in proc_text.split()]))
                similarities = []
                for patt in patt_lst:
                    if f:
                        break
                    for lem in fact_lemmas:
                        temp = process_text(nlp, patt)
                        sim = round(nlp(temp).similarity(nlp(lem)), 2)
                        similarities.append((temp + " <-> " + lem, sim))
                        if sim == 1.0:
                            f = True
                            break
                # print(f"body #{i+1}\n", similarities)
            if len(similarities) != 0:
                result.append((f"body #{i+1}", max(similarities, key=itemgetter(1))[1]))
            else:
                result.append((f"body #{i+1}", 0))
        i += 1
    return dict(result)


def test():
    nlp = spacy.load('ru_core_news_lg')

    # print(nlp.Defaults.stop_words)

    text1 = process_text(nlp, "Основные этапы и вехи")
    print(text1)
    text2 = process_text(nlp, "Этапы и вехи")
    print(text1, text2)

    doc1 = nlp(text1)
    doc2 = nlp(text2)
    # print(nlp.pipe_names)

    print(doc1.similarity(doc2))

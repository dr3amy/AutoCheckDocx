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


def headings_sim(nlp, fact_headings, patt_headings):
    """Возвращает список лучших совпадений фактических разделов с разделами шаблона"""

    result = []
    for fact in fact_headings:
        sims = []
        nlp_fact = nlp(process_text(nlp, fact))
        for patt in patt_headings:
            nlp_patt = nlp(process_text(nlp, patt))
            sims.append((patt, round(nlp_fact.similarity(nlp_patt), 2)))
        result.append((fact,  max(sims, key=itemgetter(1))))
    return result


def check_headings(nlp, data, pattern):
    """Проверка заголовков на совпадение шаблону"""

    result = []
    fact_headings = [elem.head for elem in data]
    patt_headings = list(pattern.keys())
    missing_headings = len(patt_headings) - len(fact_headings)
    result.append(("missing partitions", missing_headings))
    transpositions = 0
    for fact, patt in zip(fact_headings, patt_headings):
        if fact != patt:
            transpositions += 1
    result.append(("number of unordered partitions", int(transpositions/2)))
    heads_sim = headings_sim(nlp, fact_headings, patt_headings)
    for pair in heads_sim:
        result.append((pair[0] + " <-> " + pair[1][0], pair[1][1]))

    return dict(result)


def check_bodies(nlp, data, pattern):
    """Проверка содержаний на совпадение шаблону"""

    result = []
    patt_bodies = list(pattern.values())
    i = 0
    for head in data:
        # print(head)
        patt_lst = patt_bodies[i]
        body = reduce_list(bodies_search(head))  # из вложенных списков генерируется один общий
        # print(body)
        for text in body:
            proc_text = process_text(nlp, text)
            fact_lemmas = list(filter(None, [elem for elem in proc_text.split()]))
            similarities = []
            for patt in patt_lst:
                for lem in fact_lemmas:
                    temp = process_text(nlp, patt)
                    doc1 = nlp(temp)
                    doc2 = nlp(lem)
                    try:
                        similarities.append((temp + " <-> " + lem, round(doc1.similarity(doc2), 2)))
                    except UserWarning as uw:
                        print(f"{temp}, {lem}: {uw}")
            # print(f"body #{i+1}\n", similarities)
        result.append((f"body #{i+1}", max(similarities, key=itemgetter(1))[1]))
        i += 1
    return dict(result)


def test(data, pattern):
    nlp = spacy.load('ru_core_news_lg')
    headings = [key for key in pattern]
    bodies = [value for value in pattern]

    # print(nlp.Defaults.stop_words)

    text1 = process_text(nlp, "собрание")
    text2 = process_text(nlp, "этап")
    print(text1, text2)

    doc1 = nlp(text1)
    doc2 = nlp(text2)
    # print(nlp.pipe_names)

    print(doc1.similarity(doc2))

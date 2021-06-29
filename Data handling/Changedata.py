import json
import random

random.seed()

resource_file = open('files/resources.txt', 'w')
trainset_file = open('files/trainset.txt', 'w')
devset_file = open('files/devset.txt', 'w')

with open(
        'concept_dict_mini') as json_data:
    dict_csk = json.load(json_data)
with open('stopwords') as json_data:
    stopwords_list = json.load(json_data)

csk_triples = []
csk_entities = []
dict_csk_triples = {}
dict_csk_entities = {}
for entity in dict_csk:
    for triple in dict_csk[entity]:
        csk_triples.append(triple)
        hrt = triple.split(', ')
        csk_entities += [hrt[0], hrt[2]]
csk_triples = list(set(csk_triples))
csk_entities = list(set(csk_entities))
for idx, t in enumerate(csk_triples):
    dict_csk_triples[t] = idx
for idx, t in enumerate(csk_entities):
    dict_csk_entities[t] = idx


def build_vocab(corpus):
    print("Creating vocabulary...")
    vocab = {}
    for i, pair in enumerate(corpus):
        if i % 1000 == 0:
            print("    processing line %d" % i)
        for token in pair[0] + pair[1]:
            if token in vocab:
                vocab[token] += 1
            else:
                vocab[token] = 1
    return vocab


def csk_list_given_message_response_pair(post, response):

    list_of_entities = []
    post_triple_dict = {}
    post_triples = []
    response_triples = []
    response_triple_dict = {}
    match_triples = []
    list_of_triples = []
    match_index = []
    for word in post:
        if stopwords_list.get(word, -1) == -1:
            if dict_csk.get(word, -1) != -1:
                if word not in post_triple_dict:
                    post_triple_dict[word] = len(list_of_triples) + 1
                    entity = []
                    for idx, triple in enumerate(dict_csk[word]):
                        hrt = triple.split(', ')
                        # if hrt[0] == word:
                        if word in hrt[0]:
                            entity.append(hrt[2])
                            if hrt[2] in response:
                                match_triples.append(triple)
                                response_triple_dict[hrt[2]] = [len(list_of_triples) + 1, idx, triple]
                            # elif hrt[2] == word:
                        elif word in hrt[2]:
                            entity.append(hrt[0])
                            if hrt[0] in response:
                                match_triples.append(triple)
                                response_triple_dict[hrt[0]] = [len(list_of_triples) + 1, idx, triple]
                    list_of_entities.append(entity)
                    list_of_triples.append(dict_csk[word])

    for word in post:
        if word in post_triple_dict:
            post_triples.append(post_triple_dict[word])
        else:
            post_triples.append(0)

    for word in response:
        if word in response_triple_dict:
            response_triples.append(response_triple_dict[word][2])
            match_index.append(response_triple_dict[word][:2])
        else:
            response_triples.append(-1)
            match_index.append([-1, -1])

    match_triples = list(set(match_triples))
    return list_of_entities, list_of_triples, match_triples, post_triples, response_triples, match_index


corpus = []

with open(
        'medsample.txt') as infile:
    rawlines = infile.readlines()
    random.shuffle(rawlines)
    # print(len(rawlines))
    resource = {'csk_triples': csk_triples, 'csk_entities': csk_entities, 'dict_csk_triples': dict_csk_triples,
                'dict_csk_entities': dict_csk_entities}
    # resource_file.write(resource)

    index = 0
    cnt = 0
    devset = []
    trainset = []
    for idx, line in enumerate(rawlines):
        if idx % 1000 == 0:
            print('processing line %d' % idx)
        d = {}
        post, response = line.strip().split('\t')
        post = post.split()
        response = response.split()
        # print(idx)
        # print(response)
        d['post'] = post
        d['response'] = response
        entities, triples, match_triples, post_triples, response_triples, match_index = csk_list_given_message_response_pair(
            post, response)

        if len(match_triples) != 0:
            cnt += 1
            # print(idx)
            # print(len(match_triples))
        if len(match_triples) == 0:
            continue
        d['match_triples'] = [dict_csk_triples[m] for m in match_triples]
        d['all_triples'] = [[dict_csk_triples[m] for m in tri] for tri in triples]
        d['all_entities'] = [[dict_csk_entities[m] for m in ent] for ent in entities]
        d['post_triples'] = post_triples
        d['response_triples'] = [-1 if m == -1 else dict_csk_triples[m] for m in response_triples]
        d['match_index'] = match_index
        corpus.append([post, response])

        if index < 1000:
            devset.append(d)

        else:
            trainset.append(d)

        index += 1

    print(cnt)

json.dump(devset, devset_file)
json.dump(trainset, trainset_file)
vocab = build_vocab(corpus)

lst = [resource, {'vocab': vocab}, {'dict_csk': dict_csk}]
json.dump(lst, resource_file)

devset_file.close()
trainset_file.close()
resource_file.close()

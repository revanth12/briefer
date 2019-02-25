import re
import nltk
import numpy as np

from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.chunk import conlltags2tree
from nltk import ne_chunk
from gensim.summarization.summarizer import summarize



nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')
nltk.download('stopwords')
nltk.download('conll2002')
from nltk.corpus import conll2000, conll2002
from nltk.classify import MaxentClassifier
from nltk.probability import DictionaryProbDist
import os
import pickle

txt = "It was November. Although it was not yet late, the sky was dark when I turned into Laundress Passage. Father had finished for the day, switched off the shop lights and closed the shutters; but so I would not come home to darkness he had left on the light over the stairs to the flat. Through the glass in the door it cast a foolscap rectangle of paleness onto the wet pavement, and it was while I was standing in that rectangle, about to turn my key in the door, that I first saw the letter. Another white rectangle, it was on the fifth step from the bottom, where I couldn't miss it. I closed the door and put the shop key in its usual place behind Bailey's Advanced Principles of Geometry. Poor Bailey. No one has wanted his fat gray book for thirty years. Sometimes I wonder what he makes of his role as guardian of the bookshop keys. I don't suppose it's the destiny he had in mind for the masterwork that he spent two decades writing.A letter. For me. That was something of an event. The crisp-cornered envelope, puffed up with its thickly folded contents, was addressed in a hand that must have given the postman a certain amount of trouble. Although the style of the writing was old-fashioned, with its heavily embellished capitals and curly flourishes, my first impression was that it had been written by a child. The letters seemed untrained. Their uneven strokes either faded into nothing or were heavily etched into the paper. There was no sense of flow in the letters that spelled out my name. Each had been undertaken separately -- M A R G A R E T L E A -- as a new and daunting enterprise. But I knew no children. That is when I thought, It is the hand of an invalid.It gave me a queer feeling. Yesterday or the day before, while I had been going about my business, quietly and in private, some unknown person -- some stranger -- had gone to the trouble of marking my name onto this envelope. Who was it who had had his mind's eye on me while I hadn't suspected a thing?"


def briefer(txt):
    reduced_text = summarize(txt, ratio=0.8)

    tokenised = nltk.word_tokenize(reduced_text)
    position = nltk.pos_tag(tokenised)
    ent_it = nltk.ne_chunk(position, binary=False)

    entiti = list(ent_it)
    enti = []
    for ent in entiti:
        if (type(ent) == nltk.tree.Tree):
            enti.append(ent)

    label_names = [enti[i].label() for i in range(len(enti))]

    def word_detection(word):
        start_index = txt.index(word)
        end_index = txt.index(word) + len(word)
        return (start_index, end_index)

    entities = {}
    for i in range(len(enti)):
        if enti[i].label() not in entities.keys():
            entities[enti[i].label()] = [' '.join([enti[i][j][0] for j in range(len(enti[i]))])]
        else:
            entities[enti[i].label()].append(' '.join([enti[i][j][0] for j in range(len(enti[i]))]))

    values = list(entities.values())

    vult = []

    for key, value in entities.items():
        for val in value:
            vult.append(key)

    vult
    #################################################
    entities = {}
    for i in range(len(enti)):
        if enti[i].label() not in entities.keys():
            entities[enti[i].label()] = [' '.join([enti[i][j][0] for j in range(len(enti[i]))])]
        else:
            entities[enti[i].label()].append(' '.join([enti[i][j][0] for j in range(len(enti[i]))]))

    entity_key = list(entities.keys())

    # word_detection(entities[entity_key[0]][0][0])

    word_position = {}
    for i in range(len(entity_key)):
        for j in range(len(entities[entity_key[i]])):
            word_position[entities[entity_key[i]][j]] = word_detection(entities[entity_key[i]][j])

    word_position

    #####################################################
    entities_updated = {}
    for key, value in entities.items():
        # print(key)
        for li in value:
            if (len(li) > 1):
                # print([' '.join(li)])
                entities_updated[key] = ' '.join(li)
                print(entities_updated)
            else:
                # print(li)
                entities_updated[key] = li
                print(entities_updated)

    ####################################################
    ' '.join(list(entities.values())[0][0])
    ############################################

    stop_words = set(stopwords.words('english'))

    def stop_word_removal(input_text):
        words_in_text = word_tokenize(input_text)
        processed_words = [word for word in words_in_text if word not in stop_words]
        return processed_words

    training_set = [(['Laundress Passage'], 'ORGANIZATION'),
                    (['Advanced Principles'], 'PERSON'),
                    (['Father'], 'PERSON'),
                    (['Bailey'], 'PERSON'),
                    (['Poor Bailey'], 'PERSON'),
                    (['Geometry'], 'GPE')]

    def list_to_dict(words_list):
        return dict([(word, True) for word in words_list])

    training_set_formatted = [(list_to_dict(element[0]), element[1]) for element in training_set]
    training_set_formatted

    ######################################
    numIterations = 100

    algorithm = nltk.classify.MaxentClassifier.ALGORITHMS[1]
    classifier = nltk.MaxentClassifier.train(training_set_formatted, algorithm, max_iter=numIterations)

    #######################################
    scores = []
    for i in range(len(training_set_formatted)):
        prob = classifier.prob_classify(training_set_formatted[i][0])
        label = prob.max()
        probability = prob.prob(label)
        scores.append(probability)
    #########################################
    final_dict = {}
    for i in range(len(word_position)):
        new_dict = {}
        new_dict['BeginOffset'] = word_position[list(word_position.keys())[i]][0]
        new_dict['EndOffset'] = word_position[list(word_position.keys())[i]][1]
        new_dict['Type'] = vult[i]
        new_dict['Score'] = scores[i]
        final_dict[list(word_position.keys())[i]] = new_dict

    return final_dict











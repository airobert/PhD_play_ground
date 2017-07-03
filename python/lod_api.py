import requests
import time
import re
import random
import tsv_reader as tsvr

endpoint_subject = 'http://webscale.cc:3001/LOD-a-lot?'
filepath_movies_train = "../../../../mc-movies.pruned.train.tsv"



def respronse_clean_up(response_triple):
    response_triple_list = response_triple.split('> ')
    if response_triple_list[-1] == '.':
        response_triple_list = response_triple_list[:-1]
    clean_triple = []
    for triple_part in response_triple_list:
        triple_part = re.sub('[<>]', '', triple_part)
        clean_triple.append(triple_part)
    return clean_triple

def generate_walk(word, endpoint):
    param_sub = {'subject': word}
    start_time_call = time.time()
    response_sub = requests.get(endpoint, params=param_sub)
    if '<!DOCTYPE html>' in response_sub.content:
        response_sub = []
    param_obj = {'object': word}
    response_obj = requests.get(endpoint, params=param_obj)
    end_time_call = time.time()
    time_call = end_time_call - start_time_call
    if '<!DOCTYPE html>' in response_obj.content:
        response_obj = []
    if response_obj == [] and response_sub == []:
        return []
    else:
        if not response_sub:
            response_sub_list = []
        else:
            response_sub_list = response_sub.content.split('\n')[:-1]
        if not response_obj:
            response_obj_list = []
        else:
            response_obj_list = response_obj.content.split('\n')[:-1]
        weighted_rand_int = random.randint(0, len(response_sub_list + response_obj_list)-1)
        if weighted_rand_int < len(response_sub_list):
            triple_index = random.randint(0, len(response_sub_list) - 1)
            response_triple = respronse_clean_up(response_sub_list[triple_index])
        else:
            triple_index = random.randint(0, len(response_obj_list) - 1)
            response_triple = respronse_clean_up(response_obj_list[triple_index])[::-1]
        return response_triple, time_call

def main(endpoint, filepath_train):
    tsv_reader = tsvr.tsvReader(filepath_train)
    words, labels = tsv_reader.retrieve_words_and_labels()
    f = open('random_walks_py_all11.txt', 'w')
    faulty_count = 0
    total_count = 0
    start_time = time.time()
    call_time = 0
    for word_index, word in enumerate(words):
        total_count += 1
        if 1384-total_count < 798:
            for j in range(1000):
                random_walk = []
                used_word = word
                for i in range(8):
                    triple, time_call_triple = generate_walk(used_word, endpoint)
                    call_time += time_call_triple
                    if not triple:
                        break
                    else:
                        random_walk = random_walk + triple
                        used_word = triple[2]
                if not random_walk:
                    faulty_count += 1
                    continue
                else:
                    f.write(str(random_walk) + '\n')
            total_time = time.time() - start_time
            system_time = total_time - call_time
            print('%s to go' % (1384-total_count))
            print('[Total time: %s]' % total_time)
            print('[Total system time: %s]' % system_time)
            print('[Total call time: %s]' % call_time)
    print('total count : %s' % total_count)
    print('faulty count : %s' % faulty_count)
    f.close()

# time used for calling and time used for script
# count how many testset instances are not used


main(endpoint_subject, filepath_movies_train)
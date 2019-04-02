import pronoun_detect_2 as pd2
import json
import os 
import urllib.request
import etri
import argparse
import socket
import struct
from urllib.parse import quote
import urllib.request
import re

#NER_dic = {'PERSON': 0, 'STUDY_FIELD' : 1, 'THEORY' : 2, 'ARTIFACTS' : 3, 'ORGANIZATION' : 4, 'LOCATION' : 5, 'CIVILIZATION' : 6, 'DATE' : 7, 'TIME': 8, 'EVENT' : 9, 'ANIMAL' : 10, 'PLANT' : 11, 'MATERIAL' : 12, 'TERM' : 13, 'JOB' : 14, 'QUANTITY' : 15, 'ETC' : 16}
NER_dic = {'PERSON': 0, 'STUDY_FIELD' : 5, 'THEORY' : 5, 'ARTIFACTS' : 5, 'ORGANIZATION' : 2, 'LOCATION' : 1, 'CIVILIZATION' : 5, 'DATE' : 5, 'TIME': 4, 'EVENT' : 3, 'ANIMAL' : 5, 'PLANT' : 5, 'MATERIAL' : 5, 'TERM' : 5, 'JOB' : 5, 'QUANTITY' : 5, 'ETC' : 5}
#NER_dic = {'PERSON': 0, 'LOCATION' : 1, 'ORGANIZATION':2, 'EVENT':3, 'TIME': 4, 'ETC':5}

description = "[--input_path]: path of input json dataset [--output_path]: output v4_gold_conll file path [--previous_path]: previous paragraph of input datasets [--output_file]: output file name [--modified_path]: modify input json dataset which adds pronoun candidates [--mode]: [predict/train] [--ratio] floating number [--ZA]: [on/off] (default:off)"

def getETRI(text):
    host = '143.248.135.146'
    port = 33333
    
    ADDR = (host, port)
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
#print("clientSocket.connect")
        clientSocket.connect(ADDR)
    except Exception as e:
        return None
    try:
#print(text)
        clientSocket.sendall(str.encode(text))
        #clientSocket.sendall(text.encode('unicode-escape'))
        #clientSocket.sendall(text.encode('utf-8'))
        buffer = bytearray()
        while True:
#print("clinetSocket.recv")
            data = clientSocket.recv(1024)
            if not data:
                break
            buffer.extend(data)
        result = json.loads(buffer.decode(encoding='utf-8'))
        return result
    except Exception as e:
        pass
    finally :
        clientSocket.close()

def get_conll_format(morp_file, file_name, pronouns, entities, pronoun_candidates, mode, ZAs, ZA_mode):
    string = "#begin document (" + file_name + "); part 000\n"
    for sentence in morp_file:
        opener = 0
        closer = 0
        token_list = []
        token_index = 0
        for token in sentence:
            temp = []
            temp.append(token['lemma'])
            temp.append(token['type'])
            temp.append(token['st'])
            temp.append(token['en'])
            temp.append("-")
            temp.append("-")
            temp.append("*")
            token_list.append(temp)
        '''
        with open('./test/token_list', 'a') as f:
            f.write(file_name+'\n')
            for item in token_list :
                f.write('%s\n' % item)
            f.write('\n')
        '''


        if ZA_mode == 'on':
            ZA_index = 200000
            for candidate in ZAs:
                ZA_index += 1
                min_st = candidate['st_modified']
                max_en = candidate['en_modified']
                for token in token_list:
                    if candidate['st_modified'] <= token[2] and candidate['en_modified'] > token[2] and max_en <= token[3]:
                         max_ex = token[3]
                    if token[3] > candidate['st_modified'] and token[3] <= candidate['en_modified'] and min_st >= token[2]:
                         min_st = token[2]
                pos = 0
                for token in token_list:
                    if min_st == token[2] and max_en == token[3]:
                         if token[5] == '-':
                            token[5] = "<" + str(ZA_index) + ">"
                            opener += 1
                            closer += 1
                         else:
                            token[5] = "<" + str(ZA_index) + ">" + "|" + token[5]
                            opener += 1
                            closer += 1       
                         pos = 1
                if pos == 0:
                    open_i = 0
                    close_i = 0
                    for token in token_list:
                        if min_st == token[2] and open_i == 0:
                            opener += 1
                            if token[5] == '-':
                                 token[5] = "<" + str(ZA_index)
                            else:
                                 token[5] = "<" + str(ZA_index) + token[5]
                            open_i = 1
                        if max_en == token[3] and close_i == 0:
                            closer += 1
                            if token[5] == '-':
                                 token[5] = str(ZA_index) + ">"
                            else:
                                 token[5] = token[5] + "|" + str(ZA_index) + ">"
                            close_i = 1

        pronoun_index = 100000
        #if mode == 'predict' : predict일때만 대명사 검출기를 사용할 경우 풀기.
        if True :
            for candidate in pronoun_candidates:
                pronoun_index += 1
                min_st = candidate['st_modified']
                max_en = candidate['en_modified']
                for token in token_list:
                    if candidate['st_modified'] <= token[2] and candidate['en_modified'] > token[2] and max_en <= token[3]:
                        max_en = token[3]
                    if token[3] > candidate['st_modified'] and token[3] <= candidate['en_modified'] and min_st >= token[2]:
                        min_st = token[2]
                pos = 0
                for token in token_list:
                    if min_st == token[2] and max_en == token[3]:
                        if token[5] == '-':
                            token[5] = "<" + str(pronoun_index) + ">"
                            opener += 1
                            closer += 1
                        else:
                            token[5] = "<" + str(pronoun_index) + ">"+ "|"+ token[5]
                            opener += 1
                            closer += 1
                            
                        pos = 1
                if pos == 0:
                    open_i = 0
                    close_i = 0
                    for token in token_list:
                        if min_st == token[2] and open_i == 0:
                            opener += 1
                            if token[5] == '-':
                                token[5] = "<" + str(pronoun_index)
                            else:
                                token[5] = "<" + str(pronoun_index) + "|" + token[5]
                            open_i = 1
                        if max_en == token[3] and close_i == 0:
                            closer += 1
                            if token[5] == '-':
                                token[5] = str(pronoun_index) + ">"
                            else:
                                token[5] = token[5] + "|" + str(pronoun_index) + ">"
                            close_i = 1
        
        if mode == 'train' :             
            for pronoun in pronouns:
                pronoun_index += 1
                min_st = pronoun['st_modified']
                max_en = pronoun['en_modified']

                for token in token_list:
                    if pronoun['st_modified'] <= token[2] and pronoun['en_modified'] > token[2] and max_en <= token[3]:
                        max_en = token[3]
                    if token[3] > pronoun['st_modified'] and token[3] <= pronoun['en_modified'] and min_st >= token[2]:
                        min_st = token[2]

                # 태깅받은 대명사를 멘션 바운더리로 활용할 경우 풀기.
                '''
                pos = 0
                for token in token_list:
                    if min_st == token[2] and max_en == token[3]:
                        if token[5] == '-':
                            token[5] = "<" + str(pronoun_index) + ">"
                            opener += 1
                            closer += 1
                        else:
                            token[5] = "<" + str(pronoun_index) + ">"+ "|"+ token[5]
                            opener += 1
                            closer += 1
                                
                        pos = 1
                if pos == 0:
                    open_i = 0
                    close_i = 0
                    for token in token_list:
                        if min_st == token[2] and open_i == 0:
                            opener += 1
                            if token[5] == '-':
                                token[5] = "<" + str(pronoun_index)
                            else:
                                token[5] = "<" + str(pronoun_index) + "|" + token[5]
                            open_i = 1
                        if max_en == token[3] and close_i == 0:
                            closer += 1
                            if token[5] == '-':
                                token[5] = str(pronoun_index) + ">"
                            else:
                                token[5] = token[5] + "|" + str(pronoun_index) + ">"
                            close_i = 1
                '''
                    
                if 'coref_index' in pronoun:
                    pos = 0
                    for token in token_list:
                        if min_st == token[2] and max_en == token[3]:
                            if token[4] == '-':
                                token[4] = "(" + str(pronoun['coref_index']) + ")"
                                opener += 1
                                closer += 1
                            else:
                                token[4] = "(" + str(pronoun['coref_index']) + ")"+ "|"+ token[4]
                                opener += 1
                                closer += 1
                            pos = 1
                    if pos == 0:
                        #print(pronoun)
                        #print(min_st, max_en)
                        open_i = 0
                        close_i = 0
                        for token in token_list:
                            if min_st == token[2] and open_i == 0:
                                opener += 1
                                if token[4] == '-':
                                    token[4] = "(" + str(pronoun['coref_index'])
                                else:
                                    token[4] = "(" + str(pronoun['coref_index']) + "|" + token[4]
                                open_i = 1
                            if max_en == token[3] and close_i == 0:
                                closer += 1
                                if token[4] == '-':
                                    token[4] = str(pronoun['coref_index']) + ")"
                                else:
                                    token[4] = token[4] + "|" + str(pronoun['coref_index']) + ")"
                                close_i = 1

        entity_index = 0
        for entity in entities:
            entity_index += 1
            #if (entity_index == 60) : print(entity)
            if mode == 'train':
                if 'coref_index' in entity:
                    min_st = entity['st_modified']
                    max_en = entity['en_modified']

                    for token in token_list:
                        if entity['st_modified'] <= token[2] and entity['en_modified'] > token[2] and max_en <= token[3]:
                            max_en = token[3]
                        if token[3] > entity['st_modified'] and token[3] <= entity['en_modified'] and min_st >= token[2]:
                            min_st = token[2]
                    #if (entity_index == 60) : print("min&max", min_st, max_en)
                    
                    pos = 0
                    for token in token_list:
                        if min_st == token[2] and max_en == token[3]:
                            opener += 1
                            closer += 1
                            if token[4] == '-':
                                token[4] = "(" + str(entity['coref_index']) + ")"
                            else:
                                token[4] = "(" + str(entity['coref_index']) + ")"+ "|"+ token[4]
                            pos = 1
                    if pos == 0:
                        open_i = 0
                        close_i = 0
                        for token in token_list:
                            if min_st == token[2] and open_i == 0:
                                opener += 1
                                if token[4] == '-':
                                    token[4] = "(" + str(entity['coref_index'])
                                else:
                                    token[4] = "(" + str(entity['coref_index']) + "|" + token[4]
                                open_i = 1
                            if max_en == token[3] and close_i == 0:
                                closer += 1
                                if token[4] == '-':
                                    token[4] = str(entity['coref_index']) + ")"
                                else:
                                    token[4] = token[4] + "|" + str(entity['coref_index']) + ")"
                                close_i = 1

            min_st = entity['st_modified']
            max_en = entity['en_modified']

            for token in token_list:
                if entity['st_modified'] <= token[2] and entity['en_modified'] > token[2] and max_en <= token[3]:
                    max_en = token[3]
                if token[3] > entity['st_modified'] and token[3] <= entity['en_modified'] and min_st >= token[2]:
                    min_st = token[2]

            pos = 0
            for token in token_list:
                if min_st == token[2] and max_en == token[3]:
                    opener += 1
                    closer += 1
                    if token[5] == '-':
                        token[5] = "<" + str(entity_index) + ">"
                    else:
                        token[5] = "<" + str(entity_index) + ">"+ "|"+ token[5]
                    if token[6] == '*':
                        token[6] = "[" + str(NER_dic[entity['ne_type']]) + "]"
                    else:
                        token[6] = "[" + str(NER_dic[entity['ne_type']]) + "]"+ "|"+ token[6]
                    pos = 1
            if pos == 0:
                open_i = 0
                close_i = 0
                for token in token_list:
                    if min_st == token[2] and open_i == 0:
                        opener += 1
                        if token[5] == '-':
                            token[5] = "<" + str(entity_index)
                        else:
                            token[5] = "<" + str(entity_index) + "|" + token[5]
                        if token[6] == '*':
                            token[6] = "[" + str(NER_dic[entity['ne_type']]) 
                        else:
                            token[6] = "[" + str(NER_dic[entity['ne_type']]) + "|" + token[6]
                        open_i = 1
                    if max_en == token[3] and close_i == 0:
                        closer += 1
                        if token[5] == '-':
                            token[5] = str(entity_index) + ">"
                        else:
                            token[5] = token[5] + "|" + str(entity_index) + ">"
                        if token[6] == '*':
                            token[6] = str(NER_dic[entity['ne_type']]) + "]"
                        else:
                            token[6] = token[6] + "|" + str(NER_dic[entity['ne_type']]) + "]"
                        close_i = 1                
                            
        if opener != closer:
            print("filename :", file_name)
            print(opener, closer)
            with open('make_conll.log', 'a', encoding='utf-8') as f:
                log_string = file_name + '\t' + str(opener) + '\t' + str(closer)+'\n'
                f.write(log_string)

        for token in token_list:
            string += file_name + "\t"
            string += "0" + "\t"
            string += str(token_index) + "\t"
            token_index += 1
            string += token[0]+"/"+token[1]+ "\t"
            string += token[1] + "\t"
            string += "-" + "\t"
            if token[1].startswith("V") == True:
                string += token[0] + "\t"
            else:
                string += "-" + "\t"
                
            string += "-\t-\t-\t"
            string += token[6] + "\t"+ token[5] + "\t"
            string += "NOTIME\tNOTIME\t-\t"
            string += token[4] + "\n"
        string += "\n"
    string += "#end document\n"
    return string

def make_coref_indices(input_path,  mode, ratio, previous_dir=None, modified_set_dir=None, output_path="./", output_file = "output", ZA_mode = "off"):
    #/print("okay")
    entity_dic = {}
    entity_index = 1
    contents = []
    history_file = []
    total_string = ""
    coref_index = 1
    data_list = os.listdir(input_path)
    if mode == 'train':
        train_file = data_list[:int(ratio * len(data_list))]
        dev_file = data_list[int(ratio*len(data_list)):]
        total_file = [train_file, dev_file]
        #print("total file :", total_file)
        print("train_file :", len(train_file))
        print("dev_file :", len(dev_file))
        
    elif mode == 'predict':
        total_file = [data_list]
    f_index = 1
    for files in total_file:
        #print(files)
        for golden_set in files:
            print("golden_set :", golden_set)
            document_dic = {}
            save_file_name = []   

            file = input_path + golden_set
            if golden_set in history_file:
                continue
            f = open(file, "r", encoding="utf-8")
            json_file = json.load(f)
            f.close()
            #print(json_file)
            index = golden_set.split('_')[0]
            total_json = []
            for i in range(1, 15):
                previous_p = str(index)+"_"+str(i)+".json"
                if os.path.exists(previous_dir + previous_p) == True:
                    g = open(previous_dir + previous_p, "r", encoding="utf-8")
                    prev_file = json.load(g)
                    history_file.append(previous_p)
                    save_file_name.append(previous_p)
                    g.close()

                    total_json += [prev_file]
            if total_json == []:
                total_json = [json_file]
                save_file_name = [golden_set]
            
            if (mode == 'train'):
                for json_list in total_json:
                    for entities in json_list['entities']:
                        if entities['ancestor'].startswith("-") or entities['ancestor'] == '':
                            continue
                        p_index = int(entities['ancestor'].split('-')[0])
                        e_index = int(entities['ancestor'].split('-')[1])
                        for json_ in total_json:
                            if int(json_['parID']) == p_index: 
                                if 'coref_index' not in json_['entities'][e_index]:
                                    json_['entities'][e_index]['coref_index'] = coref_index
                                    coref_index += 1
                                    entities['coref_index'] = json_['entities'][e_index]['coref_index']
                                else:
                                    entities['coref_index'] = json_['entities'][e_index]['coref_index']
                for json_list in total_json:
                    if 'pronouns' in json_list:
                        for pronouns in json_list['pronouns']:
                            if pronouns['ancestor'].startswith("-") or pronouns['ancestor'] == '':
                                continue
                            p_index = int(pronouns['ancestor'].split('-')[0])
                            e_index = int(pronouns['ancestor'].split('-')[1])
                            for json_ in total_json:
                                if p_index == int(json_['parID']):
                                    if 'coref_index' not in json_['entities'][e_index]:
                                        json_['entities'][e_index]['coref_index'] = coref_index
                                        coref_index += 1
                                        pronouns['coref_index'] = json_['entities'][e_index]['coref_index']
                                    else:
                                        pronouns['coref_index'] = json_['entities'][e_index]['coref_index']
    
            pd = pd2.PronounDetector()
            for x in range(0, len(total_json)):
                total_json[x]['pronoun_candidate'] = pd.detect({'text': total_json[x]['plainText']})['pronoun_list'] 
                total_json[x]['ModifiedText'] = total_json[x]['plainText'].replace("[.<line>.]", " ")
                total_json[x]['ModifiedText'] = total_json[x]['ModifiedText'].replace("_", " ")
                for pronoun_candidate in total_json[x]['pronoun_candidate']:
                    pronoun_candidate['st_modified'] = pronoun_candidate['st']
                    pronoun_candidate['en_modified'] = pronoun_candidate['en']
                for pronoun in total_json[x]['pronouns']:
                    pronoun['st_modified'] = pronoun['st']
                    pronoun['en_modified'] = pronoun['en']
                for entity in total_json[x]['entities']:
                    entity['st_modified'] = entity['st']
                    entity['en_modified'] = entity['en']
                ETRI = getETRI(total_json[x]['ModifiedText'])
                while (ETRI == None) :
                    ETRI = getETRI(total_json[x]['ModifiedText'])
                sentences = ETRI['sentence']
                if ZA_mode == "on" :
                    total_json[x]['ZA_candidate'] = []
                    #ETRI = ETRI_   
                    #print(ETRI.keys())
                    
                    temp_texts = ""
                    ZA_id = 0
                    ZA_length = 0
                    plus_index = 0
                    sentence_number = 0
                    ZA_number = 0
                    plus_number = 0
                    for sentence in sentences:
                        temp_text = sentence['text']
                        temp_text_length = len(sentence['text'])
                        temp_plus_index = 0
                        sorted_entity = sorted(total_json[x]['entities'], key = lambda k : k['st_modified'])
                        '''
                        ET_temp_text = sentence['text']
                        for entity in sorted_entity:
                            if entity['st_modified']+temp_plus_index >= ZA_length and entity['en_modified']+temp_plus_index < ZA_length + temp_plus_index + temp_text_length:
                                st_temp = entity['st_modified']-ZA_length+temp_plus_index
                                en_temp = entity['en_modified']-ZA_length+temp_plus_index
                                ET_temp_text = ET_temp_text[:st_temp]+"[" + ET_temp_text[st_temp:en_temp] + "]" + ET_temp_text[en_temp:]
                                temp_plus_index += 2
                        '''
                        abbreviation_existance = 0
                        #print(temp_texts[ZA_length-2:ZA_length])
               
                        if ZA_length > 0 and temp_texts[ZA_length-1] == '.' and re.match('[A-Za-z]',temp_texts[ZA_length-2]) != None:
                            abbreviation_existance = 1
                            #print(abbreviation_existance)
                        SBJ_existance = 0
                        V_existance = 0
                        if temp_text[0] == ' ':
                            plus_index = 1
                            plus_number += 1
                        else:
                            plus_index = 0

                        for dependency in sentences[sentence_number]['dependency']:
                            if dependency['label'].find("SBJ") != -1:
                                SBJ_existance = 1
                            if dependency['label'] == "VP" or dependency['label'] == "VNP":
                                V_existance = 1

                        z = 0
                        if SBJ_existance == 0 and V_existance == 1 and abbreviation_existance == 0:
                            for pronoun_candidate in total_json[x]['pronoun_candidate']:
                                if pronoun_candidate['st_modified'] >= ZA_length + plus_index:
                                    pronoun_candidate['st_modified'] += 3
                                    pronoun_candidate['en_modified'] += 3
                            for pronoun in total_json[x]['pronouns']:
                                if pronoun['st_modified'] >= ZA_length + plus_index:
                                    pronoun['st_modified'] += 3
                                    pronoun['en_modified'] += 3
                            for entity in total_json[x]['entities']:
                                if entity['st_modified'] >= ZA_length + plus_index:
                                    entity['st_modified'] += 3
                                    entity['en_modified'] += 3
                            for zas in total_json[x]['ZA_candidate']:
                                if zas['st_modified'] >= ZA_length + plus_index:
                                    zas['st_modified'] += 3
                                    zas['en_modified'] += 3
                            start_position = sentence['morp'][0]['position']
                            _he = {'lemma': '그', 'position': start_position + ZA_number*7, 'id': 0, 'type':'NP', 'weight' : 0.328001}
                            _is = {'lemma': '는', 'position': start_position + ZA_number*7+3, 'id': 1, 'type':'JX', 'weight' : 0.122593}
                            sentence['morp'].insert(0, _is)
                            sentence['morp'].insert(0, _he)
                            ZA_number += 1
                            #print(sentence['morp'])
                            #print('ZA_number' ,ZA_number)

                            temp_text = temp_text[:plus_index] + "그는 " + temp_text[plus_index:]
                            sentence['text'] = temp_text
                            total_json[x]['ZA_candidate'].append({"id": ZA_id, "st_modified": ZA_length+plus_index, "en_modified": ZA_length+1+plus_index, "surface": "그"})
                            z = 2

                        for morp in sentence['morp'][z:] :
                            morp['position'] += ZA_number*7
                            morp['id'] += 2
                            
                        
                        
                        temp_texts += temp_text
                        ZA_length = len(temp_texts)      
                        sentence_number += 1
                    total_json[x]['ModifiedText'] = temp_texts
                result = pd._set_position_character(sentences)
                #print(golden_set)
#with open('./MTA02/temp/'+golden_set, 'w', encoding='utf-8') as parse_f:
#                    json.dump(result, parse_f, ensure_ascii=False, indent='\t')
                with open('./pilot2_task2_output/morp/'+golden_set, 'w', encoding='utf-8') as parse_f:
                    json.dump(result, parse_f, ensure_ascii=False, indent='\t')
				#print(result) 
                morp_result = []
                for res in result:
                     #print(res['morp'])
                     morp_result.append( res['morp'] )
                #    print(res)
                if ZA_mode == 'on':
                    string = get_conll_format(morp_result, save_file_name[x], total_json[x]['pronouns'], total_json[x]['entities'], total_json[x]['pronoun_candidate'], mode, total_json[x]['ZA_candidate'], ZA_mode)
                else:
                    string = get_conll_format(morp_result, save_file_name[x], total_json[x]['pronouns'], total_json[x]['entities'], total_json[x]['pronoun_candidate'], mode, [], ZA_mode)
                total_string += string
                #print("total_string :", total_string[:40])
                #print("string :", string[:40])
            if modified_set_dir != None:
                for x in range(0, len(total_json)):
                    with open(modified_set_dir+save_file_name[x], 'w', encoding='utf-8') as make_file:
                        json.dump(total_json[x], make_file, ensure_ascii=False, indent='\t')
    
        if mode == 'train' and f_index == 1:
            g = open(output_path+'train.'+output_file+".v4_gold_conll", "w", encoding='utf-8')
            g.write(total_string)
            print("wrtie training data")
            total_string = ""
            g.close()
        if mode == 'train' and f_index == 2:
            g = open(output_path+'dev.'+output_file+".v4_gold_conll", "w", encoding='utf-8')
            g.write(total_string)
            print("write dev data")
            g.close()
        if mode == 'predict':
            g = open(output_path+output_file+".v4_gold_conll", "w", encoding='utf-8')
            g.write(total_string)
            g.close()
        print(f_index)       
        f_index += 1
        
def main():
    parser = argparse.ArgumentParser(description=description)
    
    parser.add_argument('--input_path', type=str, default=None,
                         metavar = 'input_path',
                        help = 'your input json file path')
    parser.add_argument('--output_path', type=str, default=None,
                        metavar = 'output_path',
                        help = 'your output v4_gold_conll file path')
    parser.add_argument('--output_file', type=str, default=None,
                        metavar = 'output_file',
                        help = 'your output v4_gold_conll file name')
    parser.add_argument('--previous_path', type=str, default=None,
                        metavar = 'previous_path',
                        help = 'your previous paragraphs previous path (default: input_path)')
    parser.add_argument('--modified_path', type=str, default=None,
                        metavar = 'modified_path',
                        help = 'your modified json file output path (default: None)')
    parser.add_argument('--mode', type=str, default='predict',
                        metavar = 'mode [train/predict]',
                        help = 'select mode [train/predict]')
    parser.add_argument('--ratio', type=float, default='1.0',
                        metavar = 'ratio of train/dev set in train mode',
                        help = 'ratio of train/dev set in train mode')
    parser.add_argument('--ZA', type=str, default='off',
                        metavar = 'zero anaphora converting to \"he is\"',
                        help = '[on/off]')
    args = parser.parse_args()
    input_path = args.input_path
    output_path = args.output_path
    output_file = args.output_file
    previous_path = args.previous_path
    modified_path = args.modified_path
    ZA_mode = args.ZA
    mode = args.mode
    ratio = args.ratio
    if previous_path == None:
        previous_path = input_path
    if input_path == None or output_file == None:
        print("[Error]")
        
    make_coref_indices(input_path, mode, ratio, previous_path, modified_path, output_path, output_file, ZA_mode)

if __name__ == "__main__":
    main()
    print("[Done] make conll form")

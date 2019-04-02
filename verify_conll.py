f = open('./MTA02/input/nonJosa_train1345.NER5.v4_gold_conll', 'r', encoding='utf-8')

iscontent = False
ner_stack = []
mention_stack = []
gold_stack = []
#count = 0
name = ''
while True:
    line = f.readline()
#    print(line)
#    print(count)
#    count += 1
    if not line : break
    if (line == '\n'): continue
    if (line.find("#end document") != -1) :
        if (len(ner_stack) != 0) :
            print(name)
            print("ner_stack :", ner_stack)
        if (len(mention_stack) != 0) :
            print(name)
            print("mention_stack :", mention_stack)
        if (len(gold_stack) != 0):
            print(name)
            print("gold_stack :", gold_stack)
        iscontent = False
        #print("one document finish")

    if iscontent :
#        print("iscontent :", iscontent)
        words = line.split()
        ners = words[10].split('|')
        mentions = words[11].split('|')
        golds = words[15].split('|')

        #print(mention_stack)
        for ner in ners :
            if ((ner == '*') or (ner == '-')): break
            if ((ner[0] == '[') and (ner[-1] == ']')) : continue
            elif (ner[0] == '[') :
                ner_stack.append(line)
            elif (ner[-1] == ']') :
                if (len(ner_stack) == 0 ) :
                    print(name)
                    print(line)
                ner_stack.pop()
        for mention in mentions :
            if ((mention == '-') or (mention == '*')): break
            if ((mention[0] == '<') and (mention[-1] == '>')) : continue
            elif (mention[0] == '<') :
                mention_stack.append(line)
            elif (mention[-1] == '>') : 
                if (len(mention_stack) == 0) : 
                    print(name)
                    print(line)
                mention_stack.pop()
        for gold in golds :
            if ((gold == '-') or (gold == '*')): break
            if ((gold[0] == '(') and (gold[-1] == ')')) : continue
            elif (gold[0] == '(') :
                gold_stack.append(line)
            elif (gold[-1] == ')') : 
                if (len(gold_stack) == 0) :
                    print(name)
                    print(line)
                gold_stack.pop()

    if (line.find("#begin document") != -1) :
        iscontent = True
        ner_stack = []
        mention_stack = []
        gold_stack = []
        name = line.split()[2]
#    print(line)

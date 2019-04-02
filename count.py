

f = open('./test/181130/test.result181130.v4_gold_conll', 'r', encoding='utf-8')

iscontent = False
mention_stack = []
#mention_stack_wopn = []
gold_stack = []
f1 = []

mention_id = -1
group_id = -1

count = 0
while True:
    line = f.readline()
    if not line : break
    if (line == '\n'): continue
    if (line.find("#end document") != -1) :
        gold_stack.append(group_id+1)
        mention_stack.append(mention_id+1)
        iscontent = False
    if iscontent :
        words = line.split()
        mentions = words[11].split('|')
        golds = words[15].split('|')
        
        for mention in mentions :
            if ((mention == '-') or (mention == '*')): break
            else :
                temp_id = int(mention.replace('<', '').replace('>', ''))
                if (temp_id > mention_id) : mention_id = temp_id
        for gold in golds :
            if ((gold == '-') or (gold == '*')): break
            else :
                gold_id = int(gold.replace('(', '').replace(')', ''))
                if (gold_id > group_id) : group_id = gold_id


    if (line.find("#begin document") != -1) :
#        print(line)
        iscontent = True
        mention_id = -1
        group_id = -1
        count += 1

print("documents :", count) 
print("group :", gold_stack[-1])
#print("mention :", mention_stack)

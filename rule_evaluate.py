

f = open('./test/181130/test.result181130.v4_gold_conll', 'r', encoding='utf-8')

iscontent = False
mention_stack = []
#mention_stack_wopn = []
gold_stack = []
f1 = []
#count = 0
while True:
    line = f.readline()
    if not line : break
    if (line == '\n'): continue
    if (line.find("#end document") != -1) :
        iscontent = False
#        print("one document finish")
     #   p = len(gold_stack) / len(mention_stack)
    #    r = 1
   #     score = (p*r) / (p+r)
  #      f1.append(score)
 #       print("f1 :", sum(f1)/len(f1))
    if iscontent :
        words = line.split()
        mentions = words[11].split('|')
        golds = words[15].split('|')
        
        for mention in mentions :
            if ((mention == '-') or (mention == '*')): break
            elif (mention[0] == '<') :
                mention_stack.append(mention[1:])
                #if (int(mention[1:].replace('>', "")) < 10000) :
                    #print(mention)
                  #  mention_stack_wopn.append(mention[1:])
        for gold in golds :
            if ((gold == '-') or (gold == '*')): break
            elif (gold[0] == '(') :
                gold_stack.append(gold[1:])

    if (line.find("#begin document") != -1) :
#        print(line)
        iscontent = True
#        mention_stack = []
#        gold_stack = []
#print(len(mention_stack))
#print(len(mention_stack_wopn))
p = len(gold_stack) / len(mention_stack)
r = 1
f1 = 2*(p*r)/(p+r)
print("precision :", p)
print("f1 :", f1)
#print("precision(without PN) :", len(gold_stack) / len(mention_stack_wopn))
#    print(line)

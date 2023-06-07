import re
import time

from language_elements import Word, Chunk, Sentence

word_attributes = vars(Word)['__annotations__']
chunk_attributes = vars(Chunk)['__annotations__']
sentence_attributes = vars(Sentence)['__annotations__']

print(word_attributes, chunk_attributes, sentence_attributes, sep='\n\n\n')
time.sleep(1)

list_of_sentences = []
s = None
c = None
w = None

with open(r".\Dataset\DL-DL MT\DL-DL MT\Set1_governance_translated_part1_00001-00050.txt", mode='r',  encoding='utf-8') as f:
    for line_number, line in enumerate(f):
        # print(line)
        if line_number < 4:
            continue

        tab_sep = line.strip().split('\t')
        # print(tab_sep)
        if(tab_sep==['']):
            continue

        elif(tab_sep[0]=='))'):
            s.list_of_chunks.append(c)
            continue

        elif(line.startswith("</document>")):
            continue

        elif(line.startswith("</Sentence>")):
            list_of_sentences.append(s)
            continue
        
       
        if(line.startswith("<Sentence")):
            s = Sentence()
            s.list_of_chunks = []
            s.id = re.search(r'\d+', line).group()
            continue

        if(tab_sep[1]=='(('):
            c = Chunk()
            c.list_of_words = []
            c.chunk_id = int(tab_sep[0])
            c.chunk_group = tab_sep[2]
            continue
    

        w = Word()

        ########################### HARD CODED - SKIPPING CHUNK 8 --> Line 1727 
        try:
            index_of_dot = tab_sep[0].index('.')
        except:
            continue
        ########################### HARD CODED

        w.word_id = tab_sep[0][index_of_dot + 1]

        w.kannada_word = tab_sep[1]

        w.pos = tab_sep[2]


        fsaf = tab_sep[3]
        index_of_start = fsaf.index("'")
        fsaf = fsaf[index_of_start+1: -2]

        fsaf_words = fsaf.split(',')
        w.rootword = fsaf_words[0]
        w.lexical_category = fsaf_words[1]
        w.gender = fsaf_words[2]
        w.number = fsaf_words[3]
        w.person = fsaf_words[4]
        w.mode = fsaf_words[5]
        w.suffixes = fsaf_words[6]

        c.list_of_words.append(w)

def test_parsing():
    for sentence in list_of_sentences:
        print("------SENTENCE START-------")
        print("| Sentence ID:", sentence.id)

        for chunk in sentence.list_of_chunks:
            print("| \t------CHUNK START-------")
            print("| \t| Chunk ID:", chunk.chunk_id)
            print("| \t| Chunk Group:", chunk.chunk_group)

            for word in chunk.list_of_words:
                print("| \t| \t------WORD START-------")
                for attr in word_attributes:
                    print('| \t|\t|', attr, getattr(word, attr))
                print("| \t|\t------WORD END-------\n|\t|")
            
            print("| \t------CHUNK END-------\n|")
        print("------SENTENCE END-------\n\n\n")

        print("=========================================================")
        input()

test_parsing()
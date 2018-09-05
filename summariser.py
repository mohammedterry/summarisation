from semantic_vectors import we_vecs, cg_vecs
stopwords = ('can', 'until', 'over', 'him', 'further', 'am', 'after', 'few', 'do', 'he', 'aren', 'need', 'it', 'usually', 'call', 'shall', "n't", 'm', 'an', 'ca', 'whom', 'in', 'we', 'this', 'or', 'which', '"', 'themselves', 'out', 'were', 'below', 'hers', 'and', 'above', 'only', 'but', 'them', 'cal', 'more', 't', 'wan', 'yours', 'our', 'being', 'then', "'ve", 'to', 'ours', "'", 'mean', 'sha', 'had', 'while', 'again', 'myself', 'both', 'should', 'been', 'own', 'itself', 'nt', 'once', 'no', 'into', 'most', 'his', 'may', 'not', 'before', 'that', 'ourselves', 'as', 'a', 'if', 'having', 'doing', 'against', 'up', 'now', 'any', 'she', 'because', 'dare', 'her', 'have', 'might', 'i', 'the', 'yourselves', 'just', 'very', 'too', "'m", 'be', 'for', 'my', 'by', 'from', 'was', 'sometimes', 'off', 'me', 'other', 'on', 's', 'must', 'na', 'its', 'you', 'here', 'with', 'of', 'does', 'their', 'yourself', 'through', 'has', 'did', 'himself', 'these', 'nor', 'all', 'could', 'your', 'they', 'than', 'those', 'same', 'some', 'would', 'at', 'ought', 've', 'will', 'such', 'down', 'theirs', 'between', 'herself', 'want', 'so', 'are', 'under', 'don', 'still', 'during', 'about', 'each', 'there', 'is')


def summarise(paragraph, threshold =.99):
    cleaned_paragraph = [word.lower() for word in clean(paragraph).split() if word not in stopwords]
    weights = [len(vectorise(word)) for word in cleaned_paragraph]
    total_weight = sum(weights)
    return {word for word,weight in zip(cleaned_paragraph, weights) if importance(weight,total_weight) >= threshold}

def vectorise(word):
    if word in we_vecs:
        return we_vecs[word]
    if word[:-1] in we_vecs:
        return we_vecs[word[:-1]]
    if word[:-2] in we_vecs:
        return we_vecs[word[:-2]]
    return intersect_vectors([cg_vecs[cg] if cg in cg_vecs else set() for cg in chargrams(word)])    

def chargrams(word):
    word = ' ' + word.lower() + ' '
    return {char + nex + nnex for char,nex,nnex in zip(word,word[1:],word[2:])}

def intersect_vectors(vectors):
    try:
        vec = vectors[0]
        for vector in vectors:
            vec = vec.intersection(vector)
        return vec
    except:
        return set()

def importance(weight,total_weight):
    return 1-(weight/total_weight)


def clean(txt):
    cleaned = ''
    for letter in txt:
        if 97 <= ord(letter.lower()) <= 122 or letter.isdigit():
            cleaned += letter
        elif letter not in "'´-":
            cleaned += " "
    return ' '.join(cleaned.split())

example = '''
Textual information in the form of digital documents quickly accumulates to huge amounts of data. 
Most of this large volume of documents is unstructured: it is unrestricted and has not been organized into traditional databases. 
Processing documents is therefore a perfunctory task, mostly due to the lack of standards.
'''
summary = summarise(example)
print(summary)
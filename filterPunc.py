import string

def filterPunc(inputStr=""):
    #version 1.0, Oct. 21st, 2016
    #IMPORTANT:
    #at the beginning of the whole program, must import string
    #i.e. "import string"
    exclude= set(string.punctuation);
    res = ''.join(ch for ch in inputStr if ch not in exclude)
    return res





if __name__ == "__main__":
    # a test function
    trial="ring. With. Punctuation!@$!#%@*!(@ADq!@@$(!@E{}#|}qww]"
    output=filterPunc(trial)
    print output;



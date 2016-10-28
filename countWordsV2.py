#0-49;50-99;100-149;150-199;200-249;250-299;300+
import string
import matplotlib.pyplot as plt
import numpy as np

def filterPunc(inputStr=""):
    #version 1.0, Oct. 21st, 2016
    #IMPORTANT:
    #at the beginning of the whole program, must import string
    #i.e. "import string"
    exclude= set(string.punctuation);
    res = ''.join(ch for ch in inputStr if ch not in exclude)
    return res

def countWords(readInFileName="./posts.txt",drawPlot=0):
    readin_file=open(readInFileName, "r");
    wholeContent=readin_file.read();
    postList=wholeContent.split("}, {");
    Eng = [0, 0, 0, 0, 0, 0, 0];
    Kh = [0, 0, 0, 0, 0, 0, 0];
    mixEng = [0, 0, 0, 0, 0, 0, 0];
    mixKh = [0, 0, 0, 0, 0, 0, 0];
    maxNum=0;#max(Kh+Eng)
    for postnum in range(len(postList)):
        if "\\\"message\\\"" not in postList[postnum]:
            #this post does not have a message field
            continue;
        thisLan=2;#represents which Language this post is using, 1 for Eng, 2 for Eng+Kh, 3 for Kh
        divideOne=postList[postnum].split("\\\"message\\\": \\\"")
        divideTwo=divideOne[1].split("\\\", \\\"");
        #use divideTwo[0]
        KhCount=divideTwo[0].count("\\u");#how many Kh words
        EngCount=0;
        divideThree=divideTwo[0].split(" ");
        for iter in range(len(divideThree)):
            if "\\u" not in divideThree[iter]:
                EngCount=EngCount+1;
        maxNum=max(maxNum,(KhCount+EngCount));

        if KhCount==0:
            thisLan=1;
        if EngCount==0:
            thisLan=3;
        if thisLan==1:#eng
            idx=int(EngCount/50);
            if idx>6:
                idx=6;
            Eng[idx]+=1;
        else:
            if thisLan==2:#mix
                idxe=int(EngCount/50);
                idxk=int(KhCount/50);
                if idxe>6:
                    idxe=6;
                if idxk>6:
                    idxk=6;
                mixEng[idxe]+=1;
                mixKh[idxk]+=1;
            else:#kh
                idx=int(KhCount/50);
                if idx > 6:
                    idx = 6;
                Kh[idx] += 1;




        #postList[postnum]
    print "0-49;50-99;100-149;150-199;200-249;250-299;300+"
    print "pure Eng"
    print Eng
    print "pure Kh"
    print Kh
    print "mix Eng"
    print mixEng
    print "mix Kh"
    print mixKh

    if drawPlot==1:
        fig, ax = plt.subplots();
        index = np.arange(7);
        bar_width = 0.2
        opacity = 0.4
        error_config = {'ecolor': '0.3'}
        rects1 = plt.bar(index, Eng, bar_width,
                         alpha=opacity,
                         color='b',
                         # yerr=std_men,
                         error_kw=error_config,
                         label='English')

        rects2 = plt.bar(index + bar_width, Kh, bar_width,
                         alpha=opacity,
                         color='r',
                         # yerr=std_women,
                         error_kw=error_config,
                         label='Khmer')

        rects3 = plt.bar(index + bar_width * 2, mixEng, bar_width,
                         alpha=opacity,
                         color='b',
                         # yerr=std_men,
                         error_kw=error_config,
                         label='English-mixed')

        rects4 = plt.bar(index + bar_width * 3, mixKh, bar_width,
                         alpha=opacity,
                         color='g',
                         # yerr=std_men,
                         error_kw=error_config,
                         label='Khmer-mixed')
        maxRectHeight=0;
        def autolabel(rects):
            # attach some text labels
            for rect in rects:
                height = rect.get_height()
                maxRectHeight=max(height,maxRectHeight)
                ax.text(rect.get_x() + rect.get_width() / 2.0, 1.05 * height,
                        '%d' % int(height), ha='center', va='bottom')

        for rect in rects1:
            height = rect.get_height()
            maxRectHeight = max(height, maxRectHeight)
            ax.text(rect.get_x() + rect.get_width() / 2.0, 1.05 * height,
                    '%d' % int(height), ha='center', va='bottom')
        for rect in rects2:
            height = rect.get_height()
            maxRectHeight = max(height, maxRectHeight)
            ax.text(rect.get_x() + rect.get_width() / 2.0, 1.05 * height,
                    '%d' % int(height), ha='center', va='bottom')
        for rect in rects3:
            height = rect.get_height()
            maxRectHeight = max(height, maxRectHeight)
            ax.text(rect.get_x() + rect.get_width() / 2.0, 1.05 * height,
                    '%d' % int(height), ha='center', va='bottom')
        for rect in rects4:
            height = rect.get_height()
            maxRectHeight = max(height, maxRectHeight)
            ax.text(rect.get_x() + rect.get_width() / 2.0, 1.05 * height,
                    '%d' % int(height), ha='center', va='bottom')

        plt.xlabel("English | Khmer | English-mixed | Khmer-mixed")
        plt.ylabel("number of posts")
        plt.title("Statistics of number of posts w.r.t language")
        plt.xticks(index + bar_width, ('0-49', '50-99', '100-149', '150-199', '200-249', '250-299', '300+'))
        # plt.legend()
        ax.set_ybound(0, maxRectHeight+200)

        plt.tight_layout()
        plt.show()
        # plt.savefig(u't.png')
        pass;

    if drawPlot==2:#Eng+Khmer
        distribution=np.zeros(maxNum+1);
        for postnum in range(len(postList)):
            if "\\\"message\\\"" not in postList[postnum]:
                # this post does not have a message field
                continue;
            thisLan = 2;  # represents which Language this post is using, 1 for Eng, 2 for Eng+Kh, 3 for Kh
            divideOne = postList[postnum].split("\\\"message\\\": \\\"")
            divideTwo = divideOne[1].split("\\\", \\\"");
            # use divideTwo[0]
            KhCount = divideTwo[0].count("\\u");  # how many Kh words
            EngCount = 0;
            divideThree = divideTwo[0].split(" ");
            for iter in range(len(divideThree)):
                if "\\u" not in divideThree[iter]:
                    EngCount = EngCount + 1;
            wordchar=KhCount+EngCount;
            if KhCount<0:
                print "K"
            if EngCount<0:
                print "E"
            distribution[wordchar]=distribution[wordchar]+1;

        pass;
        #print distribution
        #print maxNum
        x = np.arange(0,maxNum+1)
        plt.figure(1)
        plt.plot(x, distribution)
        plt.show()
        plt.figure(2)
        plt.plot(x[:400], distribution[:400])
        plt.show()
        pass;

    if drawPlot==3:#Eng
        distribution = np.zeros(maxNum+1);
        for postnum in range(len(postList)):
            if "\\\"message\\\"" not in postList[postnum]:
                # this post does not have a message field
                continue;
            thisLan = 2;  # represents which Language this post is using, 1 for Eng, 2 for Eng+Kh, 3 for Kh
            divideOne = postList[postnum].split("\\\"message\\\": \\\"")
            divideTwo = divideOne[1].split("\\\", \\\"");
            # use divideTwo[0]
            KhCount = divideTwo[0].count("\\u");  # how many Kh words
            EngCount = 0;
            divideThree = divideTwo[0].split(" ");
            for iter in range(len(divideThree)):
                if "\\u" not in divideThree[iter]:
                    EngCount = EngCount + 1;
            wordchar = EngCount;
            distribution[wordchar] = distribution[wordchar] + 1;

        pass;
        # print distribution
        # print maxNum
        x = np.arange(0, maxNum + 1)
        plt.figure(3)
        plt.plot(x, distribution)
        plt.show()
        plt.figure(4)
        plt.plot(x[:400], distribution[:400])
        plt.show()

        pass;

    if drawPlot==4:#Khmer
        distribution = np.zeros(maxNum+1);
        for postnum in range(len(postList)):
            if "\\\"message\\\"" not in postList[postnum]:
                # this post does not have a message field
                continue;
            thisLan = 2;  # represents which Language this post is using, 1 for Eng, 2 for Eng+Kh, 3 for Kh
            divideOne = postList[postnum].split("\\\"message\\\": \\\"")
            divideTwo = divideOne[1].split("\\\", \\\"");
            # use divideTwo[0]
            KhCount = divideTwo[0].count("\\u");  # how many Kh words
            EngCount = 0;
            divideThree = divideTwo[0].split(" ");
            for iter in range(len(divideThree)):
                if "\\u" not in divideThree[iter]:
                    EngCount = EngCount + 1;
            wordchar = KhCount;
            distribution[wordchar] = distribution[wordchar] + 1;

        pass;
        # print distribution
        # print maxNum
        x = np.arange(0, maxNum + 1)
        plt.figure(5)
        plt.plot(x, distribution)
        plt.show()
        plt.figure(6)
        plt.plot(x[:40], distribution[:40])
        plt.show()
        print np.max(distribution)

        pass;



    #print postList[1].split("\\\", \\\"")[1];
    #print len(postList)
    #print postList[len(postList)-1]



if __name__ == "__main__":
    # a test function
    countWords(readInFileName="./posts.txt",drawPlot=2);
    countWords(readInFileName="./posts.txt", drawPlot=3);
    countWords(readInFileName="./posts.txt", drawPlot=4);


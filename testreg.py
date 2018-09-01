import re

def str():
    newstr = '1212 ehsan \r\n RTP m audio 15000 RTP main' 
    # print(re.match('^RTP m audio 15000 RTP', ))

    firstIndex = newstr.find('m audio')
    index_of_RTP = newstr.find('RTP', firstIndex)
    data = newstr[firstIndex:index_of_RTP]
    port = newstr[firstIndex+len('m audio'): index_of_RTP]
    newstr = newstr.replace(data, 'm audio 16000 ')
    print (port)
    print(newstr)


if __name__ == '__main__':
        str()

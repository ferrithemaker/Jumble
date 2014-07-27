import urllib2
import sys
import re

def getlinksfromurl(url):
        linkset = set()
        try:    
                usock = urllib2.urlopen(url)
                data = usock.read()
                usock.close()
        except:
                data= ''
        s = re.finditer('href', data)
        for link in s:
                endlink=data.find('"',link.end()+2,len(data))
                linkstring=data[link.end()+2:endlink]
                if linkstring.startswith('http'):
                        linkset.add(linkstring)
                if linkstring.startswith('/'):
                        linkset.add(sys.argv[1]+linkstring)
                if linkstring.startswith('./'):
                        linkset.add(sys.argv[1]+linkstring[1:])
        return linkset

def searchstringfromurl(string,url):
        try:    
                usock = urllib2.urlopen(url)
                data = usock.read()
                usock.close()
        except:
                data= ''        
        s = re.finditer(string, data,re.IGNORECASE)
        count = 0
        for hits in s:
                count+=1        
        return count

# TODO: backlinks control
def searchstringfromurlrecursive(string,url,deep,maxdeep):
        linkset=getlinksfromurl(url)
        totalhits=0
        count=1
        print "Analizing (level %i) url %s" %(deep,url)
        print "%i links retrived" % (len(list(linkset)))
        if deep>=maxdeep: #last iteration level
                print "Reading last iteration."
                totalhits=totalhits+searchstringfromurl(string,url)
        if deep<maxdeep: #recursive section
                for link in linkset:
                        print "There are %i links, going recursive into link number %i at url %s" %(len(list(linkset)),count,link)
                        totalhits=totalhits+searchstringfromurlrecursive(string,link,deep+1,maxdeep)
                        count+=1
                totalhits=totalhits+searchstringfromurl(string,url)
                print "Leaving linkset..."
        return totalhits

# Main program
#url = sys.argv[1] #only root url's
#string = sys.argv[2]
#maxdeep = sys.argv[3]
#linkset=getlinksfromurl('http://ferranfabregas.info/testrec/i1_1.html')
#for link in linkset:
#       print link
print "%i matches with the word %s" % (searchstringfromurlrecursive('Barcelona','http://ferranfabregas.info/testrec/i1_1.html',0,3),'barcelona')

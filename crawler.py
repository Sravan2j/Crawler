import sys
import urllib, htmllib, formatter
from urlparse import urljoin
from HTMLParser import HTMLParseError
import string

# This is a crawler program and it needs two arguments,
    #   1. Website link to start crawling from. ( http://..............)
    #   2. Number of links to store ( if not provided, 100 is considered as default value)

class LinksExtractor(htmllib.HTMLParser): # derive new HTML parser
    
    def __init__(self, formatter) :        # class constructor        
        htmllib.HTMLParser.__init__(self, formatter)  # base class constructor
        self.links = []        # create an empty list for storing hyperlinks

    def start_a(self, attrs) :  # override handler of <A ...>...</A> tags
      # process the attributes
        if len(attrs) > 0 :
           for attr in attrs :
               if attr[0] == "href" :   # ignore all non HREF attributes
                   #Refine the hyperlinks: ignore the parameters in dynamic URL, converting
                   #all hyperlinks to absolute URLs, remove duplicated URLs.
                   url=attr[1]
                   url=url.split('?')[0]   #Extract the part before '?' if any.
                   url=url.split('#')[0]   #Extract the part before '#' if any.
                   if url not in self.links:  # check to ensure that duplicate links are not copied.
                       self.links.append(url) # save the link info in the list
    def start_frame(self, attrs) :  # override handler of <frame ...> tags
      # process the attributes
        if len(attrs) > 0 :
           for attr in attrs :
               if attr[0] == "src" :         # ignore all non SRC attributes
                   #Refine the hyperlinks: ignore the parameters in dynamic URL, converting
                   #all hyperlinks to absolute URLs, remove duplicated URLs.
                   url=attr[1]
                   url=url.split('?')[0]   #Extract the part before '?' if any.
                   url=url.split('#')[0]   #Extract the part before '#' if any.
                   if url not in self.links:
                       self.links.append(url) # save the link info in the list
    def start_iframe(self, attrs) :  # override handler of <iframe ...>...</iframe> tags
      # process the attributes
        if len(attrs) > 0 :
           for attr in attrs :
               if attr[0] == "src" :         # ignore all non SRC attributes
                   #Refine the hyperlinks: ignore the parameters in dynamic URL, converting
                   #all hyperlinks to absolute URLs, remove duplicated URLs.
                   url=attr[1]
                   url=url.split('?')[0]   #Extract the part before '?' if any.
                   url=url.split('#')[0]   #Extract the part before '#' if any.
                   if url not in self.links:
                       self.links.append(url) # save the link info in the list
    def get_links(self):
         return self.links

maxcnt=0                     

# IDLE won't accept command line arguments. so, provided an option to work in Python IDLE. 
try:
    __file__       #The __file__ attribute is present when you run this program from command prompt.
                   #If you run this program from IDLE, it will raise a NameError.
except:            
    website=raw_input("Enter the website to start parse from:") 
    num=input("Number of URL's to get:")            
    sys.argv = [sys.argv[0], website,num]         #set sys.argv manually for IDLE

if len(sys.argv)<2:  #check to see whether all the required arguments are passed.
    sys.exit("Error: No start url was passed")  #following error is printed when no arguments are passed.
elif len(sys.argv)<3:  
    print "FYI: Number of URL's to read is not specified. So, 100 will be set as maximum number of URL's count to read"
    maxcnt=100   #set 100 as default value for maximum count, when maximum count is not passed.
else:
    maxcnt=int(sys.argv[2])
    
count=0                                      # maintains the count of links that are stored at any point of time.
format = formatter.NullFormatter()           # create default formatter

if not sys.argv[1].startswith('http://'):    #concatenates "http://" to the link, if not prefixes as "http://"
    sys.argv[1]="http://"+sys.argv[1]

if not sys.argv[1].endswith('/'):    #concatenates "/" to the link, if not suffixes as "/"
    sys.argv[1]=sys.argv[1]+"/"

try:
    urllib.urlopen(sys.argv[1])
except IOError:
    sys.exit("Not a real URL")  #following error is printed when incorrect URL is passed.

urllist=[]                                  # stores all the links
urllist.append(sys.argv[1])                 # stores first link
count=count+1                               # increment the count value each time a link is stored.
links=[]
for eachlink in urllist:
    #skips all non-valid HTML links, i.e., links which directs to download pop-up screen for downloading the files.
    rc=string.find(eachlink,"ftp")          #files that are available for download, can be placed in the folder "ftp".
    if rc!=-1:                              #skips the links that contains string "ftp" in it.
        continue
    rc=string.find(eachlink,"/file")        #files that are available for download, can be placed in the folder "file" or "files".
    if rc!=-1:                              #skips the links that contains string "/file" or "/files" in it.
        continue
    rc=string.find(eachlink,".tar")         
    if rc!=-1:                              #skips the links that contains string ".tar" in it.
        continue

    #skips the files that ends with the .msi,.zip,.exe,.doc,.mkv,.pdf,.tgz,.dmg,.war,.rar,.jpg,.gif,.jpeg,.png
    if eachlink.endswith('.msi/') or eachlink.endswith('.zip/') or eachlink.endswith('.exe/') or eachlink.endswith('.doc/')  \
    or eachlink.endswith('.mkv/') or eachlink.endswith('.pdf/') or eachlink.endswith('.tgz/') or eachlink.endswith('.dmg/')  \
    or eachlink.endswith('.war/') or eachlink.endswith('.rar/') or eachlink.endswith('.jpg/') or eachlink.endswith('.gif/')  \
    or eachlink.endswith('.jpeg/') or eachlink.endswith('.png/'):
        continue
    
    htmlparser = LinksExtractor(format)        # create new parser object
    
    try:
        data = urllib.urlopen(eachlink)
        htmlparser.feed(data.read())              # parse the file saving the info about links
        htmlparser.close()    
        links = htmlparser.get_links()            # get the hyperlinks list
        convlink=[urljoin(eachlink,each) for each in links]      #urljoin is used to combine a base URL and a relative URL to get an absolute URL.
        for each in convlink:                     
            if each not in urllist:               # check to ensure that the duplicate link names are not sored.
                if not each.endswith("/"):
                    each=each+'/'
                urllist.append(each)
                count=count+1
            if count==maxcnt:
                break
        if count==maxcnt:                         # checks whether required count is reached or not.
            break
    except HTMLParseError:
        htmlparser.close()
        continue

#prints all the saved links at the end.
for each in urllist:
    print each


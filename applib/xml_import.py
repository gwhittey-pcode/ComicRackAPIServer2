from xml.dom.minidom import parse
from applib.db_functions import Comic

def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)
def get_node(node,stxt):
    return_value = ""
    try:
        return_value = getText(node.getElementsByTagName(stxt)[0].childNodes)    
    except:
        print("number failed")
    return return_value
def get_xml_dbfile(xmldbfile):
    datasource = open(xmldbfile)
    dom2 = parse(datasource)  # parse an open file
    books = dom2.getElementsByTagName("Book")
    for book in books:
        number = 0
        id = book.getAttribute('Id')
        number = get_node(book,"Number")
        sfile = book.getAttribute('File')
        series =  get_node(book,"Series")
        volume =  get_node(book,"Volume")
        year = get_node(book,"Year")
        month = get_node(book,"Month")
        pagecount = get_node(book, "PageCount")
        currentpage = get_node(book,"CurrentPage")
        lastpageread = get_node(book,"LastPageRead")
        summary = get_node(book,"Summary")
        print(f'ID={id} File={sfile} Number={number}')
        
        comic, created = Comic.get_or_create(
            Id = id,
            Number = number,
            Series = series,
            Volume = volume,
            Year = year,
            Month = month,
            PageCount = pagecount,
            FilePath = sfile,
            LastPageRead = lastpageread,
            CurrentPage = currentpage,
            Summary = summary,
            )
        if created == True:
            print ("created")
        else:
            print ("not created")
        # try:
            
        #     pagecount = book.getElementsByTagName('PageCount')[0]
        #     print(f'Page:{getText(pagecount.childNodes)}')
        # except:
        #     print("ERROR")
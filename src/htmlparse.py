#coding=utf-8
#百度url的编码是GB2312
import urllib.request,re 
import urllib.parse  
import json
#url及页面编码charset
def downloadPage(url,charset):
    h=urllib.request.urlopen(url)
    return h.read().decode(charset)
#抽取(href,标题)二元组
def getterms(r,content):
    m=re.compile(r)
    terms=re.findall(m,content)
    return terms

parseurl=urllib.parse.urlparse("""http://tieba.baidu.com/f/fdir?fd=%C9%FA%BB%EE&sd=%C2%C3%D3%CE&pn=2""")
parsequery=urllib.parse.parse_qs(parseurl.query,False,False,'GBK')
terms=[]
#翻页，获取所有链接
for i in range(1,13):
    parsequery['pn']=i
    print(i)
    encodeparse=urllib.parse.urlencode(parsequery,True,'','GB2312',None)#doSeq是说map中值是sequence形式的即[]括起来的。safe中的字符是不被编码的
    newurl=urllib.parse.urlunparse((parseurl.scheme ,parseurl.netloc,parseurl.path ,parseurl.params ,encodeparse,parseurl.fragment ))
    content=downloadPage(newurl,'GBK')
    terms=terms+getterms(r'<a href=\'(.+)\' target=\'_blank\'>(.+)</a>',content)

postbarDict={}
file='load.json'
fw=open(file,'at')
count=1803
for (url,name) in terms[1803:]:
    postbarDict[name]={'url':url}
    content=downloadPage(url,'utf-8')
    #time.sleep (random.random ())
    member_num=getterms(r'"member_num":(\d+),',content)
    post_num=getterms(r'"post_num":(\d+),',content)
   # print(type(member_num))
    #print(len(member_num))
    if len(member_num)!=0:
        count=count+1
        print( count)
        postbarDict[name]['member_num']=member_num[0]
        postbarDict[name]['post_num']=post_num[0]

    else:
        postbarDict[name]['member_num']=0
        postbarDict[name]['post_num']=0

    fw.writelines(json.dumps({name:postbarDict[name]}))

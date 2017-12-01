import requests
import sqlite3
from selenium import webdriver
import datetime,re,time
from urllib.request import urlopen
import smtplib
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_mail(html):
    


    me = "g.caresort123@gmail.com"
    pwd="sortcare@453"
    
    
    you = "ankushgupta78145@gmail.com"
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Link"
    msg['From'] = me
    msg['To'] = you
    part2 = MIMEText(html, 'html')
    
    msg.attach(part2)
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    ####### Enter email id and password here
    server.login(me,pwd)
    
    server.sendmail(me, you, msg.as_string())
    server.quit()


def check_domain(url):
     if '.de' in url:
        
        return (True)
    
def imprissum(driver,url,con):
    a=open('tv.txt','a')
    source=str(driver.page_source.encode('utf-8'))
    
    scr=re.findall("<script>(.*?)</script>",source)
    s=source.find("<h1>SEO &amp; Speedtest")
    source=source[s:]
    s=source.find('<div class="panel-heading"><h3>')
    source=source[:s]
    for a in range(0,len(scr)):
        source=source.replace(scr[a],'')
    
    
    source=source.replace('\\n','')
    imp=driver.find_element_by_xpath('//*[@id="colophon"]/div[1]/div[4]/div/div[2]/div/p[1]/a').text
    
    if imp=='Imprint':
        driver.get("https://callanerd.help/impressum/")
    else:
        driver.get("https://callanerd.help/impressum/")
    
    email=(driver.find_element_by_xpath('//*[@id="main"]/div/section/div/div/div/div/div/p[5]/a').text)
    print (email) 
    
    con.execute("insert into Website_to_contact values ('%s','%s')"%(url,email))
    con.commit()
    send_mail(source)
    print ('Mail sent')
    

def extract_data(url,driver,con):
    
    if check_domain(url):
        
        site="https://callanerd.help/seo-analyse-und-webseiten-speedtest/"
        driver.get(site)
        driver.find_element_by_xpath('//*[@id="form-buscar"]/section/div/div/h3[2]/input').send_keys(url)
        driver.find_element_by_xpath('//*[@id="form-buscar"]/section/div/div/button').click()
        
        speed=(driver.find_element_by_xpath('//*[@id="content"]/div[1]/div/main/section[3]/div/div[2]/div[2]/p/span[3]').text)
        seo=(driver.find_element_by_xpath('//*[@id="content"]/div[1]/div/main/section[3]/div/div[2]/div[1]/p/span[2]').text)
        print (speed,seo)
        if seo and speed:
            if int(speed)<60 or int(seo.rstrip('%'))<60:
                imprissum(driver,url,con)
        else:
            try:
                imprissum(driver,url,con)
            except:
                
                con.execute("insert into Website_to_contact(url) values ('%s')"%(url))
                con.commit()
                df=''

def txt(x):
    file=open('visited.txt','r')
    rd=file.readlines()
    flag=0
    for a in rd:
        if x in a:
            flag=1
    file.close()
    if flag==0:
        return True

    
        
                
def url_check(u,con):
    file=open('visited.txt','a')
    v=u.split('/')[0]
    if txt(v):
        if "http" not in v:
            w="http://"+v
        try:
            response = urlopen(w)
            x=response.geturl().rstrip('/')
            
        except:
            x=w
        
        if txt(v):
            print (x)
            extract_data(x,driver,con) 
        file.write(x+'\n')
        file.flush()
    file.write(v+'\n')
    file.flush()
    file.close()
    
    if '.de' in u:
        
        
        con.execute("delete from urls_to_visit where url like " + "'" + u + "'")
        con.commit()
        
        now = datetime.datetime.now()
        row = [(str(u),str(now))]
        con.executemany("insert into visited_urls(url, date) values (?, ?)", row)
        con.commit()

driver = webdriver.Chrome(executable_path='C:\chromedriver.exe')

con = sqlite3.connect("memory.db")

try:
    tb="create table Website_to_contact(url varchar(100),email varchar(100));"
    tb=tb.replace('\n','').replace('  ','')
    con.execute(tb)
    con.commit()
except:
    pass

get=con.execute("select url from urls_to_visit")
for row in get:
    u=row[0]
    url_check(u,con)
    
get1=con.execute("select url, tag, date, full_url from wordpress_sites")
for row in get1:
    if "wordpress" in row[1].lower() and ".de" in row[0]:
        u=row[0]
        url_check(u,con)
    
 

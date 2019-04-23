import requests
import re

header = {
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"
}

def get_data(url, data):
    ret = requests.post(url,headers=header,data=data)
    data = re.findall('id="ct100_ContentPlaceHolder_LabelAnswer">.*?"(.*?)"', ret.text, re.S)

def get_val(url):
    ret = requests.get(url, headers=header)
    val = re.findall(r'name="ct100\$ContentPlaceHolder1\$HiddenField2".*?value="(.*?)"', ret.text, re.S)
    print(val)
    return val


def get_vie(url):
    ret = requests.get(url,headers=header).text
    vie = re.findall('id="__VIEWSTATE" value="(.*?)" />',ret,re.S)[0]
    return vie

if __name__ == '__main__':
    url = 'http://www.cmd5.com/'
    md5 = input("请输入需要解密的字符串")
    hed = '''
     __EVENTTARGET:
     __VIEWSTATE:{vie} 
     __VIEWSTATEGENERATOR: CA0B0334
     ctl00$ContentPlaceHolder1$TextBoxInput: 0192023a7bbd73250516f069df18b500
     ctl00$ContentPlaceHolder1$InputHashType: {md5}
     ctl00$ContentPlaceHolder1$Button1: 查询
     ctl00$ContentPlaceHolder1$HiddenFieldAliCode: 
     ctl00$ContentPlaceHolder1$HiddenField1: 
     ctl00$ContentPlaceHolder1$HiddenField2: {val}
    '''.format(vie=get_vie(url),val=get_val(url), md5=md5).strip()
    con = re.findall('(\S+):(\S+)', hed)
    data = dict(con)
    get_data(url, data)
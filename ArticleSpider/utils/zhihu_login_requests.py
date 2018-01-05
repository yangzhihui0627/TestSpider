_author_ = 'young'
import requests
import time
import  os
try:
    from PIL import Image
except:
    pass
try:
    import cookielib
except:
    import http.cookiejar as cookielib
import re
"""
 使用request.session()发请求可以避免每次重新请求新的cookie及session信息，
 提高请求效率。session会自动保存cookie信息便于下次请求使用
"""
session = requests.session()
"""
 由于session.cookies本身没有save方法，因此重写此方法为cookielib.LWPCookieJar后可以
 继承该方法，方便使用cookie操作
"""
session.cookies = cookielib.LWPCookieJar(filename="cookies.txt")
try:
    session.cookies.load(ignore_discard=True)
except:
    print("cookie未能正常加载...")

agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36"
header = {
    "HOST":"www.zhihu.com",
    "Referer":"https://www.zhihu.com",
    "User-Agent":agent
}
def get_index():
    response = session.get("https://www.zhihu.com", headers=header)
    with open("index_page.html","wb") as html:
        html.write(response.text.encode("utf-8"))
    print("ok")
def get_xsrf():
    response = session.get("https://www.zhihu.com",headers=header)
    match_obj = re.match('.*name="_xsrf" value="(.*?)"',response.text)
    if match_obj:
        return  match_obj.group(1)
    else:
        return ""
#获取验证码
def get_capchar():
    t = str(int(time.time()*1000))
    capchar_url = "https://www.zhihu.com/captcha.gif?r="+t+"&type=login&lang=cn"
    r = session.get(capchar_url,headers=header)
    with open("capchar.png","wb") as f:
        f.write(r.content)
        f.close()
    # 用pillow 的 Image 显示验证码
    # 如果没有安装 pillow 到源代码所在的目录去找到验证码然后手动输入
    try:
        img = Image.open("capchar.png")
        img.show()
        img.close()
    except:
        print(u'请到%s目录手动输入'+os.path.abspath("capchar.png"))
    capchar = input("please input the capchar:")
    return capchar

def is_loagin():
    url = "https://www.zhihu.com/settings/profile"
    login_code = session.get(url,allow_redirects=False).status_code
    print(login_code)
def zhihu_login(account,password):
    #知乎登录
    if re.match("yangzhihui0627@126.com",account):
        post_url = "https://www.zhihu.com/login/email"
        """
        _xsrf=1a22194e1f60a14b171ae9d64ebffbda&
        password=zh450371847&
        captcha={"img_size":[200,44],"input_points":[[20.375,22],[136.375,29]]}&
        captcha_type=cn&
        email=yangzhihui0627@126.com
        """
        post_data = {
            '_xsrf':get_xsrf(),
            "email":account,
            "password":password,
            "captcha_type":"cn",
            "capchar":get_capchar()
        }
        response_text = session.post(post_url, data=post_data, headers=header)
        print(response_text.cookies)

        session.cookies.save()
zhihu_login("yangzhihui0627@126.com","zh450371847")
# get_xsrf()
# get_index()
# get_capchar()
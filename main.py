from Tools.client_tools import get_domain
from uvicorn import run
# from web_url import app

if __name__ == '__main__':
    run("main:app", host="192.168.78.120", port=8000, reload=True)
    get_domain.Get_Domain_Save_Main()


    #获得当前主机建立的连接、IP访问日志（log）、维持实时会话表（now）




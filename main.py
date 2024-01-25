from Tools.client_tools import get_domain
def run_cmd_Popen_fileno(cmd_string):
    """
    执行cmd命令，并得到执行后的返回值，python调试界面输出返回值
    :param cmd_string: cmd命令，如：'adb devices'
    :return:
    """
    import subprocess

    print('运行cmd指令：{}'.format(cmd_string))
    return subprocess.Popen(cmd_string, shell=True, stdout=None, stderr=None).wait()

if __name__ == '__main__':
    print("正在获取当前连接")
    a = "cd web_url && uvicorn app:app --reload --host 192.168.78.71 --port 8000"

    run_cmd_Popen_fileno(a)
    #获得当前主机建立的连接、IP访问日志（log）、维持实时会话表（now）
    get_domain.Get_Domain_Save_Main()



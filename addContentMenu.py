# coding:utf-8
import _winreg as reg
def add_hello_context_menu():
    '''
    添加右键菜单，打印'Hello World'
    :return:
    '''
    # 菜单名称，如果含有中文，需要采用GBK编码格式，否则会出现乱码
    menu_name = '批量添加'.decode('utf-8').encode('gbk')
    # 点击菜单所执行的命令
    menu_command = 'python ./add.py'

    # 打开名称为'HEKY_CLASSES_ROOT\\Directory\\Background\\shell'的注册表键，第一个参数为key，第二个参数为sub_key
    # 函数原型：OpenKey(key, sub_key, res = 0, sam = KEY_READ)
    # 注：路径分隔符依然要使用双斜杠'\\'
    key = reg.OpenKey(reg.HKEY_CLASSES_ROOT, r'Directory\\Background\\shell')

    # 为key创建一个名称为menu_name的sub_key，并设置sub_key的值为menu_name，数据类型为REG_SZ即字符串类型，后面跟的'(&H)'表示执行该sub_key的快捷键
    # 函数原型：SetValue(key, sub_key, type, value)
    reg.SetValue(key, menu_name, reg.REG_SZ, menu_name + '(&H)')

    # 打开刚刚创建的名为menu_name的子键
    sub_key = reg.OpenKey(key, menu_name)
    # 为sub_key添加名为'command'的子键，并设置其值为menu_command，数据类型为REG_SZ字符串类型
    reg.SetValue(sub_key, 'command', reg.REG_SZ, menu_command)

    # 关闭sub_key和key
    reg.CloseKey(sub_key)
    reg.CloseKey(key)

if __name__ == '__main__':
    add_hello_context_menu()
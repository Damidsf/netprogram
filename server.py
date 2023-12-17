"""
我真诚地保证：
我自己独立地完成了整个程序从分析、设计到编码的所有工作。
我的程序里中凡是引用到其他程序或文档之处，
例如教材、课堂笔记、网上的源代码以及其他参考书上的代码段,
我都已经在程序的注释里很清楚地注明了引用的出处。
我从未没抄袭过别人的程序，也没有盗用别人的程序，
不管是修改式的抄袭还是原封不动的抄袭。
我编写这个程序，从来没有想过要去破坏或妨碍其他计算机系统的正常运转。 
周宁， 陈邵颂
"""
import socket
import datetime

MAX_BYTES = 65535
ADDRESS = "127.0.0.1"
PORT = 1600

# 选项菜单
def menu(sock, Users_message):
    while True:
        data, address = sock.recvfrom(MAX_BYTES)
        # print(data,address)
        text_list = data.decode("ascii").split("  ")

        if int(text_list[0]) == 1:
            # 注册
            Register(sock, Users_message, text_list, address)
        if int(text_list[0]) == 2:
            # 登陆
            Login(sock, Users_message, text_list, address)
        if int(text_list[0]) == 3:
            # 公聊
            Public_chat(sock, Users_message, text_list)
        if int(text_list[0]) == 4:
            # 私聊
            Private_chat(sock, Users_message, text_list, address)
        if int(text_list[0]) == 5:
            # 退出
            Exit(sock, Users_message, text_list)


# 注册
def Register(sock, Users_message, text_list, address):
    name = text_list[1]
    password = text_list[2]
    if name in Users_message.keys():
        sock.sendto("Error_UserExist".encode("ascii"), address)
        # print(Users_message)
    else:
        Users_message[name] = [password, address]
        # print(Users_message[name])
        print(name + " 成功进入房间")
        sock.sendto("OK".encode("ascii"), address)


# 登陆
def Login(sock, Users_message, text_list, address):
    name = text_list[1]
    password = text_list[2]
    if name in Users_message.keys():
        if Users_message[name][0] == password:
            sock.sendto("OK".encode("ascii"), address)
            Users_message[name] = [password, address]
            print(name + " 成功进入房间\n")
        else:
            sock.sendto("Error_PasswordError".encode("ascii"), address)
    else:
        sock.sendto("Error_UserNotExist".encode("ascii"), address)


# 公聊
def Public_chat(sock, Users_message, text_list):
    name = text_list[1]
    message = text_list[3]
    data = "public-[" + name + "]:" + message
    for user in Users_message.keys():
        if user != name:
          sock.sendto(data.encode('ascii'), Users_message[user][1])
    print("[" + str(datetime.datetime.now()) + "]" + "[" + name + "]:" + message)


# 私聊
def Private_chat(sock, Users_message, text_list, address):
    name = text_list[1]
    message = text_list[3]
    Destination = text_list[4]
    flag = False
    for user in Users_message.keys():
        if user == Destination:
            flag = True
            data = "private-[" + name + "]:" + message
            sock.sendto(data.encode("ascii"), Users_message[user][1])
            print(f"{name}私聊发送成功")
    if not flag:
        print(f"{name}私聊发送失败")


# 退出程序
def Exit(sock, Users_message, text_list):
    name = text_list[1]
    address = text_list[2]
    # print(address)
    data = "exit"
    for user in Users_message.keys():
        if name == user:
            sock.sendto(data.encode("ascii"), Users_message[user][1])
            print(name + " 成功退出房间\n")


# 套接字连接
def main():
    # 用户信息存在字典中，实现可持久化存储可将用户信息写入txt等文本内
    Users_message = {}
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # UDP Socket
    sock.bind((ADDRESS, PORT))
    # socket listen to (ADDRESS,PORT) ipv4
    print("listen to {}".format(sock.getsockname()))
    menu(sock, Users_message)


if __name__ == "__main__":
    main()

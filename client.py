import socket
import sys
from multiprocessing import Process
import os

MAX_BYTES = 65535
ADDRESS = '127.0.0.1'
PORT = 1600


# 将注册或者登陆信息打包发送给服务器端
def Person_Message(sock, choice):
    name = input('请输入用户名:')
    password = input('请输入密码:')
    text = str(choice) + '  ' + name + '  ' + password
    data = text.encode('ascii')
    sock.sendto(data, (ADDRESS, PORT))
    data, address = sock.recvfrom(MAX_BYTES)
    return data.decode('ascii'), name, address


# 将用户聊天信息传送给公共频道
def Chat_Message(sock, name, address):
    print('请输入聊天内容:\n\n(输入 \033[1;44mExit\033[0m 退出,\n'
          '输入 \033[1;44ms/用户名/消息\033[0m 私聊)\t\t\t消息历史:')
    # 创建进程，父进程发送消息，子进程接受消息
    p = Process(target=rcvmsg, args=(sock, name, address))
    p.start()
    sendmsg(sock, name, address)


# 发送消息
def sendmsg(sock, name, address):
    while True:
        message = input()
        Words = message.split('/')

        if Words[0] == 's':
            if (len(Words) <= 2):
                print("请输入正确的私聊格式")
                continue
            Destination = Words[1]
            true_message = Words[2]
            text = '4' + '  ' + name + '  ' + str(address) + '  ' + true_message + '  ' + Destination
            data = text.encode('ascii')
            sock.sendto(data, (ADDRESS, PORT))
            print('OK!')
        elif message == 'Exit':
            text = '5' + '  ' + name + '  ' + str(address)
            data = text.encode('ascii')
            sock.sendto(data, (ADDRESS, PORT))
            sys.exit('您已成功退出房间\n')
        else:
            text = '3' + '  ' + name + '  ' + str(address) + '  ' + message
            data = text.encode('ascii')
            sock.sendto(data, (ADDRESS, PORT))


# 接收消息
def rcvmsg(sock, name, address):
    while True:
        data, address = sock.recvfrom(MAX_BYTES)
        message = data.decode('ascii')
        if message == 'exit':
            os._exit(0)
        else:
            print('\t\t\t\t\t\t' + message)


# 套接字连接
def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        while True:
            choice = int(input('请选择:\n 1、注册 2、登录\n'))
            if choice == 1 or choice == 2:
                break
            print('错误命令')
        # signal标识注册或者登陆时返回的值
        signal, name, address = Person_Message(sock, choice)
        print("标识: ", signal, "  用户名： ", name, "  地址：  ", address)
        if signal == 'OK':
            os.system("cls")
            print('您已成功进入公聊房间')
            break
        elif signal == 'Error_UserExist':
            print('该用户已存在')
        elif signal == 'Error_PasswordError':
            print('密码错误')
        elif signal == 'Error_UserNotExist':
            print('用户名不存在')
    Chat_Message(sock, name, address)


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
功能：第三方工具检测恶意域名客户端
作者：吴晓宝
日期:2018-2-5
"""

from socket import socket,AF_INET, SOCK_STREAM,error

def get_detect_result(domain,server_ip,port):

    try:
        client = socket(AF_INET, SOCK_STREAM)
    except error, e:
        print e
        return "连接异常"
    else:
        addr = (server_ip, port)
        try:
            client.connect(addr)
        except error, e:
            print e
            return "连接异常"
        else:
            result = ''
            while True:
                try:
                    client.sendall(domain)
                    buf = client.recv(2048)
                    result += buf
                except error, e:
                    print e
                    return "连接异常"
                else:
                    if not buf:
                        break
    return result

if __name__ == "__main__":
    pass
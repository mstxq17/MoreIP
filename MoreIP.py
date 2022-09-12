#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2022/9/9 3:13 PM
# @Author : xq17
# @FileName : MoreIP.py
# @Software: PyCharm

__version__ = "2.0"

import re
import socket
import ipaddress
from argparse import ArgumentParser


class Utils:
    """Provide the common function
    提供常用功能函数

    Returns:
        Utils class object
    """

    @staticmethod
    def check_domain(target: str) -> bool:
        """Check the type of target is domain or not
        检查目标类型是否为域名
        :param target: 待检测字符串
        :return: bool
        """
        domain_pattern = re.compile(r"^((?!-)[A-Za-z0-9-]{1,63}(?<!-)\.)+[a-zA-Z]{2,24}$")
        if domain_pattern.match(target):
            return True
        else:
            return False

    @staticmethod
    def check_ipv4(ip: str) -> bool:
        """Check the type of ip is ip or not
        检查变量ip是否为ip类型
        :param ip: 待检测的ip字符串
        :return: bool
        """
        try:
            ipaddress.IPv4Address(ip)
            return True
        except ValueError:
            return False

    @staticmethod
    def get_decimal_ipv4(ipv4: str) -> str:
        """Convert the ip to decimal ipv4, understand easily for human
        转换ip地址为十进制，方便给人看
        :param ipv4:
        :return: decimal ipv4 address
        """
        pass


class MoreIp(object):
    """The Core function provider class, support to do more than one difference dns query
    for specify domain/ip, and get the address of the correlation of ip.
    提供核心功能类，提供对目标域名/IP进行多地DNS查询并解析出对应IP的归属地的功能。

    Args:
        :attribute target:
        :attribute type:
        :attribute detail:

    Returns:
        MoreIp class object
    """

    def __init__(self, target: str) -> None:
        self.target: str = target
        self.type: str = ""
        self.detail: dict = dict()

    # Inspiration from https://www.cnblogs.com/baxianhua/p/10845620.html
    @classmethod
    def check_type(cls, target: str) -> str:
        domain_pattern = r"^((?!-)[A-Za-z0-9-]{1,63}(?<!-)\.)+[a-zA-Z]{2,24}$"
        ipv4_pattern = ipaddress.IPv4Address(target)

    @staticmethod
    def check_domain(domain: str) -> str:
        """get the result of dns query  from local hosts file and local dns server
        step 1: 获取本地的域名解析结果，来源hosts文件，自带dns服务器解析结果。
        step 2: 伪造 ens-client-subnet 来源ip, 从而

        :param domain: 查询的域名
        :return:
        """
        local_ip = socket.gethostbyname(domain)
        print(local_ip)

    def check_ip(self, ip: str) -> str:
        pass

    def run(self) -> None:
        pass


def parse_args():
    parser = ArgumentParser()
    # target, handled by the core function
    # 目标传入核心处理逻辑进行处理
    parser.add_argument("target", help="specified ip or domain", type=str)
    # 显示更多脚本处理的细节内容
    parser.add_argument("--verbose", help="increase output verbosity",
                        action="store_true")
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    if args.target:
        pass


if __name__ == '__main__':
    main()

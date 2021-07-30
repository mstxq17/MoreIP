#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import sys
import re
import ipaddress
import requests
import subprocess
import asyncio
import aiohttp
import json


class Utils:
    """some functions"""
    @staticmethod
    def check_valid_ipv4(ip):
        try:
            ipaddress.IPv4Address(ip)
            return True
        except ValueError:
            return False

    @staticmethod
    def check_valid_domain(domain):
        pattern = re.compile(
            r"[a-zA-z0-9][-a-zA-z0-9]{0,62}(\.[a-zA-z0-9][-a-zA-z0-9]{0,62})+[a-z]{1,}$")
        if pattern.match(domain):
            return True
        else:
            return False

    @staticmethod
    def check_cidr_ips(ips):
        pattern = re.compile(r"/\d{0,2}")
        if pattern.search(ips):
            try:
                ips = ipaddress.IPv4Network(ips, strict=False)
                return True
            except ValueError:
                pass
        return False

    @staticmethod
    def output(result):
        if isinstance(result, list):
            for item in result:
                if isinstance(item, str):
                    print(item)
                if isinstance(item, dict):
                    for k, v in item.items():
                        print("{k}: {v}".format(k=k, v=v))
                    print("\n")
        if isinstance(result, dict):
            for k, v in result.items():
                print("{k}: {v}".format(k=k, v=v))


class MoreIP:
    """core class"""

    def __init__(self, config):
        self.ip_api = config["ip_api"]
        self.ping_api = config["ping_api"]

    @staticmethod
    def parse_args():
        options = {}
        # only support IPv4 format
        if len(sys.argv) <= 1:
            # check local ip
            options["local"] = True
        else:
            # one target
            target = sys.argv[1]
            if Utils.check_valid_ipv4(target):
                options["ip"] = target
            if Utils.check_valid_domain(target):
                options["domain"] = target
            if Utils.check_cidr_ips(target):
                options["cidr"] = target
        return options

    def check_ip(self, ip=None, mode="local"):
        headers = {"User-Agent": "curl/7.64.1"}
        query_local = self.ip_api
        query_external = self.ip_api + str(ip).replace("'", "")
        if mode == "local":
            try:
                # local_ip = subprocess.
                resp_text = requests.get(
                    query_local, headers=headers, timeout=5).text
                resp_curl = subprocess.getoutput(
                    "curl -s {}".format(query_local))
                result_text = list(
                    filter(None, resp_text.replace('\t', '').split('\n')))
                result_curl = list(
                    filter(None, resp_curl.replace('\t', '').split('\n')))
                result = list(dict.fromkeys(
                    result_text + ['\n'] + result_curl))
                return result
            except Exception as e:
                print(e)
        if mode == "extern":
            result = {}
            try:
                resp_text = requests.get(
                    query_external, headers=headers, timeout=5).text
                resp_curl = subprocess.getoutput(
                    "curl -s '{}'".format(query_external))
                result_text = list(
                    filter(None, resp_text.replace('\t', '').split('\n')))
                result_curl = list(
                    filter(None, resp_curl.replace('\t', '').split('\n')))
                result = list(dict.fromkeys(result_text + ['\n']+result_curl))
                return result
            except Exception as e:
                print(e)

    def check_domain(self, domain):
        try:
            headers = {
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
            }
            data = {
                "host": domain,
                "node": 1
            }
            resp = requests.post(self.ping_api, data=data, headers=headers)
            data_ids = re.findall('data-id="(.*?)">', resp.text)
            if len(data_ids) > 0:
                tasks = [self.ping(data_id, domain) for data_id in data_ids]
                event_loop = asyncio.get_event_loop()
                results = [json.loads(r)["data"] for r in event_loop.run_until_complete(
                    asyncio.gather(*tasks))]
                event_loop.close()
                return results
        except Exception as e:
            print(e)

    async def ping(self, data_id, domain):
        headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
        }
        data = {
            "node": data_id,
            "host": domain
        }
        request_url = self.ping_api + "check-ping.html"
        async with aiohttp.request("POST", request_url, headers=headers, data=data) as r:
            response = await r.text(encoding="utf-8")
            print(response)
            return response


def main():
    options = MoreIP.parse_args()
    config = {
        # quering ip address API
        "ip_api": "http://www.cip.cc/",
        # ping ip address API
        "ping_api": "https://www.wepcc.com:443/",
    }
    moreIp = MoreIP(config)
    if options.get("local"):
        result = moreIp.check_ip(mode="local")
        Utils.output(result)

    if options.get("ip"):
        result = moreIp.check_ip(ip=options.get("ip"), mode="extern")
        Utils.output(result)
    if options.get("domain"):
        result = moreIp.check_domain(domain=options.get("domain"))
        Utils.output(result)


if __name__ == '__main__':
    main()

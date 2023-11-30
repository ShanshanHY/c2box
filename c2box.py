import os
import json
import yaml
import requests
from urllib.parse import unquote, urlparse
import convert


def build_outbound(clash_subs_list):
    outbounds = {"outbounds": [
            {"type": "selector", "tag": "订阅选择", "outbounds": [f"订阅自动"],
             "interrupt_exist_connections": False},
            {"type": "urltest", "tag": f"订阅自动", "outbounds": [],
             "interrupt_exist_connections": False}]}
    for clash_sub in clash_subs_list:
        try:
            req = requests.get(url=clash_sub, headers={'User-Agent': 'clashmeta'})
            clash_sub_name = unquote(req.headers.get("content-disposition"))
            if clash_sub_name:
                clash_sub_name = clash_sub_name.split("''")[1]
            else:
                clash_sub_name = urlparse(clash_sub).netloc
            clash_sub_proxies = yaml.load(req.text, Loader=yaml.FullLoader)["proxies"]
        except Exception:
            print(f"获取订阅链接[{clash_sub}]失败，请检查后重试")
            continue
        if len(clash_sub_proxies) == 0:
            print(f"订阅链接[{clash_sub}]内无有效节点，跳过生成")
            continue
        print(f"成功获取订阅[{clash_sub_name}]，正在生成出站列表")
        outbounds["outbounds"][0]["outbounds"].append(clash_sub_name)
        outbounds["outbounds"][1]["outbounds"].append(clash_sub_name)
        outbounds_list = [
            {"type": "selector", "tag": clash_sub_name, "outbounds": [f"[{clash_sub_name}]自动选择"],
             "interrupt_exist_connections": False},
            {"type": "urltest", "tag": f"[{clash_sub_name}]自动选择", "outbounds": [],
             "interrupt_exist_connections": False}]
        for each_proxy in clash_sub_proxies:
            outbound = dict()
            outbound["tag"] = f"[{clash_sub_name}]{each_proxy["name"]}"
            # if each_proxy.get("dialer-proxy"):
            #     outbound["detour"] = f"[{clash_sub_name}]{each_proxy.get("dialer-proxy")}"
            outbound_convert = convert.proxy(each_proxy)
            if outbound_convert:
                outbound.update(outbound_convert)
            else:
                print(f"跳过转换[{clash_sub_name}]{each_proxy["name"]}")
                continue
            outbounds_list[0]["outbounds"].append(f"[{clash_sub_name}]{each_proxy["name"]}")
            outbounds_list[1]["outbounds"].append(f"[{clash_sub_name}]{each_proxy["name"]}")
            outbounds_list.append(outbound)
        outbounds["outbounds"].extend(outbounds_list)
        print(f"[{clash_sub_name}]转换完成，共转换了{len(outbounds["outbounds"])}条协议")
    outbounds["outbounds"] += [
        {"type": "direct", "tag": "direct"},
        {"type": "block", "tag": "block"},
        {"type": "dns", "tag": "dns_out"}]
    return outbounds


def main():
    clash_subs = input("输入订阅链接，多条订阅使用 | 隔开")
    clash_subs_list = clash_subs.split("|")

    template_list = os.listdir("./template")
    if len(template_list) == 0:
        print("未找到模板文件，仅生成outbounds")
        template = dict()
    else:
        if len(template_list) > 1:
            print("找到多个模板文件，请选择需要的模板：")
            while True:
                for i, each in enumerate(template_list):
                    print(f"{i}. {each}")
                try:
                    template_name = template_list[int(input("请输入模板序号: "))]
                    break
                except ValueError:
                    print("错误的输入!")
                except IndexError:
                    print("序号不存在!")
        else:
            template_name = template_list[0]
        try:
            with open(f"./template/{template_name}", "r", encoding="UTF-8") as f:
                template = json.load(f)
        except json.decoder.JSONDecodeError:
            print(f"模板文件 {template_name} 格式错误！")
            exit(1)
        print(f"已加载模板文件 {template_name}")

    outbounds = build_outbound(clash_subs_list)
    sing_box_conf = convert.base.merge_dict(template, outbounds)
    with open("./output/config.json", 'w', encoding="UTF-8") as f:
        json.dump(sing_box_conf, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()

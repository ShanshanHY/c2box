import convert.base as base


def convert(proxy):
    outbound = dict()
    for key, value in proxy.items():
        if key == "type":
            entry = {"type": "socks", "version": "5"}

        # 提前处理tls
        elif key == "tls":
            if value:
                print(f"不支持的协议：{proxy.get("name")}.socks-tls")
                return False
            else:
                continue
        elif key == "skip-cert-verify":
            print(f"不支持的协议：{proxy.get("name")}.socks-tls")
            return False

        elif key in base.common_list:
            entry = base.convert(key, value)
        elif key in base.ignore_list:
            continue

        else:
            print(f"不支持的配置词条: {proxy.get("name")}.{key}")
            return False

        outbound = base.merge_dict(outbound, entry)
    return outbound




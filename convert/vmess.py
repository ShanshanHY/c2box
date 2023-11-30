import convert.base as base


def convert(proxy):
    outbound = dict()
    for key, value in proxy.items():
        entry = dict()
        if key == "type":
            entry = {"type": "vmess"}

        # 提前处理cipher加密方法
        elif key == "cipher":
            entry = {"security": value}

        elif key in base.common_list:
            entry = base.convert(key, value)
        elif key in base.ignore_list:
            continue

        elif key == "alterId":
            entry = {"alter_id": value}
        elif key == "network":
            entry = base.v2ray_transport(proxy)
            if not entry:
                print(f"不支持的配置词条: {proxy.get("name")}.{key}")
                return False
        elif key in ["ws-opts", "h2-opts", "http-opts", "grpc-opts"]:
            continue

        else:
            print(f"不支持的配置词条: {proxy.get("name")}.{key}")
            return False

        outbound = base.merge_dict(outbound, entry)
    return outbound

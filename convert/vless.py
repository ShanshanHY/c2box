import convert.base as base


def convert(proxy):
    outbound = dict()
    for key, value in proxy.items():
        if key == "type":
            entry = {"type": "vless"}

        elif key in base.common_list:
            entry = base.convert(key, value)
        elif key in base.ignore_list:
            continue

        elif key == "network":
            if value == "tcp":
                continue
            entry = base.v2ray_transport(proxy)
            if not entry:
                print(f"不支持的配置词条: {proxy.get("name")}.{key}")
                return False
        elif key in ["ws-opts", "h2-opts", "http-opts", "grpc-opts"]:
            continue
        elif key == "flow":
            entry = {"flow": value}
        elif key == "xudp":
            if value:
                entry = {"packet_encoding": "xudp"}
            else:
                entry = {"packet_encoding": ""}

        elif key == "reality-opts":
            entry = reality(proxy)

        else:
            print(f"不支持的配置词条: {proxy.get("name")}.{key}")
            return False

        outbound = base.merge_dict(outbound, entry)
    return outbound


def reality(proxy):
    outbound = {"tls": {"enabled": True, "reality": {"enabled": True}}}
    for key, value in proxy["reality-opts"].items():
        if key == "public-key":
            entry = {"tls": {"reality": {"public_key": value}}}
        elif key == "short-id":
            entry = {"tls": {"reality": {"short_id": value}}}
        else:
            return False
        outbound = base.merge_dict(outbound, entry)
    return outbound


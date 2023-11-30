import convert.base as base


def convert(proxy):
    outbound = dict()
    for key, value in proxy.items():
        if key == "type":
            entry = {"type": "wireguard"}

        elif key in base.common_list:
            entry = base.convert(key, value)
        elif key in base.ignore_list:
            continue

        elif key == "private-key":
            entry = {"private_key": value}
        elif key in ["ip", "ipv6"]:
            if "/" in value:
                entry = {"local_address": [value]}
            else:
                ip = f"{value}/32" if key == "ip" else f"{value}/128"
                entry = {"local_address": [ip]}
        elif key == "public-key":
            entry = {"peer_public_key": value}
        elif key == "pre-shared-key":
            entry = {"pre_shared_key": value}
        elif key == "reserved":
            entry = {"reserved": value}
        elif key == "mtu":
            entry = {"mtu": value}
        elif key in ["allowed-ips", "remote-dns-resolve", "dns"]:
            continue

        else:
            print(f"不支持的配置词条: {proxy.get("name")}.{key}")
            return False

        outbound = base.merge_dict(outbound, entry)
    return outbound




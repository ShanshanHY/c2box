common_list = ["server", "port", "username", "password", "cipher", "password", "udp",
               "udp-over-tcp", "udp-over-tcp-version", "ip-version", "interface-name",
               "routing-mark", "client-fingerprint", "sni", "servername", "uuid",
               "skip-cert-verify", "alpn", "ca", "ca-str", "ws-path", "ws-headers"]
ignore_list = ["name", "dialer-proxy", "fingerprint", "tls"]


def convert(key, value):
    if key == "server":
        return {"server": value}
    elif key == "port":
        return {"server_port": value}
    elif key == "cipher":
        return {"method": value}
    elif key == "username":
        return {"username": value}
    elif key == "password":
        return {"password": value}
    elif key == "udp":
        return {} if value else {"network": "tcp"}
    elif key == "udp-over-tcp":
        return {"udp_over_tcp": {"enabled": True}} if value else {}
    elif key == "udp-over-tcp-version":
        return {"udp_over_tcp": {"version": value}}
    elif key == "ip-version":
        if value == "ipv4":
            return {"domain_strategy": "ipv4_only"}
        elif value == "ipv4-prefer":
            return {"domain_strategy": "prefer_ipv4"}
        elif value == "ipv6":
            return {"domain_strategy": "ipv6_only"}
        elif value == "ipv6-prefer":
            return {"domain_strategy": "prefer_ipv6"}
    elif key == "interface-name":
        return {"bind_interface": value}
    elif key == "routing-mark":
        return {"routing_mark": value}
    elif key == "client-fingerprint":
        return {"tls": {"enabled": True, "utls": {"enabled": True, "fingerprint": value}}}
    elif key in ["sni", "servername"]:
        return {"tls": {"enabled": True, "server_name": value}}
    elif key == "uuid":
        return {"uuid": value}
    elif key == "skip-cert-verify":
        return {"tls": {"enabled": True, "insecure": value}}
    elif key == "alpn":
        return {"tls": {"enabled": True, "alpn": value}}
    elif key == "ca":
        return {"tls": {"enabled": True, "certificate_path": value}}
    elif key == "ca-str":
        return {"tls": {"enabled": True, "certificate": value}}

    # 过时的ws协议兼容
    elif key == "ws-path":
        return {"transport": {"path": value}}
    elif key == "ws-headers":
        return {"transport": {"headers": value}}


def merge_dict(base_dict, new_dict):
    for key, value in new_dict.items():
        if key in list(base_dict):
            if isinstance(value, dict) and isinstance(base_dict.get(key), dict):
                base_dict[key] = merge_dict((base_dict[key]), value)
            elif isinstance(value, list) and isinstance(base_dict.get(key), list):
                base_dict[key].append(value)
        else:
            base_dict[key] = value
    return base_dict


def v2ray_transport(proxy):
    transport_type = proxy.get("network")
    if transport_type in ["h2", "http"]:
        transport = {"transport": {"type": "http"}}
        transport = merge_dict(transport, {"transport": {proxy.get("h2-opts")}})
        return transport
    elif transport_type == "grpc":
        transport = {"transport": {"type": "grpc"}}
        opts = proxy.get("grpc-opts")
        for key, value in opts.items():
            if key == "grpc-service-name":
                entry = {"transport": {"service_name": value}}
            else:
                return False
            transport = merge_dict(transport, entry)
        return transport
    elif transport_type == "ws":
        transport = {"transport": {"type": "ws"}}
        opts = proxy.get("ws-opts")
        for key, value in opts.items():
            if key == "path":
                entry = {"transport": {"path": value}}
            elif key == "headers":
                entry = {"transport": {"headers": value}}
            elif key == "max-early-data":
                entry = {"transport": {"max_early_data": value}}
            elif key == "early-data-header-name":
                entry = {"transport": {"early_data_header_name": value}}
            elif key == "v2ray-http-upgrade":
                print(f"http升级暂不支持: {proxy.get("name")}")
                return False
            else:
                return False
            transport = merge_dict(transport, entry)
        return transport


def smux(proxy):
    entry = dict()
    for key, value in proxy.get("smux").item():
        if key in ["enable", "protocol", "max_connections",
                   "min_streams", "max_streams", "padding"]:
            entry[key] = value
        elif key == "brutal-opts":
            entry["brutal"] = value
        else:
            print(f"忽略转换 smux.{key}")
    return entry

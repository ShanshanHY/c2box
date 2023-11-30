import convert.base as base


def convert(proxy):
    outbound = {"congestion_control": "bbr"}
    for key, value in proxy.items():
        if key == "type":
            entry = {"type": "tuic"}

        elif key in base.common_list:
            entry = base.convert(key, value)
        elif key in base.ignore_list:
            continue

        elif key == "ip":
            continue
        elif key == "heartbeat-interval":
            entry = {"heartbeat": value}
        elif key == "disable_sni":
            entry = {"tls": {"enabled": True, "disable_sni": value}}
        elif key == "reduce-rtt":
            entry = {"zero_rtt_handshake": value}
        elif key == "request-timeout":
            entry = {"connect_timeout": value}
        elif key == "udp-relay-mode":
            entry = {"udp_relay_mode": value}
        elif key == "congestion-controller":
            entry = {"congestion_control": value}
        elif key == "fast-open":
            entry = {"tcp_fast_open": value}

        else:
            print(f"不支持的配置词条: {proxy.get("name")}.{key}")
            return False

        outbound = base.merge_dict(outbound, entry)
    return outbound




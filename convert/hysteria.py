import convert.base as base


def convert(proxy):
    outbound = {}
    for key, value in proxy.items():
        entry = dict()
        if key == "type" and value in ["hysteria", "hysteria2"]:
            entry = {"type": value}
        elif key in base.common_list:
            entry = base.convert(key, value)
        elif key in base.ignore_list:
            continue

        # 流控处理
        elif key == "up":
            entry = {"up_mbps": hysteria_cc(value)}
        elif key == "down":
            entry = {"down_mbps": hysteria_cc(value)}

        elif key == "auth":
            entry = {"auth": value}
        elif key in ["auth_str", "auth-str"]:
            entry = {"auth_str": value}

        elif key == "obfs":
            if proxy["type"] == "hysteria":
                entry = {"obfs": value}
            elif proxy["type"] == "hysteria2":
                entry = {"obfs": {"type": value}}
        elif key == "obfs-password":
            entry = {"obfs": {"password": value}}

        elif key == "protocol":
            continue
        elif key == "recv_window_conn":
            entry = {"recv_window_conn": value}
        elif key in ["recv_window_conn", "recv-window-conn"]:
            entry = {"recv_window_conn": value}
        elif key in ["recv_window", "recv-window"]:
            entry = {"recv_window": value}
        elif key == "disable_mtu_discovery":
            entry = {"disable_mtu_discovery": value}
        elif key == "fast-open":
            entry = {"tcp_fast_open": value}

        elif key == "ca_str":
            entry = {"tls": {"enabled": True, "certificate": value}}

        else:
            print(f"不支持的配置词条: {proxy.get("name")}.{key}")
            return False

        outbound = base.merge_dict(outbound, entry)
    return outbound


def hysteria_cc(speed):
    if isinstance(speed, int):
        return speed
    if speed[-3:] in ["bps", "Bps"]:
        if speed[-4] in ["k", "K"]:
            speed_mbps = int(int(speed[:-4]) / 1000)
        elif speed[-4] in ["m", "M"]:
            speed_mbps = int(speed[:-4])
        elif speed[-4] in ["g", "G"]:
            speed_mbps = int(int(speed[:-4]) * 1000)
        elif speed[-4] in ["t", "T"]:
            speed_mbps = int(int(speed[:-4]) * 1000 * 1000)
        else:
            speed_mbps = int(int(speed[:-4]) / 1000 / 1000)
        if speed[-3:] == "Bps":
            speed_mbps = speed_mbps * 8
        return speed_mbps
    else:
        return int(speed)

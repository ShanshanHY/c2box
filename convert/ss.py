import convert.base as base


def convert(proxy):
    outbound = {}
    for key, value in proxy.items():
        if key == "type":
            entry = {"type": "shadowsocks"}
        elif key in base.common_list:
            entry = base.convert(key, value)
        elif key in base.ignore_list:
            continue

        # 插件处理
        elif key == "plugin":
            if value == "shadow-tls":
                entry = shadowtls(proxy)
            elif value == "obfs":
                entry = obfs(proxy)
            elif value == "v2ray-plugin":
                entry = v2ray_plugin(proxy)
            else:
                print(f"不支持的配置词条: {proxy.get("name")}.{key}")
                return False
            if not entry:
                print(f"不支持的配置词条: {proxy.get("name")}.{key}")
                return False
        elif key == "plugin-opts":
            continue

        # 多路复用处理
        elif key == "smux":
            entry = base.smux(proxy)

        else:
            print(f"不支持的配置词条: {proxy.get("name")}.{key}")
            return False

        outbound = base.merge_dict(outbound, entry)
    return outbound


def shadowtls(proxy):
    entry = {"type": "shadowtls"}
    opts = proxy.get("plugin_opts")
    if opts:
        for key, value in opts.items():
            if key == "host":
                entry = base.merge_dict(entry, {"tls": {"enabled": True, "server_name": value}})
            elif key == "password":
                entry = base.merge_dict(entry, {"password": value})
            elif key == "version":
                entry = base.merge_dict(entry, {"version": value})
            else:
                return False
    return entry


def obfs(proxy):
    entry = {"plugin": "obfs-local"}
    parameters = str()
    opts = proxy.get("plugin_opts")
    if opts:
        print(opts)
        for key, value in opts.items():
            if key == "mode":
                parameters += f"obfs={value};"
            elif key == "host":
                parameters += f"obfs-host={value};"
            else:
                return False
    entry["plugin_opts"] = parameters[:-1]
    return entry


def v2ray_plugin(proxy):
    entry = {"plugin": "v2ray-plugin"}
    parameters = str()
    opts = proxy.get("plugin_opts")
    if opts:
        print(opts)
        for key, value in opts.items():
            parameters += f"{key}={value};"
    entry["plugin_opts"] = parameters[:-1]
    return entry




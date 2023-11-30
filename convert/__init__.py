import os

path = os.path.dirname(__file__)
package = os.path.basename(path)
for module in os.listdir(path):
    if module == '__init__.py' or module[-3:] != '.py':
        continue
    __import__(f"{package}.{module[:-3]}")
    print(f"成功载入模块 {module[:-3]}")


def proxy(proxy_conf):
    outbound = eval(proxy_conf.get("type")).convert(proxy_conf)
    tls_statue = proxy_conf.get("tls", "no_tls")
    if outbound and tls_statue != "no_tls":
        outbound = base.merge_dict(outbound, {"tls": {"enabled": tls_statue}})
    return outbound if outbound else False


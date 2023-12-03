import base64
import json
import re
import time
from urllib.parse import urlparse

import json5
import requests
from flask import Flask, render_template, request, abort, Response

import c2box

app = Flask(__name__, template_folder='./html')


@app.route('/')
def run():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def build_url():
    parsed_url = urlparse(request.url)
    url = f"{parsed_url.scheme}://{parsed_url.netloc}/convert?"

    # 处理订阅
    sub = re.split(r"\||\r\n", request.form['sub'])
    for i in sub:
        url += f"sub={i}&"

    # 处理模板
    template = base64.urlsafe_b64encode(request.form['template'].encode()).decode(encoding="utf-8")
    url += f"template={template}&"

    # 处理额外出站组
    outbound_group = base64.urlsafe_b64encode(request.form['outbound_group'].encode()).decode(encoding="utf-8")
    url += f"outbound_group={outbound_group}&"

    return render_template('index.html', url=url[:-1], sub=request.form['sub'],
                           template=request.form['template'], outbound_group=request.form['outbound_group'])


@app.route('/convert')
def convert():

    # 处理订阅链接
    sub = request.args.getlist('sub')
    outbound = c2box.build_outbound(sub)
    if not outbound:
        abort(412, "No available proxy in sub")

    # 处理额外出站分组文件
    if len(request.args.get('outbound_group', [""][0])) > 0:
        try:
            outbound_group = json5.loads(base64.urlsafe_b64decode(request.args.get('outbound_group', [""][0])).decode(encoding="utf-8"))
            outbound = c2box.extra_outbound(outbound, outbound_group)
        except Exception:
            abort(412, "Outbound group get fail")

        # 处理模板文件
    if len(request.args.get('template', [""][0])) > 0:
        template = base64.urlsafe_b64decode(request.args.get('template', [""][0])).decode(encoding="utf-8")
        try:
            if template.startswith("http"):
                template_url = template
                req = requests.get(url=template_url)
                template = json5.loads(req.text)
            else:
                template = json5.loads(template)
            template["outbounds"] = outbound["outbounds"]
            outbound = template
        except Exception:
            abort(412, "Template get fail")

    config_download = json.dumps(outbound, ensure_ascii=False, indent=4)
    response = Response(config_download, content_type="application/json")

    # 自定义下载文件名
    conf_name = request.args.get("conf_name", "")
    if len(conf_name) == 0:
        conf_name = f"config_{str(int(time.time()))}.json"
    response.headers.set("Content-Disposition", f"attachment; filename={conf_name}")
    return response


if __name__ == '__main__':
    app.run(debug=True)

# C2Box
一个将`Clash代理`转换为`Sing-Box出站列表`的Python脚本

A python script to convert `clash proxies` to `sing-box outbounds`

个人使用项目，转换且仅转换`proxies`为`outbounds`

支持`web api`与`本地运行`，支持模板，支持多Clash订阅链接

主要以 ~~clash meta~~ 虚空终端wiki编写，部分协议未经过测试 ~~（没有测试源）~~

转换后的订阅存储为 `订阅选择`-`订阅自动`-`订阅名称`-`[订阅名称]自动`-`[订阅名称]节点名称` 

可自行修改，转换方式位于包 `convert` 中，并且该包不会处理名称，请自行处理

# 演唱会回流票监控程序

基于原作者的优秀项目，新增UUTIX等海外平台支持的多平台回流票监控系统

## 致谢原作者

本项目基于以下原作者的优秀工作：
- **原项目地址**: [ThinkerWen/TicketMonitoring](https://github.com/ThinkerWen/TicketMonitoring)
- **技术分析文章**: 
  - [看雪论坛 - 某麦网回流票监控，sing参数分析](https://bbs.kanxue.com/thread-279165.htm)
  - [吾爱破解 - 某麦网回流票监控，sing参数分析](https://www.52pojie.cn/forum.php?mod=viewthread&tid=1845064)

感谢原作者 **ThinkerWen** 的开源贡献和技术分享！

## 本分支新增功能

在原有大麦、猫眼、纷玩岛、票星球四大平台基础上，新增以下功能：

- 🆕 **UUTIX海外平台支持** - 新增海外票务平台监控
- 🔧 **错误处理优化** - 增强异常处理和日志输出
- 📖 **文档完善** - 补充使用说明和配置指南
- 🛡️ **代码优化** - 改进代码结构和稳定性

## 功能特性

- ✅ 支持大麦网、猫眼、纷玩岛、票星球、UUTIX等多平台监控
- ✅ 实时监控回流票，自动发送邮件通知
- ✅ 支持多演出同时监控
- ✅ 支持代理配置，避免IP被封
- ✅ 容器化部署，开箱即用

## 使用

### 一、源代码

```bash
# 克隆本项目
git clone https://github.com/A11MiND/TicketMonitoring.git
cd TicketMonitoring
# 安装python运行需要的包
python3 -m pip install -r requirements.txt
# 执行程序
python3 start.py
```

### 二、Docker（推荐）

```bash
mkdir /etc/ticket-monitor
vim /etc/ticket-monitor/config.json  # 配置文件见config.json⬆️️
docker run -d --restart=unless-stopped -v /etc/ticket-monitor/config.json:/app/config.json --name="ticket-monitor" designerwang/ticket-monitor:latest
```

## 添加监控演出

添加新的演出监控请在`config.json`中配置：

| 字段名       | 含义      | 备注                                                                       |
|-----------|---------|--------------------------------------------------------------------------|
| show_id   | 演出id    | 通过抓包获取，找到类似于`perfromId` `projectId` `showId` 等的关键字即可                     |
| show_name | 演出名称    | 可以任意填写，自己好记即可                                                            |
| platform  | 演出的监控平台 | 和`show_id`的平台对应，`platform`参照：(`大麦: 0` `猫眼: 1` `纷玩岛: 2` `票星球: 3` `UUTIX: 4`) |
| deadline  | 监控的截止时间 | 截止时间内进行监控，超过截止时间则停止监控,需按照`2000-01-01 00:00:00`格式填写                       |

## 新增功能

### UUTIX平台监控（新增）

- 新增支持UUTIX海外票务平台监控
- 通过抓包获取`MY_` 开头的token实现认证
- 支持演唱会、话剧等多种演出类型的票务监控

### Token获取方法

1. **猫眼平台**: 登录猫眼小程序后抓包获取token
2. **UUTIX平台**: 登录UUTIX网站后按F12开发者工具，在Application/Storage中查找cookie获取token

## 注意事项

- 程序仅供学习研究，请勿用于违法活动中，如作他用所承受的法律责任一概与作者无关
- 编程能力有限，代码仅供参考 ^_^
- 使用前请正确配置`config.json`中的token和监控信息
- 请尊重原作者的知识产权，合理使用开源代码

## 再次致谢

特别感谢原作者 **ThinkerWen** 的开源精神和技术贡献！

本项目在原有优秀基础上进行功能扩展，如有任何问题或建议，欢迎交流讨论。

---

**原始项目来源**: [ThinkerWen/TicketMonitoring](https://github.com/ThinkerWen/TicketMonitoring)

**本分支维护者**: A11MiND

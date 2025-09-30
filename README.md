# 演唱会回流票监控程序

## 原项目介绍

本项目 fork 自 [ThinkerWen/TicketMonitoring](https://github.com/ThinkerWen/TicketMonitoring)

原作者 **ThinkerWen** 通过逆向分析实现了大麦、猫眼、纷玩岛、票星球等主流平台的回流票监控，并分享了详细的技术分析：
- [看雪论坛 - 某麦网回流票监控，sing参数分析](https://bbs.kanxue.com/thread-279165.htm)
- [吾爱破解 - 某麦网回流票监控，sing参数分析](https://www.52pojie.cn/forum.php?mod=viewthread&tid=1845064)

## 本 Fork 说明

在原项目基础上新增了 UUTIX 海外票务平台的监控支持。

## 使用方法

```bash
git clone https://github.com/A11MiND/TicketMonitoring.git
cd TicketMonitoring
python3 -m pip install -r requirements.txt
# 配置 config.json 中的 token 和监控信息
python3 start.py
```

## 配置说明

在 `config.json` 中配置监控演出：

| platform | 平台 |
|----------|------|
| 0 | 大麦 |
| 1 | 猫眼 |
| 2 | 纷玩岛 |
| 3 | 票星球 |
| 4 | UUTIX |

## 免责声明

程序仅供学习研究，请勿用于违法活动。

---

**原项目**: [ThinkerWen/TicketMonitoring](https://github.com/ThinkerWen/TicketMonitoring)  
**本 Fork**: A11MiND

# LXNSProvider

实现：ISongProvider, IPlayerProvider, IScoreProvider, IAliasProvider

源站：https://maimai.lxns.net/

申请开发者Token：https://maimai.lxns.net/developer

开发者交流群：991669419

## 关于开发者Token

落雪的开发者Token仅在以下场景是必须提供的：

- 获取玩家信息
- 获取玩家的B50成绩 (ScoreKind.BEST)
- 获取玩家的所有成绩 (ScoreKind.ALL)
- 更新玩家分数

建议始终提供落雪的开发者Token，落雪的大部分操作都需要开发者Token。

## 关于别名数据源

落雪自身有提供别名数据源 (IAliasProvider)，不过数据可能没有Yuzu全，还是推荐使用Yuzu的。

## 关于隐私设置

通过落雪获取或上传信息时，需要玩家同意落雪的隐私设置，否则会抛出隐私异常

![Snipaste_2024-12-21_12-52-35.png](https://s2.loli.net/2024/12/21/EcjIO8eDuWvQotB.png)
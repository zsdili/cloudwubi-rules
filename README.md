# CloudWubi Rules — 去中心化五笔规则库

> 面向 5G/6G 的云原生五笔输入法 · 语言资源组件
> **全球社区共建的公共语言资产** · CC-BY 4.0 · CI 自动文法校验

## 简介

本仓库是 CloudWubi 云五笔的**核心语言资源库**，存放五笔拆字编码、构词文法、测试用例。
**这是去中心化共建的公共资产**：任何志愿者可提交拆字修正、生僻字、行业词汇，
经 CI 自动文法校验后并入主库，不存在单一厂商锁定。

## 与代码仓库的关系

```
cloudwubi-rules（本仓库：语言资源）
    │ 编码表、构词文法
    ▼
cloudwubi-gateway（云端：加载规则库 → 查询/构词）
    ▼
cloudwubi-client（端侧：<800KB 极简内核，不携带字库）
```

> 关键设计：**字库与代码彻底分离**。程序可以无限升级，语言资源由社区持续共建，互不阻塞。

## 数据文件格式

每行一条记录，`#` 开头为注释：

```
编码 汉字 [汉字...]
```

示例：
```
wq  你 您
g   一
gggg 王
```

## 文件

| 文件 | 内容 | 状态 |
| ---- | ---- | ---- |
| `wubi86_basic.txt` | 基础 86 五笔编码表（一级简码等） | ✅ 当前 |
| `rule_verify.py` | 自动校验器（CI 核心程序） | ✅ 完成 |
| `.github/workflows/rule-verify.yml` | CI 流水线 | ✅ 完成 |

## 自动校验规则（CI 强制执行）

`rule_verify.py` 自动检查：

1. 编码必须为 1~4 位小写字母 a~y
2. 每行至少 1 个汉字
3. 汉字必须是合法 CJK 字符
4. 编码不得重复（重码请合并到同一行）
5. 非法条目直接拦截，无法合并进主库

```bash
# 本地运行校验器
python3 rule_verify.py wubi86_basic.txt
# ✅ 校验通过  /  ❌ 发现 N 个问题（退出码非0）
```

## 如何贡献（去中心化共建流程）

1. Fork 本仓库
2. 修改 `wubi86_basic.txt` 或新增行业词库文件
3. 提交 Pull Request
4. **CI 自动文法校验** → 社区评审 → 合并入主库
5. 合并后自动同步到 Gitee 镜像

## 阶段规划

| 阶段 | 内容 | 状态 |
| ---- | ---- | ---- |
| 1 | 基础高频字（一级简码） | ✅ 完成 |
| 2 | 完整 86 五笔码表 | 📋 规划 |
| 3 | 行业专业词库（创业BP、编程、法律等） | 📋 规划 |
| 4 | 生僻字、异体字、多语种混合 | 📋 规划 |

## 授权

- **CC-BY 4.0**：可自由复制、分发、修改，保留署名即可
- 完整协议：https://creativecommons.org/licenses/by/4.0/deed.zh

## 相关仓库

- [cloudwubi-client](https://github.com/zsdili/cloudwubi-client) - 端侧内核
- [cloudwubi-gateway](https://github.com/zsdili/cloudwubi-gateway) - 云端网关
- [cloudwubi-ai](https://github.com/zsdili/cloudwubi-ai) - AI 引擎（规划中）

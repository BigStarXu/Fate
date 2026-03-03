# Fate（命运）

基于 [Rasa](https://rasa.com/) 的对话机器人项目。

---

## 环境要求

- **Python** 3.10
- 推荐使用 [Cursor](https://cursor.sh/) 编辑器进行开发

## 安装

### 1. 安装 Rasa

```bash
pip3 install rasa
```

若在国内网络环境下，建议使用清华镜像加速：

```bash
pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple rasa
```

### 2. 训练模型

在项目根目录下执行，基于当前 `data/` 中的 NLU、stories、rules 进行训练：

```bash
rasa train
```

训练完成后，模型会生成在 `models/` 目录下。

## 运行

启动服务后即可与机器人对话（具体命令可参考 [Rasa 文档](https://rasa.com/docs/)）：

```bash
rasa run
```

（另开终端）启动 action 服务：

```bash
rasa run actions
```

---

*Fate — 命运*
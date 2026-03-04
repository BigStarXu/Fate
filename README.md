# Fate（命运）

基于 [Rasa](https://rasa.com/) 的对话机器人项目，**使用中文**与用户对话。

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

### 2. 安装中文分词依赖（必装）

本项目为中文机器人，NLU 使用 `JiebaTokenizer` 分词，需要安装 jieba：

```bash
pip install jieba
```

若未安装，执行 `rasa train` 时会因默认 `WhitespaceTokenizer` 不支持 `language: zh` 而报错。

### 3. 训练模型

在项目根目录下执行，基于当前 `data/` 中的 NLU、stories、rules 进行训练：

```bash
rasa train
```

训练完成后，模型会生成在 `models/` 目录下。

## 中文配置说明

- **config.yml**：`language: zh`，且 pipeline 使用 `JiebaTokenizer`（中文不能用默认的 `WhitespaceTokenizer`）。
- **data/nlu.yml**：意图示例为中文（如「你好」「再见」「心情不好」等）。
- **domain.yml**：所有回复文案为中文。

修改上述文件后需重新执行 `rasa train`。

## 运行
直接对话
```bash
rasa shell
```

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
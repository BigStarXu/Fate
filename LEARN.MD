# 项目结构详解

```
FATE/
 ├── actions/
 │    └── actions.py
 ├── data/
 │    ├── nlu.yml
 │    ├── stories.yml
 │    ├── rules.yml
 ├── domain.yml
 ├── config.yml
 ├── endpoints.yml
```
---

# NLU（意图识别）

文件：`data/nlu.yml`

示例：

```yaml
version: "3.1"

nlu:
- intent: greet
  examples: |
    - hello
    - hi
    - hey

- intent: goodbye
  examples: |
    - bye
    - see you
```

👉 意图就是：用户想干嘛

---

# 对话流程（stories）

文件：`data/stories.yml`

```yaml
version: "3.1"

stories:
- story: happy path
  steps:
  - intent: greet
  - action: utter_greet
  - intent: goodbye
  - action: utter_goodbye
```

---

# domain.yml（机器人能力总表）

```yaml
version: "3.1"

intents:
  - greet
  - goodbye

responses:
  utter_greet:
  - text: "你好呀 👋"

  utter_goodbye:
  - text: "再见 👋"
```

👉 这里定义：

* 所有意图
* 所有回复
* 所有 actions
* 所有 slot

---

# 训练模型

```bash
rasa train
```

会生成：

```
models/
```

---

# 开始对话

```bash
rasa shell
```

调试模式：

```bash
rasa shell --debug
```

---

# 自定义业务逻辑（重点）

比如你要查数据库。

## 1️写 action

`actions/actions.py`

```python
from rasa_sdk import Action
from rasa_sdk.events import SlotSet

class ActionHello(Action):

    def name(self):
        return "action_hello"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(text="我是自定义逻辑")
        return []
```

---

## 注册到 domain.yml

```yaml
actions:
  - action_hello
```

---

## story 使用

```yaml
- story: test custom
  steps:
  - intent: greet
  - action: action_hello
```

---

## 4启动 action 服务

```bash
rasa run actions
```

---

## 再开一个终端

```bash
rasa shell
```

---

# 变成 API 服务

```bash
rasa run --enable-api --cors "*"
```

接口地址：

```
http://localhost:5005/webhooks/rest/webhook
```

---

# 进阶

你后期可能会用到：

* slot（对话记忆）
* form（收集参数）
* rule（规则对话）
* webhook 接入前端
* docker 部署
* 多语言模型
* LLM 集成

---

# 学习路径建议

### 第一步

理解：

* intent
* story
* domain

### 第二步

学会：

* slot
* form

### 第三步

学会：

* 自定义 action
* API 对接

---

# 🔥 常见坑

| 问题        | 原因                |
| --------- | ----------------- |
| 机器人不说话    | story 没写          |
| 意图识别不准    | 训练数据太少            |
| action 报错 | 没启动 action server |
| 走错流程      | story 冲突          |

---


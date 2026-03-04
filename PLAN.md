# Fate 项目计划 / 下一步做什么

## 当前进度

| 模块 | 状态 | 说明 |
|------|------|------|
| NLU 意图 | ✅ 已有 | greet, goodbye, affirm, deny, mood_great, mood_unhappy, bot_challenge |
| domain.yml | ✅ 已有 | 意图、回复、session 配置齐全 |
| stories | ✅ 已有 | happy path、sad path 1/2 |
| rules | ✅ 已有 | goodbye、bot_challenge 规则 |
| 自定义 Action | ❌ 未用 | `actions/actions.py` 里全是注释，没有实际业务逻辑 |
| slot / form | ❌ 未用 | 还没有“对话记忆”和“多轮表单” |
| API / 前端 | ❌ 未做 | 仅本地 `rasa shell` 对话 |

---

## 建议的下一步（按优先级）

### 1. 先跑通“自定义 Action”流程（推荐第一步）

**目标**：学会写一个 action、在 domain 里注册、在 story 里调用，并跑通 `rasa run actions` + `rasa shell`。

**可以做的事**：
- 在 `actions/actions.py` 里取消注释并改成一个简单 action（例如 `action_hello_world`），或新建一个 `action_hello` 返回一句自定义话。
- 在 `domain.yml` 的 `actions:` 里加上这个 action 名。
- 在 `data/stories.yml` 里加一条短 story，例如：`greet` → 你的自定义 action。
- 一个终端 `rasa run actions`，另一个终端 `rasa shell`，测试能否走到自定义 action 并收到回复。

**对应 LEARN.MD**：第三步里的“自定义 action”。

---

### 2. 加 slot + form（多轮、带记忆）

**目标**：用户说“我想订餐”，机器人连续问“时间？”“人数？”，并记住答案。

**可以做的事**：
- 在 `domain.yml` 里定义 slots（如 `time`、`people_count`）和 `restaurant_form`。
- 在 `data/stories.yml` 里写“填表”的 story，或配合 `data/rules.yml` 用 form 规则。
- 如需“查数据库/算价格”再在 `actions/actions.py` 里写 Form 对应的 action。

**对应 LEARN.MD**：第二步“slot、form”。

---

### 3. 把机器人当 API 用（给前端/其他系统）

**目标**：用 HTTP 调 Rasa，而不是只在命令行对话。

**可以做的事**：
- 运行：`rasa run --enable-api --cors "*"`。
- 用 Postman 或前端请求：`POST http://localhost:5005/webhooks/rest/webhook`，body 如 `{"message":"你好"}`。
- 若要同时用自定义逻辑，再开一个终端 `rasa run actions`。

**对应 LEARN.MD**：“变成 API 服务”。

---

### 4. 按业务定“真正要做的功能”

上面 1～3 是**能力建设**。真正计划可以按业务来拆，例如：

- **若做客服**：加“查订单”“退换货”等意图 + slot/form + action 查数据库。
- **若做订餐**：加“订餐/改单/取消”意图 + 时间/人数等 slot + form + action 落库。
- **若做 FAQ**：先加若干意图和回复，再考虑用 Rasa 的 FAQ 或 LLM 集成。

建议：先定一个**最小可用场景**（比如“就做查订单”），再按 1 → 2 → 3 把能力接上。

---

## 本周可执行的小目标（示例）

1. **今天**：在 `actions/actions.py` 里实现一个 `action_hello`，在 domain 和 story 里接上，跑通。
2. **明天**：在 domain 里加 1 个 slot、1 个 form，写一条“填表”的 story 或 rule，跑通。
3. **本周内**：用 `rasa run --enable-api` 跑起来，用 Postman 发一条消息并收到回复。

---

## 计划怎么用这个文件

- **PLAN.md**：只做“计划与下一步”，不写具体代码。
- 具体要做哪一步时，可以再说“帮我实现 action_hello”或“帮我加一个订餐 form”，再在代码里改。
- 每完成一步，可以回来在 PLAN.md 里把对应项改成 ✅，并写上“下一步：xxx”。

这样你就有一个清晰的“下一步要干啥”的清单，随时可以按顺序做。

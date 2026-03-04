# Slot + Form 为啥这么写

## 1. Rasa 的 Form 在干什么

Form = **多轮、带记忆**的对话：机器人按顺序问若干问题，把用户每次回答存进 **slot**，等必填 slot 都满了再往下走（例如执行 `action_submit_tarot`）。

- **Slot**：存在 tracker 里的“记忆”（如 `question`、`spread_type`），可跨轮保留。
- **Form**：一个“循环”——在「当前对话在填这张表」的状态下，每次用户说话都会先交给 form 处理（填 slot / 问下一个问题），直到必填 slot 都填满，form 才退出。

所以需要有一个**状态**表示“现在在填表”：这就是 **active_loop**。

---

## 2. active_loop 是什么

- **active_loop: tarot_form**  
  表示：当前处于「塔罗表单」这一轮循环里。  
  在这种状态下，Rasa 的默认行为是：**下一步先 `action_listen`（等用户输入）**，用户说完再跑 `tarot_form`，由 form 决定是继续问下一个问题还是结束。

- **active_loop: null**  
  表示：没有在跑任何 form，表单已结束。  
  在这种状态下，才可能去跑别的 action（比如 `action_submit_tarot`）。

也就是说：  
**有没有 active_loop、是哪个 form，决定了“下一步是继续等用户填表，还是去做别的事”。**

---

## 3. 为啥「激活表单」写在 rule 里

```yaml
# data/rules.yml
- rule: 用户想算塔罗时激活塔罗表单
  steps:
  - intent: ask_tarot
  - action: tarot_form
  - active_loop: tarot_form
```

- **Rule** = 只要条件对上就**一定**这么走，不学概率。  
- 我们想要：用户一说「想算塔罗」→ **必定**进入表单、开始多轮填表。  
- 所以用 rule：`ask_tarot` → 执行 `tarot_form` → 把 `active_loop` 设为 `tarot_form`。  
这样一旦识别到意图，就稳定进入 form，不会和别的 story 抢。

---

## 4. 为啥「填完后提交」写在 story 里，还要写 active_loop: null

```yaml
# data/stories.yml
- story: 塔罗占卜多轮填表（表单填完后提交）
  steps:
  - intent: ask_tarot
  - action: tarot_form
  - active_loop: tarot_form
  - action: tarot_form
  - active_loop: null
  - action: action_submit_tarot
```

- 表单**进行中**时，Rasa 内部有一条规则：**active_loop = tarot_form → 下一步是 action_listen**。  
  也就是说：只要还在填表，就优先“听用户说”，不会去跑 `action_submit_tarot`。

- 如果 story 里只写：  
  `tarot_form → tarot_form → action_submit_tarot`，  
  而不写 **active_loop: null**，Rasa 会认为「在 form 还在进行（active_loop 仍是 tarot_form）的状态下就要跑 action_submit_tarot」，和上面那条「form 进行中 → action_listen」**冲突**，训练会报错。

- 所以在 story 里**显式写一步 `active_loop: null`** 表示：  
  「这里表单已经跑完、循环结束，active_loop 被清空」。  
  这样「要执行 action_submit_tarot」的状态是「active_loop 已经是 null」，就不会和「form 进行中 → action_listen」冲突。

**总结**：  
- Rule 负责「什么时候进 form」（激活 + `active_loop: tarot_form`）。  
- Story 负责「form 跑完以后做什么」，并且**必须用 active_loop: null 标出“表单已结束”**，否则会和 Rasa 自带的 form 规则打架。

---

## 5. 实际对话对应到配置

| 用户 / 系统 | 对应配置 / 行为 |
|-------------|------------------|
| 用户：「我想算塔罗」 | 命中 rule：`ask_tarot` → `tarot_form`，`active_loop: tarot_form` |
| 系统问：「您想问哪方面的问题？」 | domain 里 `tarot_form` 的 required_slots 第一个是 `question`，自动用 `utter_ask_question` |
| 用户：「感情」 | `action_listen` 后用户输入；form 再跑，用 `from_text` 填满 `question`，接着问下一个 |
| 系统问：「想用哪种牌阵？」 | 同上，问 `spread_type`，用 `utter_ask_spread_type` |
| 用户：「三张」 | form 再跑，填满 `spread_type`，required_slots 都满了，form **自己**把 `active_loop` 设为 `null` |
| 系统跑 `action_submit_tarot` 并回复 | story 里「active_loop: null → action_submit_tarot」被命中，执行自定义 action，用 slot 记忆拼出回复 |

所以：**active_loop 在哪** = 在 **rules.yml（激活）** 和 **stories.yml（结束）** 里，用来标出「什么时候在填表、什么时候表填完了」。

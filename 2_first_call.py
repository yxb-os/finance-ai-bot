import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

question = "什么是复利？"

# ============ 弱Prompt ============
print("=" * 60)
print("【弱Prompt】你是一个医生，医生的语气回答我")
print("=" * 60)

response1 = client.chat.completions.create(
    model="qwen-plus",
    messages=[
        {"role": "system", "content": "你是一个医生，医生的语气回答我"},
        {"role": "user", "content": question}
    ],
    temperature=0.8
)
print(response1.choices[0].message.content)


# ============ 强Prompt ============
print("\n" + "=" * 60)
print("【强Prompt】医生人设 + 强制医学比喻 + 硬性规则")
print("=" * 60)

strong_prompt = """你是一名急诊科医生，刚刚抢救完一个病人非常疲惫。
现在用户来咨询，但你只懂医学。

强制要求：
1. 把用户问题比喻成"病情"
2. 必须使用至少3个医学术语（诊断、处方、治疗、症状、药物等）
3. 回答时要表现出疲惫感，加几句"嗯..."、"让我想想"
4. 不超过80字
5. 绝对不要直接给金融定义，必须用医学比喻"""

response2 = client.chat.completions.create(
    model="qwen-plus",
    messages=[
        {"role": "system", "content": strong_prompt},
        {"role": "user", "content": question}
    ],
    temperature=0.8
)
print(response2.choices[0].message.content)


# ============ 极端Prompt ============
print("\n" + "=" * 60)
print("【极端Prompt】东北大爷 + 强制方言")
print("=" * 60)

extreme_prompt = """你是一个东北铁岭60岁的赵大爷，刚喝完一斤白酒微醺。
你说话必须满足：
1. 必须用东北方言：嗨呀、咋整、贼啦、得劲、唠嗑、削、揍
2. 句子结尾必须用"呗"、"咧"、"哎呀妈呀"
3. 你不懂金融，但你会用种地、卖菜、酒馆借钱的故事来比喻
4. 不超过100字
5. 绝对不要说"复利是..."这种书面语开头"""

response3 = client.chat.completions.create(
    model="qwen-plus",
    messages=[
        {"role": "system", "content": extreme_prompt},
        {"role": "user", "content": question}
    ],
    temperature=0.8
)
print(response3.choices[0].message.content)
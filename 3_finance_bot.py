# ============================================
# Day 2 Hour 3: 金融客服AI机器人 🤖💰
# 整合：OOP + AI调用 + 多轮对话 + 文件存储
# ============================================

import os
import json
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI

# ---- 加载API Key ----
load_dotenv()
api_key = os.getenv("DASHSCOPE_API_KEY")


# ---- 客服机器人类 ----
class FinanceBot:
    """金融客服AI机器人 - 支持多轮对话"""
    # 初始化机器人
    def __init__(self, name="小金"):
        self.name = name
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
        )
        self.history = []  # 对话历史（核心！）
        # 通过字符串先定义Ai的属相
        # 系统提示词：定义AI的"人格"
        self.system_prompt = f"""你叫{name}，是一位专业、友好的金融客服。

你的职责：
1. 解答用户的金融问题（理财、贷款、信用卡、保险等）
2. 用通俗易懂的语言，避免过度专业术语
3. 涉及具体投资建议时，必须提醒用户咨询专业人士
4. 回答简洁，一般不超过150字
5. 保持友好、耐心的语气，可以用 emoji 增加亲和力

特别要求：
- 必须记住用户之前提到的信息（姓名、需求、关注点）
- 在合适时机引用之前对话的内容，体现关怀"""
    # 用户每次输入后调用机器人方法，先记录历史记录
    def chat(self, user_message):
        """单次对话（自动维护历史）"""
        # 1. 把用户消息加入历史
        self.history.append({"role": "user", "content": user_message})
        # 先把用户的回答入属性
        # 2. 构造完整 messages（system + 全部历史）
        messages = [{"role": "system", "content": self.system_prompt}]
        messages.extend(self.history)
        # 然后再给AI，并调用
        # 3. 调用AI
        try:
            response = self.client.chat.completions.create(
                model="qwen-plus",
                messages=messages,
                temperature=0.7,
            )
            ai_reply = response.choices[0].message.content
            
            # 4. AI的回答也加入历史（重要！下一轮要用）
            self.history.append({"role": "assistant", "content": ai_reply})
            # 先保存ai回答，后返回回答和所用token
            return ai_reply, response.usage.total_tokens
        
        except Exception as e:
            return f"❌ 出错了：{e}", 0
    # 创建json来保存对话
    def save_history(self):
        """保存对话历史到本地文件"""
        if not self.history:
            print("⚠️  没有对话历史可保存")
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"chat_history_{timestamp}.json"
        
        with open(filename, "w", encoding="utf-8") as f:
            json.dump({
                "bot_name": self.name,
                "system_prompt": self.system_prompt,
                "history": self.history,
                "saved_at": timestamp
            }, f, ensure_ascii=False, indent=2)
        
        print(f"💾 对话已保存：{filename}")
    
    def clear_history(self):
        """清空对话历史"""
        self.history = []
        print("🧹 历史已清空，重新开始对话")
        
    def show_history_count(self):
        """显示历史轮次"""
        rounds = len(self.history) // 2
        print(f"📊 当前对话轮次：{rounds} 轮（共 {len(self.history)} 条消息）")


# ---- 主程序：命令行交互 ----
def main():
    print("=" * 60)
    print("🤖 金融客服AI机器人「小金」上线！")
    print("=" * 60)
    print("💡 使用提示：")
    print("   - 直接输入问题开始对话")
    print("   - 输入 'exit' 退出并保存")
    print("   - 输入 'clear' 清空历史重新开始")
    print("   - 输入 'save' 中途保存对话")
    print("   - 输入 'count' 查看当前轮次")
    print("=" * 60)
    
    bot = FinanceBot("小金")
    total_tokens = 0
    
    while True:
        # 等待用户输入
        try:
            user_input = input("\n👤 你：").strip()
        except KeyboardInterrupt:
            print("\n\n👋 检测到Ctrl+C，正在保存对话...")
            bot.save_history()
            break
        
        # 特殊命令
        if user_input.lower() == "exit":
            print("\n👋 再见！正在保存对话...")
            bot.save_history()
            print(f"📊 本次对话总消耗：{total_tokens} tokens")
            print(f"   约花费：{total_tokens * 0.0014 / 1000:.6f} 元")
            break
        
        if user_input.lower() == "clear":
            bot.clear_history()
            continue
        
        if user_input.lower() == "save":
            bot.save_history()
            continue
        
        if user_input.lower() == "count":
            bot.show_history_count()
            continue
        
        if not user_input:
            continue
        
        # 调用AI回答
        print("\n🤖 小金正在思考...", end="", flush=True)
        reply, tokens = bot.chat(user_input)
        total_tokens += tokens
        
        # 清除"思考中"提示
        print("\r" + " " * 30 + "\r", end="")
        
        print(f"🤖 小金：{reply}")
        print(f"   [消耗 {tokens} tokens / 累计 {total_tokens} tokens]")


if __name__ == "__main__":
    main()
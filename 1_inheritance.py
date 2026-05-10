# ---- 父类：账户基类 ----
class BankAccount:
    """所有账户的父类"""
    # 初始化将用户姓名和balan传进来
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance
        self.account_type = "普通账户"
    # 调用方法，传入存款金额加入我们的账户
    def deposit(self, amount):
        self.balance += amount
        print(f"✅ {self.owner} 存入 {amount}元，余额：{self.balance}元")
    # 取出金额,传入需要取出的金额,金额不足则返回false
    def withdraw(self, amount):
        if amount > self.balance:
            print(f"❌ {self.owner} 余额不足")
            return False
        self.balance -= amount
        print(f"💰 {self.owner} 取出 {amount}元，余额：{self.balance}元")
        return True
    #  查询我们当前账户余额
    def show(self):
        print(f"[{self.account_type}] {self.owner}：{self.balance}元")


# ---- 子类1：VIP账户 ----
# Java: class VIPAccount extends BankAccount
# Python: class VIPAccount(BankAccount):
class VIPAccount(BankAccount):
    """VIP账户：透支额度+优先服务"""
    # 根据传入的姓名和钱包余额调用父类的初始化方法,并覆盖新增属性和覆盖属性
    def __init__(self, owner, balance=0, credit_limit=10000):
        # super() 调用父类构造，相当于Java的 super(owner, balance)
        super().__init__(owner, balance)
        self.credit_limit = credit_limit
        self.account_type = "VIP账户"  # 覆盖父类属性
    
    # 重写父类方法（Java: @Override）
    def withdraw(self, amount):
        # 重写父类方法，并允许客户超额提出账户的钱10000，如果客户提取的超额1w以上返回false，并修改账户余额，同时根据余额是否大于0返回不同的消息
        available = self.balance + self.credit_limit
        if amount > available:
            print(f"❌ {self.owner} 超出透支额度")
            return False
        self.balance -= amount
        if self.balance < 0:
            print(f"💎 VIP {self.owner} 透支 {abs(self.balance)}元（享受透支特权）")
        else:
            print(f"💰 VIP {self.owner} 取出 {amount}元，余额：{self.balance}元")
        return True


# ---- 子类2：储蓄账户 ----
class SavingsAccount(BankAccount):
    """储蓄账户：有利息"""
    # 同样是首先初始化调用父类的方法，并添加属性和覆盖属性
    def __init__(self, owner, balance=0, rate=0.03):
        super().__init__(owner, balance)
        self.rate = rate
        self.account_type = "储蓄账户"
        # 新定义方法,计算用户的年利息,并拼接字符串返回
    # 子类独有方法（父类没有的）
    def calculate_interest(self):
        interest = self.balance * self.rate
        print(f"📈 {self.owner} 年利息：{interest:.2f}元")
        return interest


# ---- 子类3：信用账户 ----
class CreditAccount(BankAccount):
    """信用账户：纯透支，没有真实余额"""
    
    def __init__(self, owner, credit_limit=20000):
        super().__init__(owner, balance=0)
        self.credit_limit = credit_limit
        self.account_type = "信用账户"
        self.debt = 0  # 欠款
    
    def withdraw(self, amount):
        if self.debt + amount > self.credit_limit:
            print(f"❌ {self.owner} 超出信用额度")
            return False
        self.debt += amount
        print(f"💳 {self.owner} 信用消费 {amount}元，欠款：{self.debt}元")
        return True
    
    def repay(self, amount):
        self.debt -= amount
        if self.debt < 0:
            self.balance = -self.debt  # 多还的变余额
            self.debt = 0
        print(f"✅ {self.owner} 还款 {amount}元，欠款：{self.debt}元")


# ---- 主程序：多态测试 ----
if __name__ == "__main__":
    print("=" * 50)
    print("🏦 银行账户系统 v2.0（继承+多态）")
    print("=" * 50)
    
    # 创建4种账户
    accounts = [
        BankAccount("张三", 1000),
        VIPAccount("李四", 500, credit_limit=5000),
        SavingsAccount("王五", 10000, rate=0.05),
        CreditAccount("赵六", credit_limit=15000),
    ]
    
    print("\n📍 测试1：所有账户显示信息（多态）")
    print("-" * 50)
    for acc in accounts:
        acc.show()  # 同一个方法，不同账户表现不同
    # 循环遍历查询账户余额,根据入参的不同,1进主流程,2进VIP流程,3进储蓄账户流程,4进信用卡账户流程
    print("\n📍 测试2：所有账户取款2000元（多态）")
    print("-" * 50)
    for acc in accounts:
        acc.withdraw(2000)
    # 每个账户根据类型不同去调用对应方法,张三余额不足,李四,取500,并用了vip额度1500,;王五因为本身没有这个方法复用父类的也是取了2000,赵六使用信用卡2000余额
    print("\n📍 测试3：储蓄账户独有方法")
    print("-" * 50)
    saving = accounts[2]  # SavingsAccount
    saving.calculate_interest()
    # 王五年利息400
    print("\n📍 测试4：信用账户还款")
    print("-" * 50)
    credit = accounts[3]  # CreditAccount
    credit.repay(500)
    credit.repay(2000)  # 多还款，转成余额
    # 赵六先还2000还掉借的,然后多换500变成余额了
    credit.show()
    # 最后,张三余额1000,李四VIP账户余额-1500,王五账户余额8000,赵六账户余额500
    print("\n🎉 OOP继承 + 多态测试完成！")
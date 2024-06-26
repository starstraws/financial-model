import numpy as np
from price import risk_free_rate, volatility, maturity, trading_days, knock_out, knock_in
from delta import delta_greek
from tqdm import tqdm


def delta_hedge_simulation(S, delta_hedge, T_len):
    stock_expense = []
    accum_cash = []
    Interest = []
    stock_units = []
    cost = 0
    prev_delta = 0

    # 截断 S 和 delta_hedge 为相同长度
    min_len = min(len(S), len(delta_hedge))
    S = S[:min_len]
    delta_hedge = delta_hedge[:min_len]

    for i, (price, delta) in enumerate(zip(S, delta_hedge)):
        delta_change = delta - prev_delta  # 计算delta差
        stock_units_change = delta_change  # 计算需要交易的现货份数(卖出为负值)

        cost += stock_units_change * price  # 交易现货增加的成本(卖出为负值)
        interest = cost * risk_free_rate / trading_days * T_len  # 计算本期利息费用
        cost += interest  # 累计成本

        prev_delta = delta  # 更新delta

        # 存入数据，最后返回
        stock_units.append(stock_units_change)
        stock_expense.append(price * stock_units_change)
        accum_cash.append(cost)
        Interest.append(interest)

        # 检查敲出条件
        if delta == 0:
            break

    return stock_units, stock_expense, accum_cash, Interest


if __name__ == "__main__":
    T_len = 1
    T = np.arange(maturity, 0, -T_len / trading_days)

    S = 10 * np.array([
        7.35000, 7.39000, 7.40000, 7.53000, 7.70000, 8.14000, 8.14000, 7.73000, 7.91000, 7.88000,
        8.67000, 9.54000, 8.66000, 8.22000, 8.26000, 8.08000, 7.75000, 7.40000, 7.43000, 6.88000,
        6.73000, 6.84000, 6.66000, 6.86000, 6.94000, 6.76000, 6.93000, 7.05000, 7.05000, 7.30000,
        7.48000, 7.66000, 7.55000, 7.60000, 7.89000, 7.78000, 7.84000, 7.55000, 8.07000, 8.52000,
        8.40000, 8.27000, 8.41000, 9.25000, 8.72000, 8.31000, 8.40000, 8.22000, 7.93000, 8.13000,
        7.98000, 7.96000, 7.87000, 7.82000, 7.77000, 7.89000, 7.94000, 7.78000, 7.88000, 7.88000,
        7.93000, 8.01000, 7.95000, 7.90000, 7.83000, 7.80000, 7.82000, 7.52000, 7.62000, 7.71000,
        7.81000, 7.76000, 8.05000, 7.93000, 7.89000, 8.12000, 8.16000, 8.16000, 8.07000, 8.08000,
        8.09000, 8.22000, 8.14000, 8.14000, 8.00000, 8.01000, 7.79000, 8.03000, 7.70000, 7.76000,
        8.27000, 8.27000, 8.33000, 8.39000, 8.31000, 8.27000, 8.46000, 8.37000, 8.48000, 8.59000,
        8.58000, 8.57000, 8.43000, 8.68000, 8.42000, 8.34000, 8.38000, 8.06000, 8.14000, 8.15000,
        8.39000, 8.40000, 8.22000, 8.13000, 8.08000, 8.00000, 7.93000, 7.73000, 7.47000, 7.42000,
        7.46000, 7.63000, 7.65000, 7.54000, 7.26000, 7.42000, 7.21000, 7.12000, 7.08000, 7.08000,
        7.18000, 7.31000, 7.32000, 7.41000, 7.49000, 7.49000, 7.60000, 7.49000, 7.61000, 7.41000,
        7.38000, 7.47000, 7.58000, 7.35000, 7.25000, 7.37000, 7.46000, 7.40000, 7.49000, 7.52000,
        7.50000, 7.39000, 7.38000, 7.53000, 7.51000, 7.58000, 7.59000, 7.65000, 7.49000, 7.36000,
        7.37000, 7.39000, 7.31000, 7.38000, 7.63000, 7.60000, 7.63000, 7.61000, 7.58000, 7.84000,
        7.82000, 7.78000, 7.94000, 7.84000, 7.68000, 7.82000, 7.77000, 7.66000, 7.64000, 7.40000,
        7.35000, 7.40000, 7.24000, 7.29000, 7.29000, 7.40000, 7.27000, 7.12000, 7.22000, 7.29000,
        7.30000, 7.32000, 7.26000, 7.25000, 7.20000, 7.17000, 7.12000, 7.26000, 7.34000, 7.29000,
        7.27000, 7.32000, 7.66000, 7.62000, 7.70000, 7.73000, 7.73000, 7.66000, 7.75000, 8.13000,
        7.80000, 7.86000, 7.85000, 7.83000, 7.75000, 7.69000, 7.35000, 7.32000, 7.40000, 7.43000,
        7.43000, 7.42000, 7.38000, 7.40000, 7.44000, 7.49000, 7.57000, 7.64000, 7.63000, 7.60000,
        7.65000, 7.61000, 7.48000, 7.58000, 7.51000, 7.69000, 7.60000, 7.69000, 7.59000, 7.65000,
        7.65000, 7.56000, 7.45000, 7.39000, 7.31000, 7.22000, 7.17000, 7.21000, 7.28000, 7.29000,
        7.18000, 7.22000, 7.04000, 7.05000, 7.10000, 7.09000, 7.14000, 7.85000, 7.75000, 8.06000,
        7.98000, 7.59000, 7.34000, 7.39000, 7.27000, 7.29000, 7.54000, 7.74000, 7.74000, 7.88000,
        7.89000, 7.85000, 7.80000, 7.74000, 7.82000, 7.66000, 7.73000, 7.66000, 7.56000, 7.47000,
        7.42000, 7.30000, 7.32000, 7.34000, 7.35000, 7.33000, 7.53000, 7.68000, 7.62000, 7.65000,
        7.51000, 7.77000, 7.75000, 7.68000, 7.71000, 7.71000, 7.69000, 7.64000, 7.80000, 7.60000,
        7.43000, 7.35000, 7.26000, 7.68000, 7.94000, 7.81000, 7.78000, 7.77000, 7.82000, 7.83000,
        7.84000, 7.84000, 7.91000, 7.83000, 7.68000, 7.78000, 7.84000, 7.74000, 7.92000, 7.98000,
        7.87000, 7.87000, 8.09000, 8.14000, 8.02000, 7.99000, 8.11000, 8.12000, 8.04000, 8.08000,
        7.95000, 7.89000, 7.78000, 7.84000, 7.88000, 7.93000, 7.64000, 7.71000, 7.71000, 7.71000,
        7.87000, 7.83000, 7.63000, 7.63000, 7.44000, 7.39000, 7.39000, 7.39000, 7.49000, 7.35000,
        7.29000, 7.43000, 7.60000, 7.62000, 7.60000, 7.54000, 7.71000, 7.79000, 7.66000, 7.91000,
        7.47000, 7.46000, 7.48000, 7.47000, 7.35000, 7.36000, 7.46000, 7.39000, 7.36000, 7.37000,
        7.38000, 7.34000, 7.28000, 7.30000, 7.35000, 7.24000, 7.31000, 7.29000, 7.01000, 6.94000,
        6.93000, 6.71000, 6.81000, 6.86000, 6.90000, 6.96000, 6.97000, 7.02000, 7.01000, 6.99000,
        7.06000, 7.14000, 7.13000, 7.10000, 7.12000, 7.13000, 7.19000, 7.20000, 7.26000, 7.22000,
        7.29000, 7.27000, 7.22000, 7.19000, 7.27000, 7.23000, 7.23000, 7.26000, 7.22000, 7.25000,
        7.27000, 7.34000, 7.23000, 7.25000, 7.25000, 7.05000, 7.15000, 7.29000, 7.27000, 7.34000,
        7.30000, 7.32000, 7.21000, 7.15000, 7.29000, 7.30000, 7.17000, 7.12000, 7.12000, 7.17000,
        7.17000, 7.25000, 7.28000, 7.30000, 7.27000, 7.08000, 7.18000, 7.16000, 7.25000, 7.27000,
        7.08000, 6.95000, 6.94000, 6.77000, 6.67000, 6.27000, 6.26000, 6.52000, 6.74000, 6.92000,
        6.72000, 6.57000, 6.32000, 6.22000, 6.10000, 5.65000, 5.89000, 5.91000, 6.18000, 6.26000,
        6.27000, 6.29000, 6.32000, 6.36000, 6.35000, 6.47000, 6.30000, 6.39000, 6.37000, 6.31000,
        6.23000, 6.30000, 6.30000, 6.31000, 6.35000, 6.39000, 6.38000, 6.41000, 6.46000, 6.50000,
        6.48000, 6.51000, 6.54000, 6.45000
    ])
    delta_hedge = []

    # 修改循环部分，使用 tqdm 遍历 T
    for i, t in enumerate(tqdm(T, desc="Calculating delta hedge")):
        if S[i] > S[0]* knock_out:
            break
        else:
            delta = delta_greek(S[i], t)
            print(delta)
            delta_hedge.append(delta)

    stock_units, stock_expense, accum_cash, Interest = delta_hedge_simulation(S, delta_hedge, T_len)
    print("股票价格:", S)
    print("delta:", delta_hedge)
    print("购买股票数量:", stock_units)
    print("股票费用:", stock_expense)
    print("累计现金流:", accum_cash)
    print("利息费用:", Interest)
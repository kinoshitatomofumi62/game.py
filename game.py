import streamlit as st
import sympy as sp
import random

st.set_page_config(page_title="極限突破！リミットバトル Ver.10", page_icon="♾️", layout="wide")

def generate_problem(stage):
    x = sp.Symbol('x', real=True) # 実数として定義
    
    patterns = ["polynomial", "trig_basic"]
    if stage >= 3: patterns.append("rationalize")
    if stage >= 5: patterns.append("trig_advanced_cos")
    if stage >= 7: patterns.append("inf_limit")
    if stage >= 9: patterns.append("squeeze")      
    if stage >= 10: patterns.append("minus_inf") # マイナス無限大(NEW!)
    
    pattern = random.choice(patterns) if stage >= 10 else patterns[min(stage-1, len(patterns)-1)]

    # --- マイナス無限大パターンのロジック ---
    if pattern == "minus_inf":
        a = random.randint(2, 5)
        # sqrt(x^2 + ax) / x  (x -> -oo) 型
        # x < 0 のとき x = -sqrt(x^2) なので、答えは -1 になる
        num = sp.sqrt(x**2 + a*x)
        den = x
        limit_val = -sp.oo
        ans = -1
        dummies = {1, 0, a, -a, sp.oo}
        p_type = "minus_inf"

    # --- 既存のパターン (整理) ---
    elif pattern == "polynomial":
        a, k = random.randint(2, 6) * random.choice([-1, 1]), random.randint(1, 5)
        num, den, limit_val, ans = sp.expand((x-a)*(x+k)), x-a, a, a+k
        dummies = {a-k, -(a+k), 0, 1}
        p_type = "poly"
        
    elif pattern == "trig_basic":
        a, b = random.randint(2, 9), random.randint(2, 9)
        num, den, limit_val, ans = sp.sin(a*x), b*x, 0, sp.Rational(a, b)
        dummies = {sp.Rational(b, a), 1, 0, a}
        p_type = "trig"

    elif pattern == "rationalize":
        a = random.randint(1, 5)
        num, den, limit_val, ans = sp.sqrt(x + a**2) - a, x, 0, sp.Rational(1, 2*a)
        dummies = {2*a, sp.Rational(1, a), 0, sp.Rational(1, 2)}
        p_type = "rat"

    elif pattern == "inf_limit":
        a, b = random.randint(2, 8), random.randint(2, 8)
        num, den, limit_val, ans = a*x**2 + random.randint(1,9)*x, b*x**2 + 1, sp.oo, sp.Rational(a, b)
        dummies = {0, sp.oo, sp.Rational(b, a), 1}
        p_type = "inf"

    elif pattern == "trig_advanced_cos":
        a = random.randint(2, 5)
        num, den, limit_val, ans = 1 - sp.cos(a*x), x**2, 0, sp.Rational(a**2, 2)
        dummies = {a**2, sp.Rational(a, 2), sp.Rational(1, 2)}
        p_type = "cos"

    elif pattern == "squeeze":
        a = random.randint(2, 5)
        if random.random() > 0.5:
            num, den, limit_val, ans = sp.sin(a*x), x, sp.oo, 0
            dummies = {1, a, sp.oo}
        else:
            num, den, limit_val, ans = sp.sin(a*x), x, 0, a
            dummies = {1, 0, a**2}
        p_type = "sq"
    
    else: # inf_minus_inf
        a = random.randint(2, 8)
        num, den, limit_val, ans = sp.sqrt(x**2 + a*x) - x, 1, sp.oo, sp.Rational(a, 2)
        dummies = {a, 0, sp.oo}
        p_type = "imi"

    # --- 共通処理 ---
    def format_opt(val):
        if val == sp.oo: return "∞"
        if val == -sp.oo: return "-∞"
        return str(sp.simplify(val))

    correct_ans_str = format_opt(ans)
    final_dummies = {format_opt(

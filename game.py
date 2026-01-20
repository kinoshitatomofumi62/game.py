import streamlit as st
import sympy as sp
import random

# レイアウトを広く使う設定
st.set_page_config(page_title="極限突破！リミットバトル", page_icon="♾️", layout="wide")

# --- 問題生成ロジック（エラー対策済み） ---
def generate_problem(stage):
    x = sp.Symbol('x')
    
    # ステージによる難易度分け
    if stage == 1:
        pattern = "polynomial"
    elif stage == 2:
        pattern = "trig_basic"
    else:
        pattern = random.choice(["polynomial", "trig_basic", "trig_advanced"])
    
    if pattern == "polynomial":
        a = random.randint(-3, 5)
        k = random.randint(-3, 5)
        num = sp.expand((x - a) * (x + k))
        den = sp.expand(x - a)
        limit_val = a
        p_type = "因数分解による不定形の解消"
        ans = a + k
        # 多めにダミーを用意してエラーを防ぐ
        dummies = {str(0), str(-(a + k)), str(a - k), str(a + k + 1), str(a + 2), str(k)}
        
    elif pattern == "trig_basic":
        a = random.randint(1, 6)
        b = random.randint(1, 6)
        num = sp.sin(a * x)
        den = b * x
        limit_val = 0
        p_type = "三角関数の基本公式"
        ans = sp.Rational(a, b)
        dummies = {f"{b}/{a}", str(a), str(b), "1", "0", "1/2", f"{a+1}/{b}"}
        
    else: # Stage 3以降の難問
        choice = random.choice(["cos", "tan"])
        limit_val = 0
        if choice == "cos":
            a = random.randint(1, 4)
            num = 1 - sp.cos(a * x)
            den = x**2
            ans = sp.Rational(a**2, 2)
            p_type = "1-cosの極限（難問）"
            dummies = {str(a**2), str(a), f"{a}/2", "0", "1", f"{a**2}/4", "1/2"}
        else:
            a = random.randint(2, 5)
            num = sp.tan(a * x)
            den = sp.sin(random.randint(1, 3) * x)
            ans = sp.limit(num/den, x, 0)
            p_type = "tanとsinの混合（難問）"
            dummies = {"1", str(a), "0", "1/2", str(a*2), "3", "2/3"}

    correct_ans = str(ans)
    dummies.discard(correct_ans) # 正解と被ったら消

import streamlit as st
import sympy as sp
import random

# ページの設定
st.set_page_config(page_title="極限突破！リミットバトル", page_icon="♾️")

def generate_problem():
    x = sp.Symbol('x')
    pattern = random.choice(["polynomial", "trig", "exp"])
    
    if pattern == "polynomial":
        a = random.randint(-3, 5)
        k = random.randint(-3, 5)
        num = sp.expand((x - a) * (x + k))
        den = sp.expand(x - a)
        limit_val = a
        p_type = "因数分解"
    elif pattern == "trig":
        a = random.randint(2, 5)
        b = random.randint(2, 5)
        num = sp.sin(a * x)
        den = b * x
        limit_val = 0
        p_type = "三角関数"
    else:
        a = random.randint(2, 4)
        num = (1 + 1/x)**(a*x)
        den = 1
        limit_val = sp.oo
        p_type = "自然対数の底 e"

    expr = num / den
    ans = sp.limit(expr, x, limit_val)
    
    # LaTeX表示用の文字列作成
    lim_sym = r"\infty" if limit_val == sp.oo else str(limit_val)
    if den == 1:
        latex_str = rf"\lim_{{x \to {lim_sym}}} {sp.latex(num)}"
    else:
        latex_str = rf"\lim_{{x \to {lim_sym}}} \frac{{{sp.latex(num)}}}{{{sp.latex(den)}}}"
        
    return latex_str, str(ans), p_type

# --- メイン画面 ---
st.title("♾️ 極限突破！リミットバトル")
st.write("数学Ⅲの極限値を求めてモンスターを倒せ！")

if 'problem' not in st.session_state:
    st.session_state.problem = generate_problem()
    st.session_state.score = 0

latex_q, correct_ans, p_type = st.session_state.problem

st.info(f"現在のステージ: {p_type}")
st.latex(latex_q)

user_input = st.text_input("答えを入力してください (例: 2, 1/2, e**2, oo)", key="input")

if st.button("回答する"):
    if user_input.replace(" ", "") == correct_ans.replace(" ", ""):
        st.success("✨ 正解！ ✨")
        st.session_state.score += 1
        if st.button("次の問題へ"):
            st.session_state.problem = generate_problem()
            st.rerun()
    else:
        st.error(f"残念！ 正解は {correct_ans} でした。")
        if st.button("もう一度挑戦"):
            st.session_state.problem = generate_problem()
            st.rerun()

st.sidebar.write(f"現在のスコア: {st.session_state.score}")

import streamlit as st
import sympy as sp
import random

# ページの設定
st.set_page_config(page_title="極限突破！リミットバトル", page_icon="♾️")

def generate_problem():
    x = sp.Symbol('x')
    # パターンを「因数分解」と「三角関数」の2つに限定
    pattern = random.choice(["polynomial", "trig"])
    
    if pattern == "polynomial":
        # 因数分解型: (x-a)(x+k) / (x-a)
        a = random.randint(-3, 5)
        k = random.randint(-3, 5)
        num = sp.expand((x - a) * (x + k))
        den = sp.expand(x - a)
        limit_val = a
        p_type = "因数分解による不定形の解消"
    else:
        # 三角関数型: sin(ax) / bx
        a = random.randint(2, 5)
        b = random.randint(2, 5)
        num = sp.sin(a * x)
        den = b * x
        limit_val = 0
        p_type = "三角関数の極限公式"

    expr = num / den
    ans = sp.limit(expr, x, limit_val)
    
    # LaTeX表示用の文字列作成
    lim_sym = str(limit_val)
    latex_str = rf"\lim_{{x \to {lim_sym}}} \frac{{{sp.latex(num)}}}{{{sp.latex(den)}}}"
        
    return latex_str, str(ans), p_type

# --- メイン画面 ---
st.title("♾️ 極限突破！リミットバトル")
st.write("数学Ⅲの極限値を求めてモンスターを倒せ！")

# セッション状態の初期化
if 'problem' not in st.session_state:
    st.session_state.problem = generate_problem()
    st.session_state.score = 0

latex_q, correct_ans, p_type = st.session_state.problem

st.info(f"現在のステージ: {p_type}")
st.latex(latex_q)

user_input = st.text_input("答えを入力してください (例: 2, 1/2, 0, -5)", key="input")

col1, col2 = st.columns(2)

with col1:
    if st.button("回答する"):
        # 空欄チェック
        if user_input == "":
            st.warning("答えを入力してください。")
        else:
            # スペースを消して比較
            if user_input.replace(" ", "") == correct_ans.replace(" ", ""):
                st.success("✨ 正解！ ✨")
                st.session_state.score += 1
                st.balloons() # お祝いのエフェクト
            else:
                st.error(f"残念！ 正解は {correct_ans} でした。")

with col2:
    if st.button("次の問題へ"):
        st.session_state.problem = generate_problem()
        st.rerun()

st.sidebar.markdown(f"### 🏆 現在のスコア: {st.session_state.score}")
if st.sidebar.button("スコアをリセット"):
    st.session_state.score = 0
    st.rerun()

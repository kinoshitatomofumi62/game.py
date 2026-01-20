import streamlit as st
import sympy as sp
import random

st.set_page_config(page_title="極限突破！リミットバトル", page_icon="♾️")

def generate_problem():
    x = sp.Symbol('x')
    pattern = random.choice(["polynomial", "trig"])
    
    if pattern == "polynomial":
        a = random.randint(-3, 5)
        k = random.randint(-3, 5)
        num = sp.expand((x - a) * (x + k))
        den = sp.expand(x - a)
        limit_val = a
        p_type = "因数分解による不定形の解消"
    else:
        a = random.randint(1, 5)
        b = random.randint(1, 5)
        num = sp.sin(a * x)
        den = b * x
        limit_val = 0
        p_type = "三角関数の極限公式"

    expr = num / den
    ans = sp.limit(expr, x, limit_val)
    
    # LaTeX表示用
    lim_sym = str(limit_val)
    latex_str = rf"\lim_{{x \to {lim_sym}}} \frac{{{sp.latex(num)}}}{{{sp.latex(den)}}}"
    
    # --- 選択肢の生成 ---
    correct_ans = str(ans)
    options = [correct_ans]
    
    # 誤答（ダミー）を3つ作る
    while len(options) < 4:
        if pattern == "polynomial":
            dummy = str(random.randint(-10, 10))
        else:
            dummy = f"{random.randint(1, 9)}/{random.randint(2, 9)}"
            
        if dummy not in options:
            options.append(dummy)
    
    random.shuffle(options) # 順番をシャッフル
    return latex_str, correct_ans, p_type, options

# --- メイン画面 ---
st.title("♾️ 極限突破！リミットバトル")

if 'problem_data' not in st.session_state:
    st.session_state.problem_data = generate_problem()
    st.session_state.score = 0
    st.session_state.answered = False

latex_q, correct_ans, p_type, options = st.session_state.problem_data

st.info(f"現在のステージ: {p_type}")
st.latex(latex_q)

# 選択肢ボタンの作成
st.write("正しい極限値を選べ！")
cols = st.columns(2)

for i, opt in enumerate(options):
    with cols[i % 2]:
        if st.button(opt, key=f"btn_{opt}", use_container_width=True):
            if not st.session_state.answered:
                if opt == correct_ans:
                    st.balloons()
                    st.success("正解！")
                    st.session_state.score += 1
                else:
                    st.error(f"不正解！ 正解は {correct_ans} でした。")
                st.session_state.answered = True

# 次へ進むボタン
if st.session_state.answered:
    if st.button("次の問題へ ➡️", type="primary"):
        st.session_state.problem_data = generate_problem()
        st.session_state.answered = False
        st.rerun()

st.sidebar.markdown(f"### 🏆 スコア: {st.session_state.score}")

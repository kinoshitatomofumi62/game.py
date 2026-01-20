import streamlit as st
import sympy as sp
import random

st.set_page_config(page_title="極限突破！リミットバトル Ver.6", page_icon="♾️", layout="wide")

def generate_problem(stage):
    x = sp.Symbol('x')
    
    # パターン選択の拡張
    patterns = ["polynomial", "trig_basic"]
    if stage >= 3: patterns.append("rationalize")
    if stage >= 4: patterns.append("trig_advanced_cos")
    if stage >= 5: patterns.append("trig_complex")
    if stage >= 6: patterns.append("inf_limit") # 無限大(NEW!)
    
    pattern = random.choice(patterns) if stage >= 6 else patterns[min(stage-1, len(patterns)-1)]

    if pattern == "polynomial":
        a = random.randint(2, 6) * random.choice([-1, 1])
        k = random.randint(1, 5)
        num = sp.expand((x - a) * (x + k))
        den = sp.expand(x - a)
        limit_val, p_type, ans = a, "不定形の解消（因数分解）", a + k
        dummies = {str(a-k), str(-(a+k)), "0", str(a), str(k)}
        
    elif pattern == "trig_basic":
        a, b = random.randint(2, 9), random.randint(2, 9)
        num, den = sp.sin(a * x), b * x
        limit_val, p_type, ans = 0, "三角関数の基本公式", sp.Rational(a, b)
        dummies = {f"{b}/{a}", "1", str(a), str(b), "0"}

    elif pattern == "rationalize":
        a = random.randint(1, 5)
        num = sp.sqrt(x + a**2) - a
        den = x
        limit_val, p_type, ans = 0, "不定形の解消（有理化）", sp.Rational(1, 2 * a)
        dummies = {str(a), str(2*a), f"1/{a}", "0", "1/2"}

    elif pattern == "inf_limit":
        # 無限大への極限 (3x^2 / 2x^2 型)
        a, b = random.randint(2, 7), random.randint(2, 7)
        num = a * x**2 + random.randint(1, 9) * x
        den = b * x**2 + random.randint(1, 9)
        limit_val, p_type, ans = sp.oo, "無限大の極限（最高次数の比較）", sp.Rational(a, b)
        dummies = {"0", "oo", f"{b}/{a}", str(a), "1"}

    elif pattern == "trig_advanced_cos":
        a = random.randint(2, 5)
        num, den = 1 - sp.cos(a * x), x**2
        limit_val, p_type, ans = 0, "1-cosの応用（2乗に注意）", sp.Rational(a**2, 2)
        dummies = {str(a**2), f"{a}/2", f"{a**2}/4", "1/2"}

    elif pattern == "trig_complex":
        a, b = random.randint(2, 8), random.randint(2, 8)
        num, den = sp.sin(a * x), sp.tan(b * x)
        limit_val, p_type, ans = 0, "三角関数の複合（sin/tan）", sp.Rational(a, b)
        dummies = {f"{b}/{a}", "1", "0", f"{a}/{a+b}"}

    correct_ans = str(ans)
    if correct_ans in dummies: dummies.remove(correct_ans)
    options = random.sample(list(dummies), 3) + [correct_ans]
    random.shuffle(options)
    
    latex_str = rf"\lim_{{x \to {sp.latex(limit_val)}}} \frac{{{sp.latex(num)}}}{{{sp.latex(den)}}}"
    return latex_str, correct_ans, p_type, options

# --- アプリ管理 (共通) ---
if 'score' not in st.session_state:
    st.session_state.update({'score':0, 'stage':1, 'lives':3, 'answered':False})
    st.session_state.problem_data = generate_problem(1)

st.title("♾️ 極限突破！リミットバトル Ver.6")

if st.session_state.lives <= 0:
    st.error("💀 GAME OVER")
    if st.button("リトライ"):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()
else:
    col_st, col_main = st.columns([1, 3])
    with col_st:
        st.metric("Stage", st.session_state.stage)
        st.metric("Score", st.session_state.score)
        st.error(f"HP: {'❤️' * st.session_state.lives}")

    with col_main:
        latex_q, correct_ans, p_type, options = st.session_state.problem_data
        st.info(f"Target: {p_type}")
        st.latex(latex_q)
        cols = st.columns(2)
        for i, opt in enumerate(options):
            with cols[i % 2]:
                if st.button(opt, key=f"b_{opt}_{st.session_state.score}", use_container_width=True, disabled=st.session_state.answered):
                    st.session_state.answered = True
                    if opt == correct_ans:
                        st.success(f"正解！ 答え: {correct_ans}")
                        st.session_state.score += 1
                        if st.session_state.score % 2 == 0:
                            st.session_state.stage += 1
                            st.balloons()
                    else:
                        st.error(f"ミス！ 正解は {correct_ans}")
                        st.session_state.lives -= 1

        if st.session_state.answered:
            if st.button("次の問題へ ➡️", type="primary"):
                st.session_state.problem_data = generate_problem(st.session_state.stage)
                st.session_state.answered = False
                st.rerun()

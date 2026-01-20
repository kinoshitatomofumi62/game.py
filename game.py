import streamlit as st
import sympy as sp
import random

st.set_page_config(page_title="極限突破！リミットバトル Ver.8", page_icon="♾️", layout="wide")

def generate_problem(stage):
    x = sp.Symbol('x')
    
    # ステージによる出現パターンの管理
    patterns = ["polynomial", "trig_basic"]
    if stage >= 3: patterns.append("rationalize")
    if stage >= 5: patterns.append("trig_advanced_cos")
    if stage >= 7: patterns.append("inf_limit")
    if stage >= 9: patterns.append("squeeze")      # はさみうち(NEW!)
    if stage >= 10: patterns.append("inf_minus_inf") # 無限-無限(NEW!)
    
    pattern = random.choice(patterns) if stage >= 10 else patterns[min(stage-1, len(patterns)-1)]

    if pattern == "polynomial":
        a = random.randint(2, 6) * random.choice([-1, 1])
        k = random.randint(1, 5)
        num, den = sp.expand((x - a) * (x + k)), sp.expand(x - a)
        limit_val, ans = a, a + k
        dummies = {str(a-k), str(-(a+k)), "0", str(a)}
        
    elif pattern == "trig_basic":
        a, b = random.randint(2, 9), random.randint(2, 9)
        num, den = sp.sin(a * x), b * x
        limit_val, ans = 0, sp.Rational(a, b)
        dummies = {f"{b}/{a}", "1", str(a), "0"}

    elif pattern == "rationalize":
        a = random.randint(1, 5)
        num, den = sp.sqrt(x + a**2) - a, x
        limit_val, ans = 0, sp.Rational(1, 2 * a)
        dummies = {str(2*a), f"1/{a}", "0", "1/2"}

    elif pattern == "inf_limit":
        a, b = random.randint(2, 8), random.randint(2, 8)
        num, den = a * x**2 + random.randint(1,9)*x, b * x**2 + 1
        limit_val, ans = sp.oo, sp.Rational(a, b)
        dummies = {"0", "oo", f"{b}/{a}", "1"}

    elif pattern == "trig_advanced_cos":
        a = random.randint(2, 5)
        num, den = 1 - sp.cos(a * x), x**2
        limit_val, ans = 0, sp.Rational(a**2, 2)
        dummies = {str(a**2), f"{a}/2", "1/2", f"{a**2}/4"}

    elif pattern == "squeeze":
        # はさみうちの原理: sin(x)/x (x -> oo) など
        a = random.randint(2, 5)
        num, den = sp.sin(a * x), x
        limit_val, ans = sp.oo, 0
        dummies = {str(a), "1", "oo", f"1/{a}"}

    elif pattern == "inf_minus_inf":
        # 無限 - 無限 (有理化が必要なタイプ)
        # sqrt(x^2 + ax) - x -> a/2
        a = random.randint(2, 8)
        num = sp.sqrt(x**2 + a*x) - x
        den = 1
        limit_val, ans = sp.oo, sp.Rational(a, 2)
        dummies = {str(a), str(a*2), f"1/{a}", "0", "oo"}

    correct_ans = str(ans)
    if correct_ans in dummies: dummies.remove(correct_ans)
    options = random.sample(list(dummies), 3) + [correct_ans]
    random.shuffle(options)
    
    # 無限-無限の時は分数形式にしない表示
    if pattern == "inf_minus_inf":
        latex_str = rf"\lim_{{x \to {sp.latex(limit_val)}}} \left( {sp.latex(num)} \right)"
    else:
        latex_str = rf"\lim_{{x \to {sp.latex(limit_val)}}} \frac{{{sp.latex(num)}}}{{{sp.latex(den)}}}"
    return latex_str, correct_ans, options

# --- アプリ管理 ---
if 'score' not in st.session_state:
    st.session_state.update({'score':0, 'stage':1, 'lives':3, 'answered':False})
    st.session_state.problem_data = generate_problem(1)

st.title("♾️ 極限突破！リミットバトル")

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
        latex_q, correct_ans, options = st.session_state.problem_data
        st.write("### この極限値を求めよ：")
        st.latex(latex_q)
        st.write("---")
        cols = st.columns(2)
        for i, opt in enumerate(options):
            with cols[i % 2]:
                if st.button(opt, key=f"b_{opt}_{st.session_state.score}", use_container_width=True, disabled=st.session_state.answered):
                    st.session_state.answered = True
                    if opt == correct_ans:
                        st.success(f"正解！ (答え: {correct_ans})")
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

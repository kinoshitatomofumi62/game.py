import streamlit as st
import sympy as sp
import random

st.set_page_config(page_title="極限突破！リミットバトル Ver.11", page_icon="♾️", layout="wide")

def generate_problem(stage):
    x = sp.Symbol('x', real=True)
    
    # 出現パターンの抽選
    patterns = ["polynomial", "trig_basic"]
    if stage >= 3: patterns.append("rationalize")
    if stage >= 5: patterns.append("trig_advanced_cos")
    if stage >= 7: patterns.append("inf_limit")
    if stage >= 9: patterns.append("squeeze")      
    if stage >= 10: patterns.append("minus_inf") 
    
    pattern = random.choice(patterns) if stage >= 10 else patterns[min(stage-1, len(patterns)-1)]

    # --- 各パターンの生成ロジック ---
    if pattern == "minus_inf":
        # x -> -oo の符号の罠
        a = random.randint(2, 6)
        num, den, limit_val, ans = sp.sqrt(x**2 + a*x), x, -sp.oo, -1
        dummies = {1, 0, a, -a, sp.oo, -sp.oo}

    elif pattern == "polynomial":
        a, k = random.randint(2, 6) * random.choice([-1, 1]), random.randint(1, 5)
        num, den, limit_val, ans = sp.expand((x-a)*(x+k)), x-a, a, a+k
        dummies = {a-k, -(a+k), 0, 1, k, -k}
        
    elif pattern == "trig_basic":
        a, b = random.randint(2, 9), random.randint(2, 9)
        num, den, limit_val, ans = sp.sin(a*x), b*x, 0, sp.Rational(a, b)
        dummies = {sp.Rational(b, a), 1, 0, a, b, sp.Rational(a+1, b)}

    elif pattern == "rationalize":
        a = random.randint(1, 5)
        num, den, limit_val, ans = sp.sqrt(x + a**2) - a, x, 0, sp.Rational(1, 2*a)
        dummies = {2*a, sp.Rational(1, a), 0, sp.Rational(1, 2), a}

    elif pattern == "inf_limit":
        a, b = random.randint(2, 8), random.randint(2, 8)
        num, den, limit_val, ans = a*x**2 + random.randint(1,9)*x, b*x**2 + 1, sp.oo, sp.Rational(a, b)
        dummies = {0, sp.oo, sp.Rational(b, a), 1, sp.Rational(a, 1)}

    elif pattern == "trig_advanced_cos":
        a = random.randint(2, 5)
        num, den, limit_val, ans = 1 - sp.cos(a*x), x**2, 0, sp.Rational(a**2, 2)
        dummies = {a**2, sp.Rational(a, 2), sp.Rational(1, 2), a}

    elif pattern == "squeeze":
        a = random.randint(2, 5)
        if random.random() > 0.5:
            num, den, limit_val, ans = sp.sin(a*x), x, sp.oo, 0
            dummies = {1, a, sp.oo, -1}
        else:
            num, den, limit_val, ans = sp.sin(a*x), x, 0, a
            dummies = {1, 0, a**2, sp.Rational(1, a)}
    
    else: # inf_minus_inf
        a = random.randint(2, 8)
        num, den, limit_val, ans = sp.sqrt(x**2 + a*x) - x, 1, sp.oo, sp.Rational(a, 2)
        dummies = {a, 0, sp.oo, 1}

    # --- 共通の整形・エラー回避処理 ---
    def format_opt(val):
        if val == sp.oo: return "∞"
        if val == -sp.oo: return "-∞"
        return str(sp.simplify(val))

    correct_ans_str = format_opt(ans)
    
    # 重複を排除し、文字列のリストにする
    final_dummies = list({format_opt(d) for d in dummies if format_opt(d) != correct_ans_str})
    
    # 【重要】もし候補が3つ未満なら、適当な数字を足して強制的に4択にする（ValueError回避）
    extra_candidates = ["2", "-2", "3", "1/3", "-1", "4", "1/4"]
    for extra in extra_candidates:
        if len(final_dummies) >= 3: break
        if extra != correct_ans_str and extra not in final_dummies:
            final_dummies.append(extra)

    options = random.sample(final_dummies, 3) + [correct_ans_str]
    random.shuffle(options)
    
    # 数式表示の切り替え
    if pattern in ["minus_inf", "inf_minus_inf"] and den == 1:
        latex_str = rf"\lim_{{x \to {sp.latex(limit_val)}}} \left( {sp.latex(num)} \right)"
    else:
        latex_str = rf"\lim_{{x \to {sp.latex(limit_val)}}} \frac{{{sp.latex(num)}}}{{{sp.latex(den)}}}"
    
    return latex_str, correct_ans_str, options

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

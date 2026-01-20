import streamlit as st
import sympy as sp
import random

st.set_page_config(page_title="極限突破！リミットバトル", page_icon="♾️", layout="wide")

def generate_problem(stage):
    x = sp.Symbol('x')
    
    # ステージ進行による難易度設定
    # ステージが上がるごとに数値の範囲を大きく、公式を複雑にする
    difficulty = stage // 2  # 2ステージごとに基本数値が上がる
    
    if stage == 1:
        pattern = "polynomial"
    elif stage == 2:
        pattern = "trig_basic"
    elif stage == 3:
        pattern = "trig_advanced_cos"
    elif stage == 4:
        pattern = "trig_advanced_tan"
    else:
        # ステージ5以降は全パターンからランダム（係数が大きい）
        pattern = random.choice(["polynomial", "trig_basic", "trig_advanced_cos", "trig_advanced_tan"])

    if pattern == "polynomial":
        # 因数分解型: 係数を大きくして暗算を少し難しくする
        a = random.randint(1, 5 + difficulty) * random.choice([-1, 1])
        k = random.randint(1, 5 + difficulty) * random.choice([-1, 1])
        num = sp.expand((x - a) * (x + k))
        den = sp.expand(x - a)
        limit_val = a
        p_type = "不定形の解消（因数分解）"
        ans = a + k
        # ひっかけ：符号ミス、代入ミス(0)、定数項ミスなど
        dummies = {str(a-k), str(-(a+k)), str(0), str(a*k), str(k), str(a)}
        
    elif pattern == "trig_basic":
        # sin(ax)/bx 型: 係数を複雑にする
        a = random.randint(2, 7 + difficulty)
        b = random.randint(2, 7 + difficulty)
        num = sp.sin(a * x)
        den = b * x
        limit_val = 0
        p_type = "三角関数の基本公式"
        ans = sp.Rational(a, b)
        # ひっかけ：逆数、係数の和、係数の差、1
        dummies = {f"{b}/{a}", str(sp.Rational(b, a)), "1", str(a), str(b), f"{a+b}/{b}"}
        
    elif pattern == "trig_advanced_cos":
        # (1-cos ax)/x^2 型
        a = random.randint(2, 4 + difficulty)
        num = 1 - sp.cos(a * x)
        den = x**2
        limit_val = 0
        ans = sp.Rational(a**2, 2)
        p_type = "1-cosの応用（2乗に注意）"
        # ひっかけ：1/2にするのを忘れる、2乗し忘れる、逆数
        dummies = {str(a**2), str(sp.Rational(a, 2)), f"1/{a**2}", str(sp.Rational(a**2, 1)), "1/2", str(a)}

    else: # trig_advanced_tan
        # tan ax / sin bx 型
        a = random.randint(2, 6 + difficulty)
        b = random.randint(2, 6 + difficulty)
        if a == b: b += 1
        num = sp.tan(a * x)
        den = sp.sin(b * x)
        limit_val = 0
        ans = sp.Rational(a, b)
        p_type = "tanとsinの混在（公式の組合せ）"
        dummies = {f"{b}/{a}", "1", "0", str(a*b), f"{a}/{a+b}", f"{a-b}/{b}"}

    correct_ans = str(ans)
    if correct_ans in dummies:
        dummies.remove(correct_ans)
    
    # 選択肢の質を上げるため、数値が近いものを優先
    sample_list = list(dummies)
    random.shuffle(sample_list)
    options = sample_list[:3] + [correct_ans]
    random.shuffle(options)
    
    latex_str = rf"\lim_{{x \to {limit_val}}} \frac{{{sp.latex(num)}}}{{{sp.latex(den)}}}"
    return latex_str, correct_ans, p_type, options

# --- アプリ構造 ---
if 'score' not in st.session_state:
    st.session_state.score = 0
    st.session_state.stage = 1
    st.session_state.lives = 3
    st.session_state.answered = False
    st.session_state.problem_data = generate_problem(st.session_state.stage)

st.title("♾️ 極限突破！リミットバトル Ver.4")

if st.session_state.get('game_over', False) or st.session_state.lives <= 0:
    st.error("💀 GAME OVER")
    st.header(f"到達ステージ: {st.session_state.stage} | スコア: {st.session_state.score}")
    if st.button("リトライ"):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()
else:
    col_st, col_main = st.columns([1, 3])
    
    with col_st:
        st.subheader("📊 Status")
        st.metric("Stage", st.session_state.stage)
        st.metric("Score", st.session_state.score)
        st.write("---")
        st.error(f"HP: {'❤️' * st.session_state.lives}")

    with col_main:
        latex_q, correct_ans, p_type, options = st.session_state.problem_data
        st.info(f"Target: {p_type}")
        st.latex(latex_q)

        st.write("答えを選べ！")
        cols = st.columns(2)
        for i, opt in enumerate(options):
            with cols[i % 2]:
                if st.button(opt, key=f"b_{opt}_{st.session_state.score}", use_container_width=True, disabled=st.session_state.answered):
                    st.session_state.answered = True
                    if opt == correct_ans:
                        st.success(f"正解！ 答え: {correct_ans}")
                        st.session_state.score += 1
                        if st.session_state.score % 2 == 0: # 2問ごとにステージアップ（速め）
                            st.session_state.stage += 1
                            st.balloons()
                    else:
                        st.error(f"ミス！ 正解は {correct_ans}")
                        st.session_state.lives -= 1

        if st.session_state.answered:
            if st.button("次の問題へ進む ➡️", type="primary"):
                st.session_state.problem_data = generate_problem(st.session_state.stage)
                st.session_state.answered = False
                st.rerun()

import streamlit as st
import sympy as sp
import random

st.set_page_config(page_title="極限突破！リミットバトル", page_icon="♾️")

# --- 問題生成ロジック ---
def generate_problem(stage):
    x = sp.Symbol('x')
    
    # ステージに応じた出現パターン
    if stage == 1:
        pattern = "polynomial"
    elif stage == 2:
        pattern = "trig_basic"
    else:
        # ステージ3以上は全パターン＋難問
        pattern = random.choice(["polynomial", "trig_basic", "trig_advanced"])
    
    if pattern == "polynomial":
        a = random.randint(-3, 5)
        k = random.randint(-3, 5)
        num = sp.expand((x - a) * (x + k))
        den = sp.expand(x - a)
        limit_val = a
        p_type = "因数分解"
        ans = a + k
        dummies = {str(0), str(-(a + k)), str(a - k), str(a + k + 1)}
        
    elif pattern == "trig_basic":
        a = random.randint(1, 6)
        b = random.randint(1, 6)
        num = sp.sin(a * x)
        den = b * x
        limit_val = 0
        p_type = "三角関数の基本"
        ans = sp.Rational(a, b)
        dummies = {f"{b}/{a}", str(a), str(b), "1"}
        
    else: # trig_advanced (Stage 3以降の難問)
        choice = random.choice(["cos", "tan"])
        limit_val = 0
        if choice == "cos":
            a = random.randint(1, 4)
            num = 1 - sp.cos(a * x)
            den = x**2
            ans = sp.Rational(a**2, 2)
            p_type = "三角関数(1-cos型)"
            dummies = {str(a**2), str(a), f"{a}/2", "0"}
        else:
            a = random.randint(2, 5)
            num = sp.tan(a * x)
            den = sp.sin(random.randint(1, 3) * x)
            ans = sp.limit(num/den, x, 0)
            p_type = "三角関数(tan混在型)"
            dummies = {"1", str(a), "0", "1/2"}

    correct_ans = str(ans)
    dummies.discard(correct_ans)
    options = random.sample(list(dummies), 3) + [correct_ans]
    random.shuffle(options)
    
    latex_str = rf"\lim_{{x \to {limit_val}}} \frac{{{sp.latex(num)}}}{{{sp.latex(den)}}}"
    return latex_str, correct_ans, p_type, options

# --- セッション状態の初期化 ---
if 'score' not in st.session_state:
    st.session_state.score = 0
    st.session_state.stage = 1
    st.session_state.lives = 3
    st.session_state.game_over = False
    st.session_state.answered = False
    st.session_state.problem_data = generate_problem(st.session_state.stage)

# --- ゲーム画面 ---
st.title("♾️ 極限突破！リミットバトル")

# サイドバーにステータス表示
st.sidebar.header("ステータス")
st.sidebar.metric("スコア", st.session_state.score)
st.sidebar.metric("ステージ", st.session_state.stage)
st.sidebar.subheader("ライフ")
st.sidebar.error("❤️ " * st.session_state.lives)

if st.session_state.game_over:
    st.error("⚠️ ゲームオーバー！")
    st.header(f"最終スコア: {st.session_state.score}")
    st.write(f"到達ステージ: {st.session_state.stage}")
    if st.button("タイトルに戻ってやり直す"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()
else:
    latex_q, correct_ans, p_type, options = st.session_state.problem_data
    
    st.subheader(f"Stage {st.session_state.stage}: {p_type}")
    st.latex(latex_q)

    # 選択肢
    cols = st.columns(2)
    for i, opt in enumerate(options):
        with cols[i % 2]:
            if st.button(opt, key=f"btn_{opt}", use_container_width=True, disabled=st.session_state.answered):
                st.session_state.answered = True
                if opt == correct_ans:
                    st.success("✨ 正解！モンスターを撃破！ ✨")
                    st.session_state.score += 1
                    # 3問ごとにステージアップ
                    if st.session_state.score % 3 == 0:
                        st.session_state.stage += 1
                        st.balloons()
                else:
                    st.error(f"残念！ダメージを受けた！ (正解: {correct_ans})")
                    st.session_state.lives -= 1
                    if st.session_state.lives <= 0:
                        st.session_state.game_over = True

    # 次へボタン
    if st.session_state.answered and not st.session_state.game_over:
        if st.button("次のモンスターが現れた！ ➡️", type="primary"):
            st.session_state.problem_data = generate_problem(st.session_state.stage)
            st.session_state.answered = False
            st.rerun()

if st.sidebar.button("最初からやり直す"):
    for key in st.session_state.keys():
        del st.session_state[key]
    st.rerun()

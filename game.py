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
    dummies.discard(correct_ans) # 正解と被ったら消す
    
    # 常に3つのダミーをランダム抽出して4択にする
    options = random.sample(list(dummies), 3) + [correct_ans]
    random.shuffle(options)
    
    latex_str = rf"\lim_{{x \to {limit_val}}} \frac{{{sp.latex(num)}}}{{{sp.latex(den)}}}"
    return latex_str, correct_ans, p_type, options

# --- セッション状態の管理 ---
if 'score' not in st.session_state:
    st.session_state.score = 0
    st.session_state.stage = 1
    st.session_state.lives = 3
    st.session_state.game_over = False
    st.session_state.answered = False
    st.session_state.problem_data = generate_problem(st.session_state.stage)

# --- 画面表示 ---
st.title("♾️ 極限突破！リミットバトル")

if st.session_state.game_over:
    st.error("💀 ライフが 0 になりました...")
    st.header(f"最終結果：Stage {st.session_state.stage}（スコア {st.session_state.score}）")
    if st.button("もう一度最初から挑戦する"):
        for key in st.session_state.keys(): del st.session_state[key]
        st.rerun()
else:
    # 左右のレイアウト設定
    col_left, col_right = st.columns([1, 2])
    
    with col_left:
        st.subheader("🛡️ ステータス")
        st.write(f"**現在のステージ:** {st.session_state.stage}")
        st.write(f"**スコア:** {st.session_state.score}")
        st.error(f"**ライフ:** {'❤️' * st.session_state.lives}")
        st.write("---")
        st.write("※画像は準備中です。")

    with col_right:
        latex_q, correct_ans, p_type, options = st.session_state.problem_data
        st.info(f"ターゲット：{p_type}")
        st.latex(latex_q)

        # 4択ボタン
        st.write("答えを選んでください：")
        cols = st.columns(2)
        for i, opt in enumerate(options):
            with cols[i % 2]:
                # 回答後はボタンを押せなくする
                if st.button(opt, key=f"btn_{opt}_{st.session_state.score}", use_container_width=True, disabled=st.session_state.answered):
                    st.session_state.answered = True
                    if opt == correct_ans:
                        st.success("正解！モンスターを倒した！")
                        st.session_state.score += 1
                        if st.session_state.score % 3 == 0:
                            st.session_state.stage += 1
                            st.balloons()
                    else:
                        st.error(f"ミス！ダメージを受けた！ (正解は {correct_ans})")
                        st.session_state.lives -= 1
                        if st.session_state.lives <= 0:
                            st.session_state.game_over = True

        # 回答後に次の問題ボタンを表示
        if st.session_state.answered and not st.session_state.game_over:
            if st.button("次のモンスターへ進む ➡️", type="primary"):
                st.session_state.problem_data = generate_problem(st.session_state.stage)
                st.session_state.answered = False
                st.rerun()

st.sidebar.caption("数Ⅲ 極限トレーニングアプリ v2.0")

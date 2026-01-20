import streamlit as st
import sympy as sp
import random

# ページ設定
st.set_page_config(page_title="極限突破！リミットバトル", page_icon="♾️", layout="wide")

# --- 問題生成ロジック（エラーを徹底排除） ---
def generate_problem(stage):
    x = sp.Symbol('x')
    
    # ステージによる難易度分け（eは出さない）
    if stage == 1:
        pattern = "polynomial" # 因数分解
    elif stage == 2:
        pattern = "trig_basic" # 三角関数基本
    else:
        pattern = random.choice(["polynomial", "trig_basic", "trig_advanced"])
    
    if pattern == "polynomial":
        a = random.randint(-3, 5)
        k = random.randint(-3, 5)
        num = sp.expand((x - a) * (x + k))
        den = sp.expand(x - a)
        limit_val = a
        p_type = "因数分解による解消"
        ans = a + k
        # ひっかけの選択肢
        dummies = {str(0), str(-(a + k)), str(a - k), str(a + k + 1), str(a + 2), str(k), "1", "-1"}
        
    elif pattern == "trig_basic":
        a = random.randint(1, 6)
        b = random.randint(1, 6)
        num = sp.sin(a * x)
        den = b * x
        limit_val = 0
        p_type = "三角関数の基本公式"
        ans = sp.Rational(a, b)
        dummies = {f"{b}/{a}", str(a), str(b), "1", "0", "1/2", f"{a+1}/{b}", "2"}
        
    else: # Stage 3以降
        choice = random.choice(["cos", "tan"])
        limit_val = 0
        if choice == "cos":
            a = random.randint(1, 4)
            num = 1 - sp.cos(a * x)
            den = x**2
            ans = sp.Rational(a**2, 2)
            p_type = "1-cosの極限公式"
            dummies = {str(a**2), str(a), f"{a}/2", "0", "1", f"{a**2}/4", "1/2", "1/4"}
        else:
            a = random.randint(2, 5)
            num = sp.tan(a * x)
            den = sp.sin(random.randint(1, 2) * x)
            ans = sp.limit(num/den, x, 0)
            p_type = "tanとsinの公式応用"
            dummies = {"1", str(a), "0", "1/2", str(a*2), "3", "2/3", "4"}

    correct_ans = str(ans)
    if correct_ans in dummies:
        dummies.remove(correct_ans)
    
    # エラー回避のため、必ず要素数を確保してから抽出
    sample_list = list(dummies)
    random.shuffle(sample_list)
    options = sample_list[:3] + [correct_ans]
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

if st.session_state.game_over:
    st.error("💀 ライフが 0 になりました。修行し直してきましょう。")
    st.header(f"今回のスコア: {st.session_state.score}")
    if st.button("もう一度最初から挑戦する"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
else:
    # 左右のレイアウト
    col_status, col_main = st.columns([1, 2])
    
    with col_status:
        st.subheader("🛡️ ステータス")
        st.metric("現在のスコア", st.session_state.score)
        st.metric("ステージ", st.session_state.stage)
        st.write("---")
        st.subheader("ライフ")
        st.error("❤️ " * st.session_state.lives)
        st.caption("※3問正解でステージアップ！")

    with col_main:
        latex_q, correct_ans, p_type, options = st.session_state.problem_data
        st.info(f"ターゲットモンスター：{p_type}")
        st.latex(latex_q)

        st.write("答えを選択してください：")
        cols = st.columns(2)
        for i, opt in enumerate(options):
            with cols[i % 2]:
                if st.button(opt, key=f"btn_{opt}_{st.session_state.score}", use_container_width=True, disabled=st.session_state.answered):
                    st.session_state.answered = True
                    if opt == correct_ans:
                        st.success(f"✨ 正解！ モンスターを倒した！ (答え: {correct_ans})")
                        st.session_state.score += 1
                        if st.session_state.score % 3 == 0:
                            st.session_state.stage += 1
                            st.balloons()
                    else:
                        st.error(f"💥 痛恨のミス！ ダメージを受けた！ (正解: {correct_ans})")
                        st.session_state.lives -= 1
                        if st.session_state.lives <= 0:
                            st.session_state.game_over = True

        if st.session_state.answered and not st.session_state.game_over:
            if st.button("次のモンスターが現れた！ ➡️", type="primary"):
                st.session_state.problem_data = generate_problem(st.session_state.stage)
                st.session_state.answered = False
                st.rerun()

st.sidebar.caption("数Ⅲ 極限攻略アプリ v3.0")

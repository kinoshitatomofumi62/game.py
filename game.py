import sympy as sp
import random

def generate_problem():
    x = sp.Symbol('x')
    pattern = random.choice(["polynomial", "trig", "exp"])
    
    if pattern == "polynomial":
        # 因数分解型: (x-a)(x+k) / (x-a)
        a = random.randint(-3, 5)
        k = random.randint(-3, 5)
        numerator = sp.expand((x - a) * (x + k))
        denominator = sp.expand(x - a)
        limit_val = a
        problem_type = "因数分解"
        
    elif pattern == "trig":
        # 三角関数型: sin(ax) / bx
        a = random.randint(2, 5)
        b = random.randint(2, 5)
        numerator = sp.sin(a * x)
        denominator = b * x
        limit_val = 0
        problem_type = "三角関数の公式"
        
    else:
        # eの定義型: (1 + 1/x)^(ax)
        a = random.randint(2, 4)
        numerator = (1 + 1/x)**(a*x)
        denominator = 1 # 非分数形式
        limit_val = sp.oo # 無限大
        problem_type = "自然対数の底 e"

    expr = numerator / denominator
    answer = sp.limit(expr, x, limit_val)
    
    # 表示用の式を作成
    limit_symbol = "∞" if limit_val == sp.oo else limit_val
    question_str = f"lim_{{x -> {limit_symbol}}}  ({numerator}) / ({denominator})"
    if denominator == 1:
        question_str = f"lim_{{x -> {limit_symbol}}}  {numerator}"

    return question_str, str(answer), problem_type

def play_game():
    score = 0
    total_rounds = 5 # まずは5問でお試し
    
    print("=== 数学Ⅲ：極限突破クイズ ===")
    print("答えが分数の場合は '1/2'、eの2乗の場合は 'e**2' のように入力してください。")
    print("-" * 30)

    for i in range(1, total_rounds + 1):
        question, correct_answer, p_type = generate_problem()
        print(f"\n第 {i} 問 [{p_type}]")
        print(f"問題: {question}")
        
        user_input = input("答えは？ > ").strip()
        
        # SymPyで比較するためにユーザー入力をパース（簡易判定）
        if user_input.replace(" ", "") == correct_answer.replace(" ", ""):
            print("★ 正解！ ★")
            score += 1
        else:
            print(f"残念... 正解は {correct_answer} でした。")

    print("-" * 30)
    print(f"ゲーム終了！ あなたのスコアは {score} / {total_rounds} です。")

if __name__ == "__main__":
    play_game()
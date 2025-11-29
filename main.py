import streamlit as st
import math

# --- 페이지 설정 ---
st.set_page_config(
    page_title="고급 계산기 웹앱",
    layout="wide"
)

st.title("🔢 스트림릿 고급 계산기 웹앱")
st.markdown("---")

# --- 입력 섹션 ---
st.header("입력 값")

# 사용자가 입력할 두 개의 숫자 필드
# 로그 연산의 밑과 진수를 고려하여 두 번째 숫자를 '피연산자 2 / 지수 / 진수'로 레이블링
col1, col2 = st.columns(2)

with col1:
    number1 = st.number_input("**첫 번째 숫자 (혹은 밑)**", value=0.0, format="%.4f", key="num1")

with col2:
    number2 = st.number_input("**두 번째 숫자 (혹은 지수 / 진수)**", value=0.0, format="%.4f", key="num2")
    # 로그 연산 시 진수 조건에 대한 안내
    if st.session_state.num2 <= 0 and st.session_state.operation == "로그연산 (log)":
        st.error("로그 연산의 진수는 0보다 커야 합니다.")

st.markdown("---")

# --- 연산 선택 섹션 ---
st.header("연산 선택")

# 사용자가 선택할 연산 드롭다운 메뉴
operation_list = [
    "덧셈 (+)", "뺄셈 (-)", "곱셈 (*)", "나눗셈 (/)",
    "모듈러연산 (%)", "지수연산 (x^y)", "로그연산 (log)"
]

st.session_state.operation = st.selectbox(
    "수행할 연산을 선택하세요:",
    options=operation_list
)

st.markdown("---")

# --- 계산 및 결과 섹션 ---

def calculate(num1, num2, operation):
    """선택된 연산에 따라 결과를 계산하는 함수"""
    result = None
    error_message = None

    try:
        if operation == "덧셈 (+)":
            result = num1 + num2
        elif operation == "뺄셈 (-)":
            result = num1 - num2
        elif operation == "곱셈 (*)":
            result = num1 * num2
        elif operation == "나눗셈 (/)" and num2 != 0:
            result = num1 / num2
        elif operation == "나눗셈 (/)" and num2 == 0:
            error_message = "0으로 나눌 수 없습니다."
        elif operation == "모듈러연산 (%)" and num2 != 0:
            # 모듈러 연산은 일반적으로 정수에 대해 사용되므로, 입력값을 정수로 변환하여 계산
            result = int(num1) % int(num2)
        elif operation == "모듈러연산 (%)" and num2 == 0:
            error_message = "0으로 모듈러 연산을 할 수 없습니다."
        elif operation == "지수연산 (x^y)":
            result = num1 ** num2
        elif operation == "로그연산 (log)":
            if num1 > 0 and num1 != 1 and num2 > 0:
                # 로그 연산: math.log(진수, 밑)
                result = math.log(num2, num1)
            elif num1 <= 0 or num1 == 1:
                error_message = "로그의 밑은 0보다 크고 1이 아니어야 합니다."
            elif num2 <= 0:
                error_message = "로그의 진수는 0보다 커야 합니다."
        
    except Exception as e:
        error_message = f"계산 중 오류가 발생했습니다: {e}"
        
    return result, error_message

# '계산하기' 버튼
if st.button("**계산하기**", type="primary"):
    result, error_message = calculate(number1, number2, st.session_state.operation)

    st.header("결과")
    
    if error_message:
        st.error(f"⚠️ 오류: {error_message}")
    elif result is not None:
        st.success(f"✅ **선택하신 연산의 결과는**")
        st.info(f"$$\\text{{{number1}}} \\quad \\text{{{st.session_state.operation.split(' ')[1]}}} \\quad \\text{{{number2}}} \\quad = \\quad \\text{{{result}}}$$")
        st.metric(label=f"**{st.session_state.operation} 결과**", value=f"{result:,.4f}")
    else:
        st.warning("계산을 위해 연산을 선택하고 입력값을 확인해 주세요.")

# --- 참고: 로그 연산 설명 ---
st.sidebar.title("연산 참고")
st.sidebar.markdown("""
### 로그 연산 ($$\log_b a$$)
* **밑 (b):** 첫 번째 숫자
    * 조건: $b > 0$ 이고 $b \neq 1$
* **진수 (a):** 두 번째 숫자
    * 조건: $a > 0$
""")

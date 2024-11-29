# streamlit_app.py
import streamlit as st
from PIL import Image
import requests
from io import BytesIO

# DALL-E 스타일 API를 호출하여 로고 생성
def generate_logo(company_name, color, style, shape, use):
    prompt = f"A {style} circular logo design for a company named '{company_name}', \
              using {color} color scheme. The logo emphasizes {use} with a {shape} layout."
    # 여기서는 OpenAI API나 다른 이미지 생성 툴을 연동한다고 가정
    # 실제 사용 시, OpenAI API 키를 설정하고 호출해야 합니다
    # API 호출 부분은 예제입니다:
    response = requests.post(
        "https://api.openai.com/v1/images/generate",
        headers={"Authorization": f"Bearer YOUR_API_KEY"},
        json={"prompt": prompt, "size": "512x512"}
    )
    if response.status_code == 200:
        image_url = response.json()["data"][0]["url"]
        image = Image.open(BytesIO(requests.get(image_url).content))
        return image
    else:
        st.error("Failed to generate logo. Please check API settings.")
        return None

# Streamlit UI 구성
st.title("Logo Generator")
st.markdown("### Create your custom logo using AI!")

# 입력 폼
with st.form("logo_form"):
    company_name = st.text_input("Company Name", value="Your Company")
    color = st.selectbox("Color Palette", ["Blue", "Red", "Green", "Black", "Custom"])
    style = st.selectbox("Logo Style", ["Minimal", "Modern", "Classic", "Abstract"])
    shape = st.radio("Logo Shape", ["Circular", "Square", "Abstract"])
    use = st.text_input("Purpose (e.g., Business Card, Website)", value="General Use")
    submit = st.form_submit_button("Generate Logo")

# 로고 생성 처리
if submit:
    st.markdown(f"### Generating logo for: {company_name}")
    logo = generate_logo(company_name, color, style, shape, use)
    if logo:
        st.image(logo, caption=f"{company_name} Logo", use_column_width=True)

# 앱 실행 방법 안내
st.markdown("---")
st.markdown("#### How to Run")
st.code("streamlit run streamlit_app.py", language="bash")

# streamlit_app.py
import streamlit as st
from PIL import Image
import requests
from io import BytesIO
import os  # 환경 변수를 가져오기 위해 os 모듈을 사용합니다.

# DALL-E 스타일 API를 호출하여 로고 생성
def generate_logo(company_name, color, style, shape, use):
    prompt = f"A {style} circular logo design for a company named '{company_name}', \
              using {color} color scheme. The logo emphasizes {use} with a {shape} layout."
    
    # 환경 변수에서 API 키를 가져옵니다.
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        st.error("API key is not set. Please check your environment variables.")
        return None

    # 실제 사용 시, OpenAI API 키를 설정하고 호출해야 합니다
    response = requests.post(
        "https://api.openai.com/v1/images/generate",
        headers={"Authorization": f"Bearer {api_key}"},
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

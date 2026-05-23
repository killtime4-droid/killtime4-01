import streamlit as st
from groq import Groq
from PIL import Image
import base64
import io

GROQ_API_KEY = "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"

st.set_page_config(page_title="AI 라면 건강 분석기", page_icon="🍜", layout="centered")

st.title("🍜 AI 라면 종합 건강 영향 분석기")
st.caption("Groq + Llama 4 Scout")

st.success("✅ Groq API 연결됨")
st.divider()

upload_type = st.radio("사진 입력 방식", ["📁 갤러리 업로드", "📷 카메라 촬영"])

if upload_type == "📁 갤러리 업로드":
    uploaded_file = st.file_uploader("라면 사진을 선택하세요", type=["jpg", "jpeg", "png"])
else:
    uploaded_file = st.camera_input("라면 사진 촬영")

if st.button("🚀 AI 분석 시작하기", type="primary", use_container_width=True):
    if not uploaded_file:
        st.error("사진을 업로드해주세요!")
    else:
        with st.spinner("Groq AI가 분석 중입니다..."):
            try:
                image = Image.open(uploaded_file)
                st.image(image, caption="업로드된 라면 사진", use_container_width=True)

                client = Groq(api_key=GROQ_API_KEY)

                buffered = io.BytesIO()
                image.save(buffered, format="JPEG")
                img_str = base64.b64encode(buffered.getvalue()).decode()

                prompt = """
                당신은 라면 건강 분석 전문 AI입니다. 사진을 분석하여 한국어로 답변해주세요.
                특히 PART 3은 항목 간 간격을 최소화하고 붙여서 출력해주세요.

                ---
                :red[**PART 1. 🎯 AI 분석 정확도**]
                - 인식 정확도: XX%

                ---
                :red[**PART 2. 📊 정밀 영양성분 표**]
                (마크다운 표로 작성)

                ---
                :red[**PART 3. 🩺 4대 만성질환 영향**]
                - :blue[🧪 간 수치 영향]: 
                - :blue[🩸 콜레스테롤 영향]: 
                - :blue[🍬 당뇨 영향]: 
                - :blue[🫀 심혈관 영향]: 

                ---
                :red[**PART 4. 🚨 종합 위험도 판정**]
                - 위험 등급: [안전 / 주의 / 위험]
                - 판정 이유:

                ---
                :red[**PART 5. 💡 건강한 섭취 팁**]
                """

                response = client.chat.completions.create(
                    model="meta-llama/llama-4-scout-17b-16e-instruct",
                    messages=[{
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_str}"}}
                        ]
                    }],
                    temperature=0.4,
                    max_tokens=1300
                )

                st.success("✅ 분석 완료!")
                st.divider()
                st.markdown(response.choices[0].message.content)

            except Exception as e:
                st.error(f"❌ 분석 실패: {e}")

import streamlit as st
from PIL import Image
import io
import zipfile
from datetime import datetime
from ali_image_tool import split_ali_grid
from streamlit_paste_button import paste_image_button

st.set_page_config(page_title="阿里合集拆分专家 V4.1", page_icon="✂️")
st.markdown("""<style>.stButton>button {width: 100%;background-color: #FF6A00;color: white;font-weight: bold; height: 4em; font-size: 20px;}</style>""", unsafe_allow_html=True)

st.title("✂️ 阿里主图 3x2 合集拆分工具")
st.info("上传 3x2 布局的合集图，自动拆分为 6 张符合阿里的 1000x1000 像素、1:1 比例的高清主图。")

pasted_result = paste_image_button("📋 方式一：点击此处粘贴合集图片")
uploaded_file = st.file_uploader("📂 方式二：点击此处上传合集文件", type=["jpg", "jpeg", "png", "webp"])

target_img = None
if pasted_result: target_img = pasted_result.image_data
elif uploaded_file: target_img = Image.open(uploaded_file)

if target_img:
    st.image(target_img, caption="📸 已加载图片预览", use_container_width=True)
    if st.button("✂️ 立即开始 3x2 自动拆分"):
        results = split_ali_grid(target_img)
        if results:
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
                st.write("### 预览拆分后的 6 张主图")
                cols = st.columns(3)
                for i, (name, img_obj) in enumerate(results):
                    buf = io.BytesIO()
                    img_obj.save(buf, format='JPEG', quality=95)
                    zip_file.writestr(name, buf.getvalue())
                    with cols[i % 3]: st.image(img_obj, caption=f"主图 {i+1}", use_container_width=True)
            st.write("---")
            st.download_button("📥 下载全部 6 张主图 (ZIP)", zip_buffer.getvalue(), f"Ali_Split_{datetime.now().strftime('%H%M%S')}.zip", "application/zip")
else:
    st.info("💡 请先粘贴或上传 3x2 合集大图以开始。")

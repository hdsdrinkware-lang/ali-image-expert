import streamlit as st
from PIL import Image
import io
import zipfile
from datetime import datetime
from ali_image_tool import get_ali_images, split_ali_grid

st.set_page_config(page_title="阿里主图 3x2 拆分专家", page_icon="🖼️")
st.markdown("""<style>.stButton>button {width: 100%;background-color: #FF6A00;color: white;font-weight: bold;}</style>""", unsafe_allow_html=True)
st.title("🖼️ 阿里主图 3x2 合集自动拆分工具")
st.info("上传 3x2 合集大图，自动切割并优化为 6 张 1:1 高清主图。")
uploaded_file = st.file_uploader("上传您的合集图", type=["jpg", "jpeg", "png", "webp"])
if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="原图预览", use_container_width=True)
    if st.button("🚀 自动拆分并优化"):
        results = split_ali_grid(img)
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            cols = st.columns(3)
            for i, (name, img_obj) in enumerate(results):
                buf = io.BytesIO()
                img_obj.save(buf, format='JPEG', quality=95)
                zip_file.writestr(name, buf.getvalue())
                with cols[i % 3]:
                    st.image(img_obj, caption=f"优化后主图 {i+1}", use_container_width=True)
        st.download_button("📥 下载全部 6 张主图 (ZIP)", zip_buffer.getvalue(), f"ali_images.zip", "application/zip")

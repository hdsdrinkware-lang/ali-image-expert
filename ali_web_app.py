import streamlit as st
from PIL import Image
import io
import zipfile
from datetime import datetime
from ali_image_tool import get_ali_images

st.set_page_config(page_title="阿里国际站主图专家", page_icon="🖼️")
st.markdown("""<style>.stButton>button {width: 100%;background-color: #FF6A00;color: white;}</style>""", unsafe_allow_html=True)
st.title("🖼️ 阿里国际站主图自动生成器")
uploaded_file = st.file_uploader("上传产品原图", type=["jpg", "jpeg", "png", "webp"])
if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="原图预览", use_container_width=True)
    if st.button("🚀 开始生成 6 张主图"):
        results = get_ali_images(img)
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            cols = st.columns(3)
            for i, (name, img_obj) in enumerate(results):
                buf = io.BytesIO()
                img_obj.save(buf, format='JPEG', quality=95)
                zip_file.writestr(name, buf.getvalue())
                with cols[i % 3]:
                    st.image(img_obj, caption=f"主图 {i+1}", use_container_width=True)
        st.download_button("📥 一键下载全部主图 (ZIP)", zip_buffer.getvalue(), f"ali_images.zip", "application/zip")

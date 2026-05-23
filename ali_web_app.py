import streamlit as st
from PIL import Image
import io
import zipfile
from datetime import datetime
from ali_image_tool import split_ali_grid
from streamlit_paste_button import paste_image_button

st.set_page_config(page_title="阿里合集拆分专家 V4.5", page_icon="✂️")
st.markdown("""<style>.stButton>button {width: 100%;background-color: #FF6A00;color: white;font-weight: bold;height: 3.5em;}</style>""", unsafe_allow_html=True)
st.title("✂️ 阿里主图合集拆分工具 V4.5")
pasted_result = paste_image_button("📋 方式一：粘贴图片")
uploaded_file = st.file_uploader("📂 方式二：上传文件", type=["jpg", "jpeg", "png", "webp"])
target_img = None
if pasted_result is not None and pasted_result.image_data is not None:
    target_img = pasted_result.image_data
elif uploaded_file is not None:
    target_img = Image.open(uploaded_file)
if target_img:
    st.image(target_img, use_container_width=True)
    st.write("### 请选择图片布局：")
    c1, c2 = st.columns(2)
    results = None
    if c1.button("📐 3列 x 2行 (横向宽图)"): results = split_ali_grid(target_img, 3, 2)
    if c2.button("📐 2列 x 3行 (纵向长图)"): results = split_ali_grid(target_img, 2, 3)
    if results:
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            grid = st.columns(3)
            for i, (name, img_obj) in enumerate(results):
                buf = io.BytesIO()
                img_obj.save(buf, format='JPEG', quality=95)
                zip_file.writestr(name, buf.getvalue())
                with grid[i % 3]: st.image(img_obj, caption=f"主图 {i+1}", use_container_width=True)
        st.download_button("📥 下载全部 6 张主图 (ZIP)", zip_buffer.getvalue(), "Ali_Split.zip", "application/zip")

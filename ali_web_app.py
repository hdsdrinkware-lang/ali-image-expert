import streamlit as st
from PIL import Image
import io
import zipfile
from datetime import datetime
from ali_image_tool import get_ali_images, split_ali_grid
from streamlit_paste_button import paste_image_button

st.set_page_config(page_title="阿里主图专家 V3.0", page_icon="🖼️")
st.markdown("""<style>.stButton>button {width: 100%;background-color: #FF6A00;color: white;font-weight: bold;}</style>""", unsafe_allow_html=True)
st.title("🖼️ 阿里主图裁切专家 V3.0")
st.info("功能：1. 自动拆分 3x2 合集；2. 单图转细节；3. 支持粘贴图片；4. 尺寸 1254x1254。")
pasted_result = paste_image_button("📋 点击此处粘贴图片 (Clipboard)")
uploaded_file = st.file_uploader("或上传图片文件", type=["jpg", "jpeg", "png", "webp"])
target_img = None
if pasted_result: target_img = pasted_result.image_data
elif uploaded_file: target_img = Image.open(uploaded_file)
if target_img:
    st.image(target_img, caption="预览", use_container_width=True)
    c1, c2 = st.columns(2)
    if c1.button("✂️ 3x2 合集拆分"):
        results = split_ali_grid(target_img)
        mode = "split"
    elif c2.button("🔍 单图生成细节"):
        results = get_ali_images(target_img)
        mode = "zoom"
    else: results = None
    if results:
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            cols = st.columns(3)
            for i, (name, img_obj) in enumerate(results):
                buf = io.BytesIO()
                img_obj.save(buf, format='JPEG', quality=95)
                zip_file.writestr(name, buf.getvalue())
                with cols[i % 3]: st.image(img_obj, caption=f"图 {i+1}", use_container_width=True)
        st.download_button("📥 下载全部 6 张高清图 (ZIP)", zip_buffer.getvalue(), "ali_images.zip", "application/zip")

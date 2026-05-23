import os
from PIL import Image
def get_ali_images(img):
    img = img.convert("RGB")
    target_size = 1000
    square_img = Image.new("RGB", (target_size, target_size), (255, 255, 255))
    w, h = img.size
    ratio = min(target_size / w, target_size / h)
    new_w, new_h = int(w * ratio), int(h * ratio)
    img_resized = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
    offset = ((target_size - new_w) // 2, (target_size - new_h) // 2)
    square_img.paste(img_resized, offset)
    base_img = square_img
    results = []
    results.append(("1_main_white_bg.jpg", base_img))
    crop_size = int(target_size * 0.666)
    left = (target_size - crop_size) // 2
    top = (target_size - crop_size) // 2
    results.append(("2_center_detail.jpg", base_img.crop((left, top, left + crop_size, top + crop_size)).resize((target_size, target_size))))
    half = target_size // 2
    results.append(("3_top_left.jpg", base_img.crop((0, 0, half, half)).resize((target_size, target_size))))
    results.append(("4_top_right.jpg", base_img.crop((half, 0, target_size, half)).resize((target_size, target_size))))
    results.append(("5_bottom_left.jpg", base_img.crop((0, half, half, target_size)).resize((target_size, target_size))))
    results.append(("6_bottom_right.jpg", base_img.crop((half, half, target_size, target_size)).resize((target_size, target_size))))
    return results
def split_ali_grid(img):
    img = img.convert("RGB")
    width, height = img.size
    cell_w = width // 3
    cell_h = height // 2
    target_dim = 1000
    results = []
    for row in range(2):
        for col in range(3):
            left = col * cell_w
            top = row * cell_h
            right = (col + 1) * cell_w if col < 2 else width
            bottom = (row + 1) * cell_h if row < 1 else height
            cell = img.crop((left, top, right, bottom))
            w, h = cell.size
            ratio = min(target_dim / w, target_dim / h)
            new_w, new_h = int(w * ratio), int(h * ratio)
            cell_resized = cell.resize((new_w, new_h), Image.Resampling.LANCZOS)
            square_img = Image.new("RGB", (target_dim, target_dim), (255, 255, 255))
            offset = ((target_dim - new_w) // 2, (target_dim - new_h) // 2)
            square_img.paste(cell_resized, offset)
            index = row * 3 + col + 1
            results.append((f"ali_main_image_{index}.jpg", square_img))
    return results

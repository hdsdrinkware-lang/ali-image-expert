import os
from PIL import Image

def get_ali_images(img):
    img = img.convert("RGB")
    target_size = max(img.size[0], img.size[1], 1000)
    square_img = Image.new("RGB", (target_size, target_size), (255, 255, 255))
    offset = ((target_size - img.size[0]) // 2, (target_size - img.size[1]) // 2)
    square_img.paste(img, offset)
    base_img = square_img.resize((1000, 1000), Image.Resampling.LANCZOS)
    results = []
    results.append(("1_main_white_bg.jpg", base_img))
    crop_size = 666
    left = (1000 - crop_size) // 2
    top = (1000 - crop_size) // 2
    results.append(("2_center_detail.jpg", base_img.crop((left, top, left + crop_size, top + crop_size)).resize((1000, 1000))))
    results.append(("3_top_left.jpg", base_img.crop((0, 0, 500, 500)).resize((1000, 1000))))
    results.append(("4_top_right.jpg", base_img.crop((500, 0, 1000, 500)).resize((1000, 1000))))
    results.append(("5_bottom_left.jpg", base_img.crop((0, 500, 500, 1000)).resize((1000, 1000))))
    results.append(("6_bottom_right.jpg", base_img.crop((500, 500, 1000, 1000)).resize((1000, 1000))))
    return results

def split_ali_grid(img):
    img = img.convert("RGB")
    width, height = img.size
    cell_w = width // 3
    cell_h = height // 2
    results = []
    for row in range(2):
        for col in range(3):
            left = col * cell_w
            top = row * cell_h
            right = (col + 1) * cell_w if col < 2 else width
            bottom = (row + 1) * cell_h if row < 1 else height
            cell = img.crop((left, top, right, bottom))
            w, h = cell.size
            target_dim = max(w, h, 1000)
            square_img = Image.new("RGB", (target_dim, target_dim), (255, 255, 255))
            offset = ((target_dim - w) // 2, (target_dim - h) // 2)
            square_img.paste(cell, offset)
            final_img = square_img.resize((1000, 1000), Image.Resampling.LANCZOS)
            index = row * 3 + col + 1
            results.append((f"ali_main_image_{index}.jpg", final_img))
    return results

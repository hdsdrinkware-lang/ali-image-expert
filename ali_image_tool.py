from PIL import Image
def split_ali_grid(img, cols=3, rows=2):
    img = img.convert("RGB")
    width, height = img.size
    cell_w = width // cols
    cell_h = height // rows
    target_dim = 1000
    results = []
    for row in range(rows):
        for col in range(cols):
            left = col * cell_w
            top = row * cell_h
            right = (col + 1) * cell_w if col < (cols - 1) else width
            bottom = (row + 1) * cell_h if row < (rows - 1) else height
            cell = img.crop((left, top, right, bottom))
            w, h = cell.size
            ratio = min(target_dim / w, target_dim / h)
            new_w, new_h = int(w * ratio), int(h * ratio)
            cell_resized = cell.resize((new_w, new_h), Image.Resampling.LANCZOS)
            square_img = Image.new("RGB", (target_dim, target_dim), (255, 255, 255))
            offset = ((target_dim - new_w) // 2, (target_dim - new_h) // 2)
            square_img.paste(cell_resized, offset)
            index = row * cols + col + 1
            results.append((f"ali_image_{index}.jpg", square_img))
    return results

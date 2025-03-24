import pandas as pd

# Đọc file CSV
file_path = "./raw_data/data/rawdata.csv"  # Thay bằng đường dẫn file thực tế
df = pd.read_csv(file_path)

# Xáo trộn dữ liệu
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

# Lưu lại file đã xáo trộn
df.to_csv("./raw_data/data/sort_lable.csv", index=False)

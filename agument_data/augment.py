import random
import pandas as pd
import csv  # Thêm import csv để sử dụng QUOTE_NONE

# Danh sách từ khóa theo nhóm (không có dấu)
tuyen_dung = ["Tuyển gấp", "Việc nhẹ lương cao", "Không cần kinh nghiệm", "Làm việc tại nhà", "Lương hấp dẫn", 
              "Chuyển khoản trước", "Đặt cọc", "Phí đăng ký", "Thu nhập khủng", "Thu nhập cao", "Làm giàu không khó", "Không cần bằng cấp"]
dau_tu = ["Cam kết lợi nhuận", "Lãi suất hấp dẫn", "Chỉ cần đầu tư X triệu", "Tiền tự động sinh lời", 
          "Đầu tư không rủi ro", "Cơ hội vàng", "Chốt đơn nhanh"]
danh_bac = ["Chơi là thắng", "Game đổi thưởng", "App kiếm tiền nhanh", "Kiếm tiền nhanh chóng", "Tool auto thắng", 
            "Thu nhập X triệu/ngày", "Tham gia ngay để nhận thưởng"]
ho_tro_tai_chinh = ["Vay tiền nhanh", "Không cần thế chấp", "Giải ngân trong ngày", "Lãi suất 0%", 
                    "Chỉ cần CCCD", "Không cần giấy tờ", "Lãi suất thấp nhất thị trường", "Hỗ trợ vay tiền 24/7"]
ban_hang = ["Hàng xách tay giá rẻ", "Hàng chính hãng giảm giá sốc", "Nhận hoa hồng khủng", "Nhận ngay ưu đãi lớn", 
            "Hưởng lợi nhuận theo cấp số nhân"]
mao_danh = ["Tài khoản của bạn gặp vấn đề", "Bạn có một đơn hàng chưa nhận", "Công an đang điều tra tài khoản của bạn", 
            "Nhấp vào đường link để cập nhật thông tin", "Nhấp vào liên kết để xác minh tài khoản"]
ho_tro_quang_cao = ["Tư vấn miễn phí", "Cập nhật từ xa", "Hỗ trợ từ xa", "Đặt hàng ngay để nhận ưu đãi", "Khuyến mãi chỉ trong hôm nay"]

giao_duc = ["Học bổng khủng", "bán khóa học giá rẻ", "Cơ hội học tập quốc tế", "Học online miễn phí", "Học phí 0 đồng", "không cần bằng cấp", "không cần chứng chỉ"]

nha_tro = ["Đặt cọc trước", "thanh toán trước", "xem trọ online", "không tính tiền điện nước"]



# Từ đồng nghĩa để thay thế (không có dấu)
synonyms = {
    "Tuyển gấp": ["Cần tuyển khẩn cấp", "Tuyển dụng ngay", "Tìm người gấp","Cần tuyển ngay lập tức", "Tuyển dụng gấp rút"],
    "Lương hấp dẫn": ["Thu nhập cao", "Lương khủng", "Tiền lương siêu tốt", "Thu nhập khủng","Tiền lương hấp dẫn", "Thu nhập đáng mơ ước"],
    "Cam kết lợi nhuận": ["Đảm bảo lợi nhuận", "Lợi nhuận chắc chắn", "Hứa hẹn sinh lời","Lợi nhuận cao","Cam kết lợi nhuận cao"],
    "Vay tiền nhanh": ["Cho vay tức thì", "Hỗ trợ tài chính ngay", "Vay gấp","Giải ngân nhanh chóng","Vay tiền ngay lập tức"],
    "Chơi là thắng": ["Tham gia là có thưởng", "Chơi thắng lớn", "Chắc chắn trúng","Tham gia là thắng","Chơi game thắng tiền"],
    "làm việc tại nhà": ["Làm việc từ xa", "Công việc online", "Làm tại gia", "Không cần di chuyển","Làm việc tại nhà online"],

}   

# Cụm từ phụ trợ (không có dấu)
extra_phrases = ["Đừng bỏ lỡ cơ hội này", "Hàng trăm người đã thành công", "Nhanh tay để không bỏ lỡ", 
                 "Chỉ dành cho người quyết đoán", "Bạn sẽ bất ngờ với kết quả" ,"Cơ hội chỉ có trong thời gian ngắn",
                "Nhanh chóng hành động ngay hôm nay",
                "Đừng để cơ hội trôi qua",
                "Thời gian không chờ đợi ai",
                "Hãy quyết định ngay trước khi quá muộn",
                "Hàng ngàn người đã thành công",
                "Kết quả đã được chứng minh",
                "Được tin dùng bởi nhiều người",
                "Phương pháp đã giúp nhiều người thành công",
                "Bạn không cần phải lo lắng",
                "Bạn sẽ không tin vào kết quả",
                "Điều gì đang chờ đợi bạn?",
                "Khám phá bí mật thành công",
                "Bạn sẽ ngạc nhiên với những gì nhận được",
                ]

# Mẫu câu đa dạng (không có dấu)
templates = [
    "Đừng bỏ lỡ cơ hội {keyword1} với {keyword2} và {keyword3} {extra}"
    "Chỉ cần {keyword1} là bạn có thể {keyword2} và {keyword3} {extra}"
    "Khám phá {keyword1} và {keyword2} để nhận {keyword3} {extra}"
    "{keyword1} với {keyword2} {keyword3} {extra}",
    "Bạn đã nghe đến {keyword1} Chỉ cần {keyword2} là có {keyword3} {extra}",
    "{keyword1} {keyword2} để nhận ngay {keyword3} {extra}",
    "Hãy thử {keyword1} bạn sẽ thấy {keyword2} và {keyword3} ngay lập tức {extra}",
    "Với {keyword1} và {keyword2} {keyword3} đang chờ bạn {extra}",
    "Bắt đầu {keyword1} ngay hôm nay để {keyword2} và {keyword3} {extra}"
    "Thực hiện {keyword1} để đạt được {keyword2} và {keyword3} {extra}"
    "Hành động ngay với {keyword1} để nhận {keyword2} và {keyword3} {extra}"
    "Lợi ích của {keyword1} là {keyword2} và {keyword3} {extra}"
    "Tại sao nên chọn {keyword1}? Vì {keyword2} và {keyword3} {extra}"
    "Sự kết hợp hoàn hảo giữa {keyword1} và {keyword2} mang đến {keyword3} {extra}"
    "Khi {keyword1} gặp {keyword2}, bạn sẽ có {keyword3} {extra}"
]

groups = [tuyen_dung, dau_tu, danh_bac, ho_tro_tai_chinh, ban_hang, mao_danh, ho_tro_quang_cao, giao_duc, nha_tro]

# Hàm chọn từ đồng nghĩa
def get_synonym(keyword):
    return random.choice(synonyms.get(keyword, [keyword]))

# Hàm tạo bài viết ngẫu nhiên (không có dấu)
def generate_scam_post():
    selected_group = random.choice(groups)
    num_keywords = random.randint(2, 4)
    keywords = random.sample(selected_group, num_keywords)
    
    # Thay thế ngẫu nhiên bằng từ đồng nghĩa
    keywords = [get_synonym(kw) for kw in keywords]
    
    # Chọn mẫu câu ngẫu nhiên
    template = random.choice(templates)
    
    # Thêm cụm từ phụ trợ
    extra = random.choice(extra_phrases)
    
    # Tạo bài viết
    if len(keywords) >= 3:
        post = template.format(keyword1=keywords[0], keyword2=keywords[1], keyword3=keywords[2], extra=extra)
    else:
        post = " ".join(keywords) + f" {extra}"
    
    return post

data = []
for _ in range(1000):
    post = generate_scam_post()
    data.append({"text": post, "label": 1}) 

# Lưu vào file CSV không có dấu ngoặc kép
df = pd.DataFrame(data)
df.to_csv("new_scam_posts.csv", index=False, encoding="utf-8", quoting=csv.QUOTE_NONE, escapechar="\\")

print("Đã tạo và lưu 5000 bài viết lừa đảo không dấu vào file 'scam_posts_no_punctuation.csv'.")
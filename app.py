# Hseh  
import streamlit as st  
from google import genai  
from google.genai import types  # Nạp thêm thư viện cấu hình  
  
# KHÔNG DÁN KEY TRỰC TIẾP VÀO ĐÂY NỮA ĐỂ TRÁNH BỊ GOOGLE KHÓA
# Khởi tạo client nằm ngoài để tránh bị chạy lại liên tục
if "client" not in st.session_state:
    st.session_state.client = genai.Client() # <--- Để trống ngoặc, nó sẽ tự tìm trong Secrets của Streamlit  
  
st.set_page_config(  
    page_title="AI Thám tử lịch sử",  
    layout="wide"  
)  
  
# ẢNH BÌA (Đảm bảo bạn có file cover.jpg trong cùng thư mục)  
# st.image("cover.jpg") # Bỏ dấu # nếu bạn có file ảnh thật  
  
st.title("🕵️ AI THÁM TỬ LỊCH SỬ 1975")  
  
st.markdown("""  
## 📂 Hồ sơ số 1: Hành quân thần tốc  
  
Chào thám tử!  
  
Một hồ sơ mật năm 1975 vừa được tìm thấy.  
  
Theo tài liệu:  
  
> "Các đơn vị quân giải phóng đã di chuyển với tốc độ chưa từng có."  
  
Nhiệm vụ của em:  
  
🔍 Tìm hiểu bí mật của cuộc hành quân thần tốc.  
  
💬 Hãy trò chuyện với các nhân chứng lịch sử.  
""")  
  
# 1. KHỞI TẠO LỊCH SỬ CHAT TRÊN STREAMLIT  
if "messages" not in st.session_state:  
    st.session_state.messages = []  
  
# 2. KHỞI TẠO KHÔNG GIAN CHAT CỦA GEMINI VÀ CẤU HÌNH CHO AI NÓI DÀI  
if "gemini_chat" not in st.session_state:  
    # Viết luật cho AI tại đây, bắt AI trả lời chi tiết và dài hơn  
    system_instruction = """  
Bạn là AI Thám tử lịch sử.  
Bối cảnh: Chiến dịch Hồ Chí Minh năm 1975.  
  
Nhiệm vụ:  
- Nhập vai nhân chứng lịch sử một cách sống động.  
- Mỗi câu trả lời phải chi tiết, dài từ 6 đến 12 câu, không được trả lời quá ngắn.  
- Trả lời tự nhiên, kể chuyện hấp dẫn, mô tả rõ không khí hào hùng thời đó.  
- Không tiết lộ đáp án ngay lập tức.  
- Gợi ý bằng manh mối để học sinh tự tìm hiểu.  
- Dùng ngôn ngữ đơn giản, dễ hiểu cho học sinh lớp 5.  
"""  
      
    # Cấu hình max_output_tokens lên cao để AI không bị cắt lời giữa chừng  
    config = types.GenerateContentConfig(  
        max_output_tokens=1500,   
        temperature=0.7,  
        system_instruction=system_instruction  
    )  
      
    # Tạo phiên chat nhớ lịch sử truyện  
    st.session_state.gemini_chat = st.session_state.client.chats.create(  
        model="gemini-2.5-flash", # Cập nhật lên bản mô hình ổn định mới  
        config=config  
    )  
  
# Hiển thị lại các tin nhắn cũ trên màn hình  
for message in st.session_state.messages:  
    with st.chat_message(message["role"]):  
        st.write(message["content"])  
  
user_input = st.chat_input(  
    "Ví dụ: Có những manh mối nào?"  
)  
  
if user_input:  
    # Hiển thị câu hỏi của người dùng  
    st.session_state.messages.append({"role": "user", "content": user_input})  
    with st.chat_message("user"):  
        st.write(user_input)  
  
    try:  
        # Sử dụng send_message để Gemini tự động nhớ câu trước câu sau  
        response = st.session_state.gemini_chat.send_message(user_input)  
        answer = response.text  
  
    except Exception as e:  
        answer = f"❌ Lỗi Gemini: {e}"  
  
    # Hiển thị câu trả lời dài và chi tiết của AI  
    st.session_state.messages.append({"role": "assistant", "content": answer})  
    with st.chat_message("assistant"):  
        st.write(answer)  

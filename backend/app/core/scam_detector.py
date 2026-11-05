import re
from typing import Dict, Any, List

# High-risk recruitment scam patterns in Vietnam
SCAM_SIGNALS = [
    {
        "pattern": r"(?:cọc|đặt cọc|phí giữ chỗ|nộp phí|phí hồ sơ|phí đồng phục|mua tài liệu|nạp tiền|chuyển khoản trước)",
        "label": "Yêu cầu ứng viên nộp tiền hoặc đặt cọc trước (vi phạm quy định tuyển dụng)",
        "weight": 0.45
    },
    {
        "pattern": r"(?:nhiệm vụ telegram|nhiệm vụ shopee|nhiệm vụ tiktok|nhiệm vụ lazada|like dạo|xem video kiếm tiền|đánh giá hoa hồng|giật đơn|nhiệm vụ nạp tiền)",
        "label": "Mô hình làm nhiệm vụ qua ứng dụng mạng xã hội có dấu hiệu lừa đảo đa cấp / cờ bạc trá hình",
        "weight": 0.50
    },
    {
        "pattern": r"(?:việc nhẹ lương cao|không cần bằng cấp.*?lương\s*(?:30|40|50|60|70|80|90|100)\s*(?:tr|triệu)|1-2 tiếng.*?kiếm\s*(?:1|2|3|5)\s*(?:tr|triệu))",
        "label": "Hứa hẹn thu nhập cao bất thường không tương xứng với yêu cầu kinh nghiệm",
        "weight": 0.35
    },
    {
        "pattern": r"(?:đầu tư sinh lời|lãi suất ngày|lợi nhuận cam kết|đọc lệnh|đầu tư tài chính không rủi ro)",
        "label": "Dấu hiệu dụ dỗ tham gia sàn giao dịch tài chính / đầu tư bất hợp pháp",
        "weight": 0.45
    }
]


def analyze_job_scam_risk(title: str, description: str, requirements: str) -> Dict[str, Any]:
    """
    Evaluates recruitment text for fraud, phishing, or illegal fee extortion signals.
    Returns:
        - risk_score: 0.0 to 1.0
        - is_suspicious: bool (True if risk_score >= 0.40)
        - detected_signals: list of detected warning labels
        - advisory: advice for job moderation and candidate warning
    """
    full_text = f"{title or ''} {description or ''} {requirements or ''}".lower()
    detected_signals: List[str] = []
    total_score = 0.0

    for item in SCAM_SIGNALS:
        if re.search(item["pattern"], full_text, re.IGNORECASE):
            detected_signals.append(item["label"])
            total_score += item["weight"]

    risk_score = min(1.0, round(total_score, 2))
    is_suspicious = risk_score >= 0.40

    advisory = "Nội dung an toàn."
    if risk_score >= 0.70:
        advisory = "CẢNH BÁO CAO: Tin tuyển dụng có dấu hiệu lừa đảo chiếm đoạt tài sản rõ rệt. Đề xuất từ chối hoặc đình chỉ ngay lập tức."
    elif is_suspicious:
        advisory = "CHÚ Ý: Phát hiện một số dấu hiệu đáng ngờ. Cần kiểm duyệt thủ công trước khi phê duyệt."

    return {
        "risk_score": risk_score,
        "is_suspicious": is_suspicious,
        "detected_signals": detected_signals,
        "advisory": advisory
    }


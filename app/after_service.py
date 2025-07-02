import re
from typing import List, Tuple, Dict, Optional

def extract_ticket_code(text: str) -> Optional[str]:
    """
    Extracts the ticket code from the input text.
    Supports formats like: mã vé ABC123, vé xyz789, etc.
    """
    match = re.search(r"\b(?:mã vé|mã|vé)?[\s:\-]*([A-Z0-9]{5,})\b", text, re.IGNORECASE)
    return match.group(1) if match else None


def extract_time(text: str) -> Optional[str]:
    """
    Extracts time from the input text in formats like 18h, 18h30, 18:30, 9h, 7:00, etc.
    Returns time in HH:MM format if found, else None.
    """
    clean_text = text.lower()
    patterns = [
        r"\b([01]?\d|2[0-3])h(\d{1,2})\b",      # 18h30
        r"\b([01]?\d|2[0-3]):(\d{1,2})\b",      # 18:30
        r"\b([01]?\d|2[0-3])h\b",               # 18h → 18:00
        r"\b([01]?\d|2[0-3])\b"                 # 18 → 18:00 (fallback)
    ]
    for pattern in patterns:
        match = re.search(pattern, clean_text)
        if match:
            hour = match.group(1)
            minute = match.group(2) if len(match.groups()) > 1 else None
            if minute:
                return f"{hour}:{minute.zfill(2)}"
            return f"{hour}:00"
    return None


def handle_after_service(user_text: str, history: List[Dict[str, str]]) -> Tuple[str, List[Dict[str, str]]]:
    """
    Handles after-service requests (e.g., ticket time change) with simple multi-turn support.
    - Extracts ticket code and time from user input.
    - Stores info in history for multi-turn dialog.
    - Returns response and updated history.
    """
    ticket_code = extract_ticket_code(user_text)
    time_change = extract_time(user_text)

    if ticket_code:
        history.append({"type": "ticket", "value": ticket_code})
    if time_change:
        history.append({"type": "time", "value": time_change})

    ticket = next((h["value"] for h in reversed(history) if h["type"] == "ticket"), None)
    new_time = next((h["value"] for h in reversed(history) if h["type"] == "time"), None)

    if ticket and new_time:
        return f"✅ Đã đổi vé mã **{ticket}** sang giờ **{new_time}**. Cảm ơn bạn!", []
    if ticket and not new_time:
        return f"📌 Đã nhận mã vé **{ticket}**. Bạn muốn đổi sang giờ nào? (VD: 15h30)", history
    if new_time and not ticket:
        return f"🕒 Đã nhận giờ mới **{new_time}**. Vui lòng cung cấp mã vé cần đổi (VD: ABC123).", history
    return "🔄 Vui lòng cung cấp mã vé và giờ muốn đổi. Ví dụ: mã vé ABC123 đổi sang 15h30.", history

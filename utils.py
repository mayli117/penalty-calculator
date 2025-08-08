
import pdfplumber

DISCOUNT_TOTAL = {
    "自選餐(全選)": 2520,
    "自選餐(自選20)": 2352,
    "家庭特選餐": 3792,
    "家庭豪華餐": 4344
}

def extract_discount_code(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if "優惠代碼" in text:
                for line in text.split("\n"):
                    if "優惠代碼" in line:
                        return line.split("優惠代碼")[-1].strip().split()[0]
    return "未偵測到"

def calculate_penalty(plan, used_days):
    total_days = 730
    discount = DISCOUNT_TOTAL.get(plan, 0)
    return round(discount * used_days * (total_days - used_days) / (total_days ** 2))

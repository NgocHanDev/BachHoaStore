def format_currency(amount):
    formatted_amount = f"{amount // 10:,.0f}đ"
    return formatted_amount.replace(",", ".")

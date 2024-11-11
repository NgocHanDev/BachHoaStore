def format_currency(amount):
    formatted_amount = f"{amount:,.0f}đ"
    return formatted_amount.replace(",", ".")

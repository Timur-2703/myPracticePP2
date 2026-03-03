import re

with open("Practice5/raw.txt", "r", encoding="utf-8") as f:
    text = f.read()

products = re.findall(r'^\d+\.\s*\n(.+)$', text, flags=re.MULTILINE)

prices = re.findall(r'\d+(?:\s\d{3})*,\d{2}', text)

dt = re.search(r'Время:\s*(\d{2}\.\d{2}\.\d{4}\s+\d{2}:\d{2}:\d{2})', text)

total = re.search(r'ИТОГО:\s*\n([\d\s]+,\d{2})', text)

payment = "Банковская карта" if re.search(r'Банковская карта', text) else "Unknown"

print("Products:")
for p in products:
    print("-", p)

print("\nPayment:", payment)
print("DateTime:", dt.group(1) if dt else "Not found")
print("Total:", total.group(1) if total else "Not found")

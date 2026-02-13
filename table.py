import pandas as pd

# 1. Define the Header Information
header_info = {
    "Seller": "HEBEI SCIENCE WAX INDUSTRY CO., LTD.",
    "Buyer": "MEDIDIS",
    "P/I No.": "SCX-2025010401L",
    "Date": "Jan. 4th, 2025",
    "Address (Buyer)": "ATTN. MR./MS. EL FAIZ MOURAD",
    "Validity": "7 Days"
}

# 2. Define the Line Item Data
# Note: Item 12 includes the corrected values ($3.50 / $17.50)
data = [
    {"Item No": 1, "Product Name": "Soy Wax in Flakes", "Description": "Ingredients: 100% hydrogenated vegetable oil, MP 48-52°C", "Quantity": 500, "Unit": "KG", "Unit Price": 2.60, "Amount": 1300.00},
    {"Item No": 2, "Product Name": "58/60 Fully Refined Paraffin Wax", "Description": "White Granules, MP 58-60°C, Oil Content ≤0.5%", "Quantity": 1500, "Unit": "KG", "Unit Price": 1.72, "Amount": 2580.00},
    {"Item No": 3, "Product Name": "Wax Melter 1", "Description": "Color: Black, Vol: 8L, 1100W, EURO Standard", "Quantity": 4, "Unit": "PIECE", "Unit Price": 55.32, "Amount": 221.28},
    {"Item No": 4, "Product Name": "Wax Melter 2", "Description": "Color: Black, Vol: 6L, 1100W, EURO Standard", "Quantity": 2, "Unit": "PIECE", "Unit Price": 48.23, "Amount": 96.46},
    {"Item No": 5, "Product Name": "Electronic thermometer", "Description": "Range: -50°C to 300°C, Probe Length: 15cm", "Quantity": 3, "Unit": "PIECE", "Unit Price": 1.15, "Amount": 3.45},
    {"Item No": 6, "Product Name": "White Cotton Wicks", "Description": "Size: 18ply * 6cmL", "Quantity": 5000, "Unit": "PIECE", "Unit Price": 0.0058, "Amount": 29.00},
    {"Item No": 7, "Product Name": "White Cotton Wicks", "Description": "Size: 18ply * 12cmL", "Quantity": 10000, "Unit": "PIECE", "Unit Price": 0.0104, "Amount": 104.00},
    {"Item No": 8, "Product Name": "White Cotton Wicks", "Description": "Size: 24ply * 17cmL", "Quantity": 10000, "Unit": "PIECE", "Unit Price": 0.0124, "Amount": 124.00},
    {"Item No": 9, "Product Name": "White Cotton Wicks", "Description": "Size: 24ply * 20cmL", "Quantity": 5000, "Unit": "PIECE", "Unit Price": 0.0165, "Amount": 82.50},
    {"Item No": 10, "Product Name": "Metal Candle Wick Holder", "Description": "Material: Stainless steel, Size: 10cmL * 2.5cmW", "Quantity": 1000, "Unit": "PIECE", "Unit Price": 0.1120, "Amount": 112.00},
    {"Item No": 11, "Product Name": "Candle Wick Sticker", "Description": "Double-sided, Dia 20mm, Color: White", "Quantity": 1500, "Unit": "PIECE", "Unit Price": 0.0710, "Amount": 106.50},
    {"Item No": 12, "Product Name": "Wax Melting Cup", "Description": "Material: 304 Stainless steel, 550ml", "Quantity": 5, "Unit": "PIECE", "Unit Price": 3.50, "Amount": 17.50},
    {"Item No": 13, "Product Name": "Heat Gun", "Description": "Color: Black/White, 230V, 300W", "Quantity": 5, "Unit": "PIECE", "Unit Price": 6.00, "Amount": 30.00},
    {"Item No": 14, "Product Name": "Candle Dye Color Liquid", "Description": "32 different colors, 10ml/bottle", "Quantity": 160, "Unit": "BOTTLE", "Unit Price": 0.84, "Amount": 134.40},
    {"Item No": 15, "Product Name": "Fragrance Oil", "Description": "Scents: Ocean Gardenia", "Quantity": 10, "Unit": "KG", "Unit Price": 27.89, "Amount": 278.90},
    {"Item No": 16, "Product Name": "Fragrance Oil", "Description": "Scents: French Vanilla", "Quantity": 10, "Unit": "KG", "Unit Price": 19.20, "Amount": 192.00},
    {"Item No": 17, "Product Name": "Fragrance Oil", "Description": "Scents: Lavender", "Quantity": 10, "Unit": "KG", "Unit Price": 20.11, "Amount": 201.10},
    {"Item No": 18, "Product Name": "Fragrance Oil", "Description": "Scents: Rosemary", "Quantity": 10, "Unit": "KG", "Unit Price": 28.11, "Amount": 281.10},
    {"Item No": 19, "Product Name": "Fragrance Oil", "Description": "Scents: Amber Sandalwood", "Quantity": 10, "Unit": "KG", "Unit Price": 25.60, "Amount": 256.00},
    {"Item No": 20, "Product Name": "Fragrance Oil", "Description": "Scents: Citronella Oil", "Quantity": 10, "Unit": "KG", "Unit Price": 22.86, "Amount": 228.60},
    {"Item No": 21, "Product Name": "Fragrance Oil", "Description": "Scents: Jasmine Tea", "Quantity": 10, "Unit": "KG", "Unit Price": 25.60, "Amount": 256.00},
    {"Item No": 22, "Product Name": "Fragrance Oil", "Description": "Scents: Oud", "Quantity": 5, "Unit": "KG", "Unit Price": 39.72, "Amount": 198.60},
]

# Create DataFrame
df = pd.DataFrame(data)

# 3. Define Output File Name
file_name = "Proforma_Invoice_Data.xlsx"

# 4. Write to Excel with formatting
with pd.ExcelWriter(file_name, engine='xlsxwriter') as writer:
    # -- Write the DataFrame to the sheet starting at row 9 (leaving room for headers) --
    df.to_excel(writer, sheet_name='Invoice', startrow=9, index=False)
    
    # -- Get Workbook and Worksheet objects --
    workbook = writer.book
    worksheet = writer.sheets['Invoice']
    
    # -- Define Formats --
    bold_fmt = workbook.add_format({'bold': True})
    title_fmt = workbook.add_format({'bold': True, 'font_size': 14})
    currency_fmt = workbook.add_format({'num_format': '$#,##0.00'})
    currency_bold_fmt = workbook.add_format({'num_format': '$#,##0.00', 'bold': True, 'bg_color': '#FFFF00'})
    header_bg_fmt = workbook.add_format({'bold': True, 'bg_color': '#D3D3D3', 'border': 1})
    
    # -- Write Header Information (Manual Writing) --
    worksheet.write('A1', "PROFORMA INVOICE", title_fmt)
    
    worksheet.write('A3', "Seller:", bold_fmt)
    worksheet.write('B3', header_info["Seller"])
    
    worksheet.write('A4', "Buyer:", bold_fmt)
    worksheet.write('B4', header_info["Buyer"])
    worksheet.write('B5', header_info["Address (Buyer)"])
    
    worksheet.write('E3', "P/I No.:", bold_fmt)
    worksheet.write('F3', header_info["P/I No."])
    
    worksheet.write('E4', "Date:", bold_fmt)
    worksheet.write('F4', header_info["Date"])
    
    worksheet.write('E5', "Validity:", bold_fmt)
    worksheet.write('F5', header_info["Validity"])
    
    # -- Format the Table Columns --
    # Set column widths
    worksheet.set_column('A:A', 8)   # Item No
    worksheet.set_column('B:B', 30)  # Product Name
    worksheet.set_column('C:C', 45)  # Description
    worksheet.set_column('D:D', 10)  # Qty
    worksheet.set_column('E:E', 10)  # Unit
    worksheet.set_column('F:F', 12)  # Unit Price
    worksheet.set_column('G:G', 15)  # Amount

    # Apply currency format to Price and Amount columns (Data is in rows 10 to 10+len(data))
    for row_num in range(10, 10 + len(data)):
        worksheet.write_number(row_num, 5, data[row_num-10]['Unit Price'], currency_fmt)
        worksheet.write_number(row_num, 6, data[row_num-10]['Amount'], currency_fmt)

    # -- Calculate and Write Footer Totals --
    last_row = 10 + len(data)
    
    # Subtotal
    worksheet.write(last_row, 5, "Subtotal", bold_fmt)
    worksheet.write_formula(last_row, 6, f'=SUM(G11:G{last_row})', currency_bold_fmt)
    
    # Shipping
    worksheet.write(last_row + 1, 5, "Shipping Charges", bold_fmt)
    worksheet.write_number(last_row + 1, 6, 125.84, currency_fmt)
    
    # Total
    worksheet.write(last_row + 2, 5, "TOTAL AMOUNT", bold_fmt)
    worksheet.write_formula(last_row + 2, 6, f'=G{last_row+1}+G{last_row+2}', currency_bold_fmt)
    
    # -- Add Notes --
    note_row = last_row + 5
    worksheet.write(note_row, 0, "NOTES:", bold_fmt)
    worksheet.write(note_row + 1, 0, "1. Payment Terms: T/T 50% deposit, balance before loading.")
    worksheet.write(note_row + 2, 0, "2. Delivery Time: Within 30-40 days after receiving payment.")
    worksheet.write(note_row + 3, 0, "3. Shipping Terms: FCA Ningbo City, China")
    worksheet.write(note_row + 4, 0, "4. Handwritten Notes: HS Code 3404909099 | 'Groupage' | '21/01/25 Full cont.'")

print(f"Excel file '{file_name}' has been created successfully.")
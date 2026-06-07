"""
Author: Nitesh Devidas Dudhe
Purpose: PDF generation for billing exports.
"""
from fpdf import FPDF
from datetime import datetime

def generate_pdf(df, days, project_id):
    if df.empty:
        print("[!] No data to write to PDF.")
        return

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    
    # Header
    pdf.cell(200, 10, txt=f"GCP Billing Report - Last {days} Days", ln=True, align="C")
    pdf.set_font("Arial", "I", 10)
    pdf.cell(200, 10, txt=f"Project: {project_id} | Date: {datetime.now().strftime('%Y-%m-%d')}", ln=True, align="C")
    pdf.ln(10)
    
    # Table Header
    pdf.set_font("Arial", "B", 12)
    pdf.cell(90, 10, "Service Name", border=1)
    pdf.cell(50, 10, "Cost", border=1, align="C")
    pdf.cell(40, 10, "Currency", border=1, align="C")
    pdf.ln()
    
    # Table Data
    pdf.set_font("Arial", "", 11)
    total_cost = 0
    currency = ""
    
    for _, row in df.iterrows():
        # Truncate long service names
        service_name = (row['Service'][:25] + '..') if len(row['Service']) > 25 else row['Service']
        
        pdf.cell(90, 10, str(service_name), border=1)
        pdf.cell(50, 10, str(row['Cost']), border=1, align="C")
        pdf.cell(40, 10, str(row['Currency']), border=1, align="C")
        pdf.ln()
        
        total_cost += row['Cost']
        currency = row['Currency']
        
    # Total Footer
    pdf.set_font("Arial", "B", 12)
    pdf.cell(90, 10, "TOTAL", border=1)
    pdf.cell(50, 10, f"{round(total_cost, 2)}", border=1, align="C")
    pdf.cell(40, 10, currency, border=1, align="C")
    
    filename = f"billing_report_{project_id}_{days}_days.pdf"
    pdf.output(filename)
    print(f"\n[+] Success! Report saved as: {filename}")
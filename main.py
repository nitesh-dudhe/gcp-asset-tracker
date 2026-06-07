"""
Author: Nitesh Devidas Dudhe
Purpose: Interactive CLI Router for GCP Asset & Billing tracking.
"""
import sys
from core.asset_inventory import get_chargeable_services, display_and_suggest_deletion
from core.billing_export import get_billing_data
from core.pdf_report import generate_pdf

def main():
    print("""
    ================================================
          GCP ASSET & BILLING TRACKER (ZERO)
    ================================================
    """)
    project_id = input("Enter your GCP Project ID: ").strip()
    
    print("\nSelect an option:")
    print("1. Find all active services across all regions/zones")
    print("2. Export Active Billing data to PDF")
    print("3. Exit")
    
    choice = input("\nChoice (1/2/3): ").strip()
    
    if choice == '1':
        assets = get_chargeable_services(project_id)
        display_and_suggest_deletion(assets, project_id)
        
    elif choice == '2':
        print("[!!] Billing CODE is UNDER PROGRESS [!!]")
#        print("\n[!] Billing data export is not enabled by default.")
#        print("    Please enable it in the BigQuery console.")
#        print("    See: https://cloud.google.com/billing/docs/how-to/export-data-bigquery")
#        input("\n[!] Press Enter after enabling billing export...")
#        print("\nSelect timeframe:")
#        print("A. 7 Days")
#        print("B. 1 Month (30 Days)")
#        print("C. 3 Months (90 Days)")
        
#        time_choice = input("Choice (A/B/C): ").strip().upper()
#        days_map = {'A': 7, 'B': 30, 'C': 90}
        
#        if time_choice not in days_map:
#            print("Invalid choice.")
#            sys.exit(1)
            
#        days = days_map[time_choice]
        
#        print("\n[!] BigQuery details required (found in your BigQuery console):")
#        dataset_id = input("Enter BigQuery Dataset ID (e.g., billing_data): ").strip()
#        table_name = input("Enter Table Name (e.g., gcp_billing_export_v1_XXXX): ").strip()
        
#        df = get_billing_data(project_id, dataset_id, table_name, days)
#        generate_pdf(df, days, project_id)
        
    else:
        print("Exiting...")
        sys.exit(0)

if __name__ == "__main__":
    main()
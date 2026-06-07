"""
Author: Nitesh Devidas Dudhe
Purpose: BigQuery integration for dynamic billing reports.
"""
from google.cloud import bigquery
import pandas as pd

def get_billing_data(project_id, dataset_id, table_name, days):
    print(f"\n[*] Querying BigQuery for the last {days} days of billing data...")
    client = bigquery.Client(project=project_id)
    
    # Standard query for GCP BigQuery Billing Export
    query = f"""
        SELECT
            service.description as service_name,
            ROUND(SUM(cost), 2) as total_cost,
            currency
        FROM
            `{project_id}.{dataset_id}.{table_name}`
        WHERE
            _PARTITIONTIME >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL {days} DAY)
        GROUP BY
            service_name, currency
        ORDER BY
            total_cost DESC
    """
    
    try:
        query_job = client.query(query)
        results = query_job.result()
        
        data = []
        for row in results:
            data.append({"Service": row.service_name, "Cost": row.total_cost, "Currency": row.currency})
            
        return pd.DataFrame(data)
        
    except Exception as e:
        print(f"\n[!] BigQuery Error: {e}")
        print("[!] Ensure BigQuery Billing Export is enabled and your dataset/table names are correct.")
        return pd.DataFrame()
"""
Author: Nitesh Devidas Dudhe
Purpose: GCP Cloud Asset Inventory scanner.
"""
from google.cloud import asset_v1

def get_chargeable_services(project_id):
    print(f"\n[*] Scanning for HIGH-COST active services in: {project_id}...")
    client = asset_v1.AssetServiceClient()
    scope = f"projects/{project_id}"
    
    # These are the classic "Always On" services that cost money just by existing
    DANGER_ZONE_ASSETS = [
        "compute.googleapis.com/Instance",        # VMs
        "sqladmin.googleapis.com/Instance",       # Cloud SQL Databases
        "compute.googleapis.com/ForwardingRule",  # Load Balancers
        "compute.googleapis.com/Address",         # Reserved Static IPs
        "container.googleapis.com/Cluster",       # GKE Control Planes
        "redis.googleapis.com/Instance"           # Memorystore
    ]
    
    request = {"scope": scope, "asset_types": DANGER_ZONE_ASSETS} 
    active_assets = []
    
    try:
        response = client.search_all_resources(request=request)
        for resource in response:
            service_type = resource.asset_type.split('/')[-1]
            
            active_assets.append({
                "name": resource.display_name or resource.name.split('/')[-1],
                "type": service_type,
                "location": resource.location or "global"
            })
            
    except Exception as e:
        print(f"[!] Error accessing Asset Inventory: {e}")
        
    return active_assets

def display_and_suggest_deletion(assets, project_id):
    if not assets:
        print("No active assets found or permission denied.")
        return

    print("\n" + "="*80)
    print(f"{'SERVICE NAME':<30} | {'LOCATION':<15} | {'ASSET TYPE'}")
    print("="*80)
    
    for a in assets:
        print(f"{a['name'][:28]:<30} | {a['location']:<15} | {a['type']}")
        
    print("\n" + "="*80)
    print("### HOW TO DELETE THESE SERVICES VIA CONSOLE ###")
    print("1. Go to the unified Asset dashboard: https://console.cloud.google.com/assets/dashboard")
    print(f"2. Or search for the exact resource type by pasting this into the top search bar:")
    print("   Example: Search 'Compute Engine' to delete running VMs.")
    print("   Example: Search 'Cloud Storage' to empty and delete buckets.")
    print("="*80 + "\n")
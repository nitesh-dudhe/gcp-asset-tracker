1. **Asset Discovery:** Instead of iterating through regions, GCP has a centralized service called the **Cloud Asset Inventory API**. It acts as a global search engine for your project. A single API call will return all active services, tagging their specific region/zone automatically.
2. **Billing Data:** Unlike AWS Cost Explorer, GCP *does not* have a direct Python SDK to query granular historical costs out-of-the-box. The enterprise standard is to enable **Cloud Billing Export to BigQuery**. Our Python script will query this BigQuery dataset to generate the 7, 30, or 90-day cost reports.

Here is the complete, Git-ready architecture and code to build your `gcp-asset-billing-tracker`.

---

### **1. Repository Architecture**

Set up your local directory with this structure. It separates API logic from presentation, making it easy to integrate into a larger automation pipeline later.

```Tree Structure
gcp-asset-billing-tracker/
│
├── core/
│   ├── __init__.py
│   ├── asset_inventory.py   # Handles global resource discovery
│   ├── billing_export.py    # Queries BigQuery for cost data
│   └── pdf_report.py        # Generates the PDF exports
│
├── .gitignore
├── requirements.txt
├── README.md
└── main.py                  # The interactive CLI entrypoint
```
---

### Python version requirement







#### **1. Google Cloud SDK Installation**

We will use the [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) (`gcloud`) to handle authentication and API interactions.

**Linux (Debian/Ubuntu):**
```bash
export CLOUD_SDK_REPO="deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main"
```

**Note:** For other operating systems (macOS, Windows), please refer to the [official installation guide](https://cloud.google.com/sdk/docs/install).

---

#### **2. Authentication & Service Account Configuration**

Since you are operating from a Linux environment, we will use Application Default Credentials (ADC). Run the following command to log in with your user account:

```bash
gcloud auth application-default login
```

**For production or service-to-service authentication**, you should create a dedicated **Service Account** with the necessary IAM roles (see **Role Reference** below) and download the JSON key file:

```bash
gcloud iam service-accounts create tracker-service \
    --display-name "Asset Tracker Service"

gcloud projects add-iam-policy-binding [YOUR_PROJECT_ID] \
    --member="serviceAccount:[EMAIL_ADDRESS]" \
    --role="roles/cloudasset.viewer"

gcloud projects add-iam-policy-binding [YOUR_PROJECT_ID] \
    --member="serviceAccount:[EMAIL_ADDRESS]" \
    --role="roles/bigquery.user"

gcloud iam service-accounts keys create ./gcp-credentials.json \
    --iam-account=[EMAIL_ADDRESS]
```

**IMPORTANT:** If using the service account key file, set the environment variable `GOOGLE_APPLICATION_CREDENTIALS` before running the script:

```bash
export GOOGLE_APPLICATION_CREDENTIALS="./gcp-credentials.json"
```

---
### 2.1 Step-by-Step Execution Guide
Follow these commands to set up your environment and run the script.

**Create a Virtual Environment (Recommended):**
We will create a isolated environment to manage dependencies.

```bash
# 1. Create the environment named 'gcp-venv'
python3 -m venv gcp-venv

# 2. Activate the environment
source gcp-venv/bin/activate
```

> **Note:** Your terminal prompt will change (usually showing `(gcp-venv)`) to indicate the environment is active.

**Install Dependencies:**
With the environment active, install the required libraries using the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

**Run the Application:**
Execute the main Python script. It will automatically pick up your `gcloud` authentication.

```bash
python3 main.py
```

---


### GCP Cost Estimator
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GCP Simplified Cost Estimator</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; background-color: #f8f9fa; color: #202124; padding: 2rem; max-width: 800px; margin: 0 auto; }
        .card { background: white; border-radius: 8px; padding: 2rem; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        h2 { border-bottom: 2px solid #4285f4; padding-bottom: 0.5rem; }
        .control-group { margin-bottom: 1.5rem; display: flex; align-items: center; justify-content: space-between; }
        label { font-weight: 500; flex: 1; }
        .slider-container { flex: 2; display: flex; align-items: center; gap: 1rem; }
        input[type="range"] { flex: 1; }
        .value-display { width: 50px; text-align: right; font-family: monospace; font-size: 1.1rem; }
        .summary { margin-top: 2rem; padding: 1.5rem; background: #e8f0fe; border-radius: 8px; text-align: center; }
        .total-cost { font-size: 2.5rem; font-weight: bold; color: #1a73e8; margin: 0.5rem 0; }
        .high-cost { color: #d93025; font-weight: bold; }
    </style>
</head>
<body>

<div class="card">
    <h2>GCP Provisioned Services Estimator</h2>
    <p>Adjust the quantities below to see how provisioned, "Always On" services impact your monthly bill.</p>
    <div class="control-group">
        <label>Compute VMs (e2-standard-2) <br><small>$48/mo each</small></label>
        <div class="slider-container">
            <input type="range" id="vmSlider" min="0" max="20" value="0" oninput="calculateCost()">
            <div class="value-display" id="vmVal">0</div>
        </div>
    </div>
    <div class="control-group">
        <label>Cloud SQL Databases <br><small>$15/mo each</small></label>
        <div class="slider-container">
            <input type="range" id="sqlSlider" min="0" max="10" value="0" oninput="calculateCost()">
            <div class="value-display" id="sqlVal">0</div>
        </div>
    </div>
    <div class="control-group">
        <label>Load Balancers <br><small>$18/mo each</small></label>
        <div class="slider-container">
            <input type="range" id="lbSlider" min="0" max="10" value="0" oninput="calculateCost()">
            <div class="value-display" id="lbVal">0</div>
        </div>
    </div>
    <div class="control-group">
        <label>Reserved Static IPs <br><small>$3/mo each</small></label>
        <div class="slider-container">
            <input type="range" id="ipSlider" min="0" max="20" value="0" oninput="calculateCost()">
            <div class="value-display" id="ipVal">0</div>
        </div>
    </div>
    <div class="control-group">
        <label>Cloud Storage (TB) <br><small>$20/mo per TB</small></label>
        <div class="slider-container">
            <input type="range" id="storageSlider" min="0" max="50" value="0" oninput="calculateCost()">
            <div class="value-display" id="storageVal">0</div>
        </div>
    </div>
    <div class="summary">
        <h3>Estimated Monthly Cost</h3>
        <div class="total-cost">$<span id="totalDisplay">0</span></div>
        <div id="warningMessage"></div>
    </div>
</div>

<script>
    function calculateCost() {
        const vms = parseInt(document.getElementById('vmSlider').value);
        const sql = parseInt(document.getElementById('sqlSlider').value);
        const lb = parseInt(document.getElementById('lbSlider').value);
        const ips = parseInt(document.getElementById('ipSlider').value);
        const storage = parseInt(document.getElementById('storageSlider').value);

        // Update displays
        document.getElementById('vmVal').innerText = vms;
        document.getElementById('sqlVal').innerText = sql;
        document.getElementById('lbVal').innerText = lb;
        document.getElementById('ipVal').innerText = ips;
        document.getElementById('storageVal').innerText = storage;

        // Calculate
        const vmCost = vms * 48;
        const sqlCost = sql * 15;
        const lbCost = lb * 18;
        const ipCost = ips * 3;
        const storageCost = storage * 20;

        const total = vmCost + sqlCost + lbCost + ipCost + storageCost;
        document.getElementById('totalDisplay').innerText = total.toLocaleString();

        // High cost warning logic
        const warningEl = document.getElementById('warningMessage');
        if (vmCost > total * 0.5 && total > 0) {
            warningEl.innerHTML = "<span class='high-cost'>⚠️ Compute Engine is driving over 50% of your costs!</span>";
        } else if (storageCost > total * 0.5 && total > 0) {
            warningEl.innerHTML = "<span class='high-cost'>⚠️ Storage is driving over 50% of your costs! Check lifecycle policies.</span>";
        } else {
            warningEl.innerHTML = "";
        }
    }
</script>

</body>
</html>


### **Pre-Flight Execution Checklist**

Before you run this, you need to authenticate your local terminal with GCP. Instead of dropping an access key file like AWS, the modern GCP approach is to authenticate via your user identity or a service account:

1. **Install the GCP CLI:** If you haven't already, install `gcloud`.
2. **Authenticate:** Run `gcloud auth application-default login`. This creates a local JSON credential file that the Python libraries will automatically detect and use.
3. **Enable the APIs:** Ensure you have enabled the `Cloud Asset API` and `BigQuery API` in your GCP project console.

This structure is highly modular. Because the logic is cleanly separated, you can easily wire `main.py` to accept arguments via `argparse` instead of `input()` later down the line if you want to execute it headless via a CI/CD pipeline or orchestration engine.
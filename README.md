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

## 💰 GCP Provisioned Services Baseline Costs

Because provision-based resources incur charges 24/7 simply for existing (even with zero incoming traffic), use this quick baseline guide to estimate your monthly exposure before spinning up environments:

| Service Type | Specific Resource Component | Estimated Base Cost | Billing Metric |
| :--- | :--- | :--- | :--- |
| **Compute Engine** | `e2-standard-2` Virtual Machine | **$48.00 / month** | Per active instance |
| **Cloud SQL** | Standard Database Instance | **$15.00 / month** | Per provisioned instance |
| **Load Balancer** | External HTTP(S) Forwarding Rule | **$18.00 / month** | First 5 forwarding rules |
| **Cloud Storage** | Standard Storage Tier | **$20.00 / month** | Per Terabyte (TB) stored |
| **Network IPs** | Unused Reserved Static IP | **$3.65 / month** | Hourly penalty when unassigned |

> ⚠️ **The Cloud Learner Rule of Thumb:** > Always execute the script asset scanner (`python3 main.py`) before logging off for the day. A single forgotten Load Balancer or idle VM left running for a weekend can completely drain your free trial credits!

---

## 📊 GCP Provisioned Cost Estimator

Don't want to calculate costs by hand? Use our interactive cost calculator to simulate monthly GCP resource costs before writing your Terraform files.

<a href="https://nitesh-dudhe.github.io/devops-journey/gcp-interactive-cost-estimator.html" target="_self">
  <img src="https://img.shields.io/badge/GCP_Cost_Estimator-Interactive_App-4285F4?style=for-the-badge&logo=googlecloud&logoColor=white" alt="Launch Live Estimator">
</a>


---
### **Pre-Flight Execution Checklist**

Before you run this, you need to authenticate your local terminal with GCP. Instead of dropping an access key file like AWS, the modern GCP approach is to authenticate via your user identity or a service account:

1. **Install the GCP CLI:** If you haven't already, install `gcloud`.
2. **Authenticate:** Run `gcloud auth application-default login`. This creates a local JSON credential file that the Python libraries will automatically detect and use.
3. **Enable the APIs:** Ensure you have enabled the `Cloud Asset API` and `BigQuery API` in your GCP project console.

This structure is highly modular. Because the logic is cleanly separated, you can easily wire `main.py` to accept arguments via `argparse` instead of `input()` later down the line if you want to execute it headless via a CI/CD pipeline or orchestration engine.
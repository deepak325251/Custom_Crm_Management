# Custom CRM Management for Odoo 17

A custom module that enhances Odoo's CRM functionality with **stage change tracking** and **secure API access** using JSON-RPC.

---

## 🔧 Features

### 📌 CRM Stage History Tracking
- Tracks every stage change of a lead.
- Logs:
  - Lead ID
  - Previous Stage
  - New Stage
  - Changed By (User)
  - Changed On (DateTime)
- Automatically logs on stage change or lead creation.
- Accessible via a new menu under **CRM > Configuration > Stage History**.

### 📌 CRM Stage History Tracking via SQL view
- Accessible via a new menu under **CRM > Configuration > Lead Stage History**.

### 👥 Security & Access
- **Managers** can see all stage history.
- **Regular Users** can only see stage history for their own leads.
- Controlled via access rights and record rules.

### 🛠️ API Endpoints (JSON-RPC)
Secure API with **API Key Authentication** via HTTP headers. The API key is stored in **System Parameters** (`custom_crm.api_key`).

| Endpoint | Method | Description |
|---------|--------|-------------|
| `/api/crm/leads` | `GET`  | Returns all open leads |
| `/api/crm/create_lead` | `POST` | Creates a new lead |
| `/api/crm/lead_stage_history/<id>` | `GET`  | Returns stage change history for given lead |

---

## 🔐 API Authentication

All API requests must include an `Authorization` header:


---

## ✅ Installation

1. Copy the `custom_crm_management` module to your Odoo `addons` directory.
2. Install the module via the **Apps** menu.
3. Set the API key in **System Parameters**.
4. Test the endpoints using tools like Postman or `curl`.

---

### 📦 Dependencies
- pip install -r requirements.txt


## 🔄 API Usage

### 1. Get Open Leads
```bash
curl -X GET http://yourdomain.com/api/crm/leads \
-H "Authorization: your_api_key_here" \
-H "Content-Type: application/json" \
-d '{}'

curl -X POST http://yourdomain.com/api/crm/create_lead \
-H "Authorization: your_api_key_here" \
-H "Content-Type: application/json" \
-d '{
  "name": "New Opportunity",
  "email": "lead@example.com",
  "phone": "1234567890",
  "contact_name": "John Doe"
}'

curl -X GET http://yourdomain.com/api/crm/lead_stage_history/15 \
-H "Authorization: your_api_key_here" \
-H "Content-Type: application/json" \
-d '{}'

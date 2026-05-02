"""Build PrettySlack target URLs."""

import json

with open("fixtures/sample_workflow_state.json", "r", encoding="utf-8") as file:
    workflow_state = json.load(file)

slug = workflow_state["link"]["slug"]
base_target_url_prevalidate = workflow_state["link"]["base_target_url"]

if not base_target_url_prevalidate.endswith("/"):
    base_target_url_prevalidate += "/"

lowercase_base_target_url_prevalidate = base_target_url_prevalidate.lower()

if not lowercase_base_target_url_prevalidate.startswith("http://") and not lowercase_base_target_url_prevalidate.startswith("https://"):
    base_target_url = f"https://{base_target_url_prevalidate}"
else:    base_target_url = base_target_url_prevalidate

utm_source = workflow_state["payload"]["utm_source"]
utm_medium = workflow_state["payload"]["utm_medium"]
utm_campaign = workflow_state["payload"]["utm_campaign"]
utm_content = workflow_state["payload"]["utm_content"]
utm_term = "URL"

payload = f"?utm_source={utm_source}&utm_medium={utm_medium}&utm_campaign={utm_campaign}&utm_term={utm_term}&utm_content={utm_content}"

target_url = f"{base_target_url}{payload}"

print(target_url)
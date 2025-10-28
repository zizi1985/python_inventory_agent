from inventory_checker import get_low_stock_items
from email_utils import send_approval_request, send_email
from llm_agent import draft_purchase_order

def run_workflow():
    low_stock_items = get_low_stock_items()

    for item in low_stock_items:
        print(f"⚠️ Low stock detected for {item['sku']}")
        send_approval_request(item)

        approved = input(f"Approve reorder for {item['sku']}? (y/n): ").strip().lower() == "y"
        if approved:
            po = draft_purchase_order(item)
            send_email(item["supplier_email"], f"Purchase Order for {item['sku']}", po)
            print(f"✅ Order sent for {item['sku']}")
        else:
            print(f"❌ Order rejected for {item['sku']}")

from get_cumulative_total_rewards import send_signed_request

plan_id_to_name = {
    2202785: "DCA1",
    2202830: "DCA2",
    2985282: "DCA3",
    3068471: "DCA4",
    7228590: "DCA5"
}

# Generic function for making API requests
def make_api_request(session, url_path, payload={}):
    response = send_signed_request('GET', url_path, session, payload)

    if response.status_code == 200:
        return response.json()
    else:
        print("API request error:", response.status_code, response.json())
        return None

def get_plans_id(session):
    url_path = '/sapi/v1/lending/auto-invest/plan/list'
    response_data = make_api_request(session, url_path, {'size': 100})

    if response_data and 'plans' in response_data:
        return [plan['planId'] for plan in response_data['plans']]
    else:
        return []

def get_plan_details(plan_id, session):
    url_path = '/sapi/v1/lending/auto-invest/plan/id'
    response_data = make_api_request(session, url_path, {'size': 100, 'planId': plan_id})

    if response_data:
        return response_data
    else:
        return {}

def get_auto_invest_amount(session):
    plan_ids = get_plans_id(session)
    plans = []

    for plan_id in plan_ids:
        plan_details = get_plan_details(plan_id, session)
        plan = {"planId": plan_id_to_name.get(plan_id, plan_id), "details": []}
        for detail in plan_details.get("details", []):
            plan["details"].append({
                "targetAsset": detail["targetAsset"],
                "totalInvestedInUSD": detail["totalInvestedInUSD"],
                "purchasedAmount": detail["purchasedAmount"]
            })
        plans.append(plan)

    return plans
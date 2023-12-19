from get_cumulative_total_rewards import send_signed_request

plan_id_to_name = {
    2202785: "DCA1",
    2202830: "DCA2",
    2985282: "DCA3",
    3068471: "DCA4",
    7228590: "DCA5"
}

def get_plans_id():
    url_path = '/sapi/v1/lending/auto-invest/plan/list'
    response = send_signed_request('GET', url_path, {'size': 100})

    if response.status_code == 200 and 'plans' in response.json():
        return [plan['planId'] for plan in response.json()['plans']]
    else:
        print("Error in get_plans_id:", response.status_code, response.json())
        return []

def get_plan_details(plan_id):
    url_path = '/sapi/v1/lending/auto-invest/plan/id'
    response = send_signed_request('GET', url_path, {'size': 100, 'planId': plan_id})

    if response.status_code == 200:
        return response.json()
    else:
        print("Error in get_plan_details:", response.status_code, response.json())
        return {}

def get_auto_invest_amount():
    plan_ids = get_plans_id()
    plans = []

    for plan_id in plan_ids:
        plan_details = get_plan_details(plan_id)
        plan = {"planId": plan_id_to_name.get(plan_id, plan_id), "details": []}
        for detail in plan_details.get("details", []):
            plan["details"].append({
                "targetAsset": detail["targetAsset"],
                "totalInvestedInUSD": detail["totalInvestedInUSD"],
                "purchasedAmount": detail["purchasedAmount"]
            })
        plans.append(plan)

    return plans


get_auto_invest_amount()
from binance_api import make_api_request, send_signed_request



def get_plans_id(session, API_KEY, API_SECRET):
    url_path = '/sapi/v1/lending/auto-invest/plan/list'
    response_data = make_api_request(session, url_path, API_KEY, API_SECRET, {'size': 100})

    if response_data and 'plans' in response_data:
        return [plan['planId'] for plan in response_data['plans']]
    else:
        return []

def get_plan_details(plan_id, session, API_KEY, API_SECRET):
    url_path = '/sapi/v1/lending/auto-invest/plan/id'
    response_data = make_api_request(session, url_path, API_KEY, API_SECRET, {'size': 100, 'planId': plan_id})

    if response_data:
        return response_data
    else:
        return {}

def get_auto_invest_amount(session, API_KEY, API_SECRET, plan_id_to_name):
    plan_ids = get_plans_id(session, API_KEY, API_SECRET)
    plans = []
    for plan_id in plan_ids:
        plan_details = get_plan_details(plan_id, session, API_KEY, API_SECRET)
        plan = {"planId": plan_id_to_name[str(plan_id)], "details": []}

        for detail in plan_details.get("details", []):
            plan["details"].append({
                "targetAsset": detail["targetAsset"],
                "totalInvestedInUSD": detail["totalInvestedInUSD"],
                "purchasedAmount": detail["purchasedAmount"]
            })
        plans.append(plan)

    return plans

def get_cumulative_total_rewards(session, API_KEY, API_SECRET):
    url_path = '/sapi/v1/simple-earn/flexible/position'
    cumulative_rewards = {}
    current_page = 1
    has_more = True

    while has_more:
        payload = {
            'size': 100,  # Set size to maximum (100) as per Binance API specification
            'current': current_page,  # Page number, starting from 1
        }
        response = send_signed_request('GET', url_path, session, API_KEY, API_SECRET, payload)

        if response.status_code == 200:
            data = response.json()
            rows = data.get('rows', [])
            for row in rows:
                asset = row.get('asset')
                cumulative_rewards[asset] = row.get('cumulativeTotalRewards')
            # Check if there are more pages to fetch
            has_more = len(rows) == 100
            current_page += 1
        else:
            print("Error:", response.status_code)
            print(response.json())
            break

    return cumulative_rewards

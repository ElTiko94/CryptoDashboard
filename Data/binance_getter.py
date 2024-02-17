from binance_api import make_api_request



def get_plans_id(session, api_key, api_secret):
    url_path = '/sapi/v1/lending/auto-invest/plan/list'
    response_data = make_api_request(session, url_path, api_key, api_secret, {'size': 100})

    if response_data and 'plans' in response_data:
        return [plan['planId'] for plan in response_data['plans']]

    return []

def get_plan_details(plan_id, session, api_key, api_secret):
    url_path = '/sapi/v1/lending/auto-invest/plan/id'
    response_data = make_api_request(session, url_path, api_key, api_secret, {'size': 100, 'planId': plan_id})

    if response_data:
        return response_data

    return {}

def get_auto_invest(session, api_key, api_secret, plan_id_to_name):
    plan_ids = get_plans_id(session, api_key, api_secret)
    plans = []
    for plan_id in plan_ids:
        plan_details = get_plan_details(plan_id, session, api_key, api_secret)
        plan = {"planId": plan_id_to_name[str(plan_id)], "details": []}

        for detail in plan_details.get("details", []):
            plan["details"].append({
                "targetAsset": detail["targetAsset"],
                "totalInvestedInUSD": detail["totalInvestedInUSD"],
                "purchasedAmount": detail["purchasedAmount"]
            })
        plans.append(plan)

    return plans

def get_cumulative_total_rewards(session, api_key, api_secret):
    url_path = '/sapi/v1/simple-earn/flexible/position'
    cumulative_rewards = {}
    current_page = 1
    has_more = True

    while has_more:
        payload = {
            'size': 100,  # Set size to maximum (100) as per Binance API specification
            'current': current_page,  # Page number, starting from 1
        }

        data = make_api_request(session, url_path, api_key, api_secret, payload)

        if data is not None:
            rows = data.get('rows', [])
            for row in rows:
                asset = row.get('asset')
                cumulative_rewards[asset] = row.get('cumulativeTotalRewards')
            # Check if there are more pages to fetch
            has_more = len(rows) == 100
            current_page += 1
        else:
            print("Error:",data)
            break

    return cumulative_rewards

from database.models import User
from typing import List, Dict

def check_fast_start_bonus(users: List[User]) -> Dict[int, List[int]]:
    bonus_results = {}

    for user in users:
        qualified_referals = [
            ref for ref in user.referrals if any(
                purchase.package.name in ["1500", "3000"] for purchase in ref.purchases
            )
        ]
        
        if len(qualified_referals) < 2:
            continue

        for ref in qualified_referals:
            qualified_ref_referals = [
                ref_ref for ref_ref in ref.referrals if any(
                    purchase.package.name in ["1500", "3000"] for purchase in ref.purchases
                )
            ]

            if len(qualified_ref_referals) < 2:
                break

            if user.id not in bonus_results:
                bonus_results[user.id] = []
            bonus_results[user.id].append(ref.id)

        if bonus_results.get(user.id) and len(bonus_results[user.id]) < 2:
            del bonus_results[user.id]

    return bonus_results
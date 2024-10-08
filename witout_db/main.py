from datetime import datetime
from typing import List, Dict
from models import User, Package, Purchase

def calculate_fast_start_bonus(users: List[User]) -> Dict[int, List[int]]:
    bonus_results = {}

    for user in users:
        qualified_referals = [
            ref for ref in user.referrals if any(
                purchase.package_id in [1500, 3000] for purchase in ref.purchases
            )
        ]

        if len(qualified_referals) < 2:
            continue

        for ref in qualified_referals:
            qualified_ref_referals = [
                ref_ref for ref_ref in ref.referrals if any(
                    purchase.package_id in [1500, 3000] for purchase in ref_ref.purchases
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

if __name__ == "__main__":
    package_1500 = Package(id=1500, name="1500")
    package_3000 = Package(id=3000, name="3000")

    users = [
        User(id=1, referal_id=None, created_at=datetime.now(), referrals=[], purchases=[
            Purchase(id=1, user_id=1, package_id=1500, purchase_date=datetime.now())
        ]),
        User(id=2, referal_id=1, created_at=datetime.now(), referrals=[], purchases=[
            Purchase(id=2, user_id=2, package_id=3000, purchase_date=datetime.now())
        ]),
        User(id=3, referal_id=1, created_at=datetime.now(), referrals=[], purchases=[
            Purchase(id=3, user_id=3, package_id=1500, purchase_date=datetime.now())
        ]),
        User(id=4, referal_id=2, created_at=datetime.now(), referrals=[], purchases=[
            Purchase(id=4, user_id=4, package_id=3000, purchase_date=datetime.now())
        ]),
        User(id=5, referal_id=2, created_at=datetime.now(), referrals=[], purchases=[
            Purchase(id=5, user_id=5, package_id=1500, purchase_date=datetime.now())
        ]),
        User(id=6, referal_id=3, created_at=datetime.now(), referrals=[], purchases=[
            Purchase(id=6, user_id=6, package_id=1500, purchase_date=datetime.now())
        ]),
        User(id=7, referal_id=3, created_at=datetime.now(), referrals=[], purchases=[
            Purchase(id=7, user_id=7, package_id=1500, purchase_date=datetime.now())
        ]),
        User(id=8, referal_id=4, created_at=datetime.now(), referrals=[], purchases=[
            Purchase(id=8, user_id=8, package_id=3000, purchase_date=datetime.now())
        ])
    ]

    users[0].referrals = [users[1], users[2]]
    users[1].referrals = [users[3], users[4]]
    users[2].referrals = [users[5], users[6]]
    users[3].referrals = [users[7]]


    result = calculate_fast_start_bonus(users)
    for user_id, ref_ids in result.items():
        print(user_id, ref_ids)

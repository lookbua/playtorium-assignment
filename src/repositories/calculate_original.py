class OriginalValue:
    def __init__(self):
        pass

    def original_price(self, cart):
        original_price = 0
        category_price = {}

        for item in cart:
            try:
                amount = int(item['amount'])
                price = float(item['price'])
            except ValueError:
                print(f"Wrong input format: amount and price should be valid numbers for {item['name']} item")
                raise ValueError
            if amount < 0 or price < 0:
                print(f"Wrong input format: amount and price should be positive numbers for {item['name']} item")
                raise ValueError
            
            
            current_price = amount * price
            original_price += current_price

            category = item["category"]
            if category in category_price:
                category_price[category] += current_price
            else:
                category_price[category] = current_price

        category_price_list = [
            {category: price} for category, price in category_price.items()
        ]

        return original_price, category_price_list

    def original_campaign(self, campaign):
        # final campaign list => if it is the same type, eliminate the latter one that is included
        final_campaign = []
        added_categories = set()
        campaign_type_map = {
            "fixed amount": "coupon",
            "percentage discount": "coupon",
            "percentage discount by item category": "on top",
            "discount by points": "on top",
            "special campaigns": "seasonal",
        }

        for item in campaign:
            campaign_type = campaign_type_map.get(item["name"])
            if campaign_type and campaign_type not in added_categories:
                final_campaign.append(item)
                added_categories.add(campaign_type)
        return final_campaign

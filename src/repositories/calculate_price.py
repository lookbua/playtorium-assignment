class DiscountCalculation:
    def fixed_amount(self, amount, total_amount):
        return max(total_amount - amount, 0), amount

    def percentage_discount(self, percentage, total_amount):
        discount_amount = total_amount * (percentage) * 0.01
        return max(total_amount - discount_amount, 0), discount_amount

    def percentage_discount_by_item_category(self, amount, category, category_price):
        total_price = 0
        for price in category_price:
            if category.lower() in price.keys():
                price[f"{category}"] = max(
                    price[f"{category}"] * (100 - amount) * 0.01, 0
                )
            total_price += list(price.values())[0]
        return category_price, total_price

    def discount_by_points(self, points, total_amount):
        if points > total_amount * 0.2:
            points = int(total_amount * 0.2)
        return max(total_amount - points, 0), points

    def special_campaign(self, every: float, discount: float, total_amount: float):
        time = float(total_amount) // float(every)
        discount_amount = discount * time
        return max(total_amount - discount_amount, 0), discount_amount

    def update_category_price(self, category_price, discount_amount):
        total_value = sum(list(price.values())[0] for price in category_price)
        if total_value == 0:
            return category_price
        for price in category_price:
            key = list(price.keys())[0]
            proportion = price[key] / total_value
            price[key] = max(0, price[key] - discount_amount * proportion)
        return category_price

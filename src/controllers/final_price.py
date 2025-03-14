import json
from src.repositories.load_data import DataInput
from src.repositories.calculate_original import OriginalValue
from src.repositories.calculate_price import DiscountCalculation


class Price_controller:
    def __init__(
        self,
        data_input: DataInput,
        original_value: OriginalValue,
        discount_cal: DiscountCalculation,
    ):
        self.data_input = data_input
        self.original_value = original_value
        self.discount_cal = discount_cal

    def final_price(self):
        try:
            final_campaign, original_price, category_price = self.get_data()
            final_price = self.discount_value(
                final_campaign, original_price, category_price
            )
            if final_price == "Wrong input format":
                return final_price
            return (
                f"The final price is {final_price if final_price > 0 else 0:.2f} BAHT"
            )
        except Exception as e:
            return "There is an error in getting final price"

    def get_data(self):
        try:
            cart, campaign = self.data_input.load_input(self)
            original_price, category_price = self.original_value.original_price(
                self, cart
            )
            final_campaign = self.original_value.original_campaign(self, campaign)
            print(
                "\noriginal_price",
                original_price,
                "\ncategory_price",
                category_price,
                "\nfinal_campaign",
                final_campaign,
            )
            return final_campaign, original_price, category_price
        except Exception as e:
            print("There is an error in getting data")
            raise e

    def discount_value(self, final_campaign, price, category_price):
        try:
            parameters = self.get_valid_parameters(final_campaign)
            if parameters == "Wrong input format":
                return parameters
            print("parameters", parameters)

            for campaign in final_campaign:
                print("\n\ncampaign: ", campaign["name"], campaign["parameter"])

                amount_fixed = parameters.get("amount_fixed", 0)
                amount_item = parameters.get("amount_item", 0)
                percentage = parameters.get("percentage", 0)
                points = parameters.get("points", 0)
                every = parameters.get("every", 0)
                discount = parameters.get("discount", 0)

                if campaign["name"] == "fixed amount":
                    price = self.discount_cal.fixed_amount(
                        self, amount=amount_fixed, total_amount=price
                    )
                    category_price = self.discount_cal.update_category_price(
                        self, category_price=category_price, discount_amount=amount_fixed
                    )
                    print("price", price, "category_price", category_price)

                elif campaign["name"] == "percentage discount":
                    price, discount_amount = self.discount_cal.percentage_discount(
                        self,
                        percentage=percentage,
                        total_amount=price,
                    )
                    category_price = self.discount_cal.update_category_price(
                        self, category_price=category_price, discount_amount=discount_amount
                    )
                    print("price", price, "category_price", category_price)

                if campaign["name"] == "percentage discount by item category":
                    category_price, price = (
                        self.discount_cal.percentage_discount_by_item_category(
                            self,
                            amount=amount_item,
                            category=campaign.get("parameter", {}).get("category").lower(),
                            category_price=category_price,
                        )
                    )
                    print("price", price, "category_price", category_price)
                elif campaign["name"] == "discount by points":
                    price, discount_amount = self.discount_cal.discount_by_points(
                        self,
                        points=points,
                        total_amount=price,
                    )
                    category_price = self.discount_cal.update_category_price(
                        self, category_price=category_price, discount_amount=discount_amount
                    )
                    print("price", price, "category_price", category_price)

                if campaign["name"] == "special campaigns":
                    price, discount_amount = self.discount_cal.special_campaign(
                        self,
                        every=every,
                        discount=discount,
                        total_amount=price,
                    )
                    category_price = self.discount_cal.update_category_price(
                        self, category_price=category_price, discount_amount=discount_amount
                    )
                    print("price", price, "category_price", category_price)

            return price
        except Exception as e:
            print("There is an error in getting discount value")
            raise e

    def get_valid_parameters(self, final_campaign):
        highest_values = {
            "amount_fixed": float("-inf"),
            "amount_item": float("-inf"),
            "percentage": float("-inf"),
            "points": float("-inf"),
            "every": float("-inf"),
            "discount": float("-inf"),
        }

        for campaign in final_campaign:
            amount_fixed = campaign.get("parameter", {}).get("amount", 0) if campaign["name"] == "fixed amount" else 0
            amount_item = campaign.get("parameter", {}).get("amount", 0) if campaign["name"] == "percentage discount by item category" else 0
            percentage = campaign.get("parameter", {}).get("percentage", 0)
            points = campaign.get("parameter", {}).get("points", 0)
            every = campaign.get("parameter", {}).get("every", 0)
            discount = campaign.get("parameter", {}).get("discount", 0)

            parameters = {
                "amount_fixed": amount_fixed,
                "amount_item": amount_item,
                "percentage": percentage,
                "points": points,
                "every": every,
                "discount": discount,
            }

            # Validate each parameter and update the highest value
            for param, value in parameters.items():
                try:
                    value = float(value)
                except ValueError:
                    print(f"Wrong input format: {param} parameter should be a valid number")
                    raise ValueError("Wrong input format")
                if value < 0:
                    print(f"Wrong input format: {param} should be a positive number")
                    raise ValueError("Wrong input format")
                
                if value > highest_values[param]:
                    highest_values[param] = value
            
            if highest_values['discount'] > highest_values['every']:
                    print(f"Wrong input format: discount should be less than interval itself")
                    raise ValueError("Wrong input format")

        return highest_values

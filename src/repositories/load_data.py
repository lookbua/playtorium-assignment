import json


class DataInput:
    def __init__(self):
        pass

    def load_input(self):
        try:
            with open("input.json", "r") as file:
                data = json.load(file)
            print("data", data, type(data))
            cart = data.get("shopping_cart")
            print("cart", cart)
            cart = [
                {
                    key: value.lower() if isinstance(value, str) else value
                    for key, value in d.items()
                }
                for d in cart
            ]

            campaign = data.get("discount campaigns")
            campaign = [
                {
                    key: value.lower() if isinstance(value, str) else value
                    for key, value in d.items()
                }
                for d in campaign
            ]

            return cart, campaign
        except Exception as e:
            print(f"There is an error in loading input file: {e}")
            raise e

import json
from src.controllers.final_price import Price_controller
from src.repositories.load_data import DataInput
from src.repositories.calculate_original import OriginalValue
from src.repositories.calculate_price import DiscountCalculation

data_input = DataInput()
original_value = OriginalValue()
discount_cal = DiscountCalculation()
price_controller = Price_controller(data_input, original_value, discount_cal)

def calculating():
    return price_controller.final_price()

if __name__ == "__main__":
    result = calculating()
    print(result)  
    





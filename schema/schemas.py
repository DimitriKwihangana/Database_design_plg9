def individual_serial (water)-> dict:

    return{
        "id":str(water["_id"]),
         "potability": (water["potability"]),
         "ph":(water["ph"]),
         "chloramines":(water["chloramines"]),
         "sulfate":(water["sulfate"]),
         "conductivity":(water["conductivity"]),
         "organic_carbon":(water["organic_carbon"]),
         "trihalomethanes":(water["trihalomethanes"]),
         "hardness":(water["hardness"]),
         "solids":(water["solids"]),
         "turbidity":(water["turbidity"])
 
    }

def list_serial (waters) -> list:
    return[individual_serial(water) for water in waters]
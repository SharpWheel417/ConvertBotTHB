
### BAT TO RUB ###
def get_bath_to_rub(bath, c_thb, c_rub):
    mc_thb = round(c_thb,2)
    mc_rub = round(c_rub,2)
    return round((bath/round(mc_thb,2))*round(mc_rub,2),2) 

def get_bath_to_rub_marje(bath, c_thb, c_rub, marje):
    mc_thb = round(c_thb*(2-marje),2)
    mc_rub = round(c_rub,2)*marje
    return round((bath/round(mc_thb,2))*round(mc_rub,2),2) 

### BAT TO USDT ###
def get_bath_to_usdt(bath, c_thb):
    mc_thb = round(c_thb ,2)
    return round(bath/mc_thb, 2)

def get_bath_to_usdt_marje(bath, c_thb, marje):
    mc_thb = round(c_thb*(2-marje),2)
    return round(bath/mc_thb, 2)


### RUB TO BAT ###
def get_bath_to_usdt(rub, c_thb):
    mc_thb = round(c_thb ,2)
    return round(bath/mc_thb, 2)

def get_bath_to_usdt_marje(bath, c_thb, marje):
    mc_thb = round(c_thb*(2-marje),2)
    return round(bath/mc_thb, 2)


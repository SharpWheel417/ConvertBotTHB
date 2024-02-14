
### BAT TO RUB ###
def get_bath_to_rub(bath, c_rub, c_thb):
    mc_thb = round(c_thb,2)
    mc_rub = round(c_rub,2)
    return f"Курс баты: {mc_thb}\nКурс рубля: {mc_rub}\n{round((bath/round(mc_thb,2))*round(mc_rub,2),2)}" 

def get_bath_to_rub_marje(bath, c_rub, c_thb, marje):
    mc_thb = round(c_thb*(2-marje),2)
    mc_rub = round(c_rub,2)*marje
    return f"Курс баты: {mc_thb}\nКурс рубля: {mc_rub}\n{round((bath/round(mc_thb,2))*round(mc_rub,2),2)}"

### BAT TO USDT ###
def get_bath_to_usdt(bath, c_thb):
    mc_thb = round(c_thb ,2)
    return f"Курс баты: {mc_thb}\n{round(bath/mc_thb, 2)}"

def get_bath_to_usdt_marje(bath, c_thb, marje):
    mc_thb = round(c_thb*(2-marje),2)
    return f"Курс баты: {mc_thb}\n{round(bath/mc_thb, 2)}"


### RUB TO BAT ###
def get_rub_to_bat(rub, c_thb, c_rub):
    mc_thb = round(c_thb ,2)
    mc_rub = round(c_rub ,2)
    return f"Курс баты: {mc_thb}\nКурс рубля: {mc_rub}\n{round(rub/(mc_rub/mc_thb),2)}"

def get_rub_to_bat_marje(rub, c_thb, c_rub, marje):
    #c_thb = 35.2
    #c_rub = 91.2
    #mc_thb = 33.44
    #
    mc_thb = round(c_thb*(2-marje),2)
    mc_rub = round(c_rub ,2)*marje
    return f"Курс баты: {mc_thb}\nКурс рубля: {mc_rub}\n{round(rub/(mc_rub/mc_thb),2)}"

def get_rub_to_usdt(rub, c_rub):
    mc_rub = round(c_rub ,2)
    return f"Курс рубля: {mc_rub} \n{round(rub/mc_rub, 2)}"

def get_rub_to_usdt_marje(rub, c_rub, marje):
    mc_rub = round(c_rub ,2)*marje
    return f"Курс рубля: {mc_rub}\n{round(rub/mc_rub, 2)}"

def get_usdt_to_bat(usdt, c_thb):
    mc_thb = round(c_thb ,2)
    return f"Курс баты: {mc_thb}\n{round(usdt*mc_thb, 2)}"

def get_usdt_to_bat_marje(usdt, c_thb, marje):
    mc_thb = round(c_thb*(2-marje),2)
    return f"Курс баты: {mc_thb}\n{round(usdt*mc_thb, 2)}"

def get_usdt_to_rub(usdt, c_rub):
    mc_rub = round(c_rub ,2)
    return f"Курс рубля: {mc_rub}\n{round(usdt*mc_rub, 2)}"

def get_usdt_to_rub_marje(usdt, c_rub, marje):
    mc_rub = round(c_rub ,2)*marje
    return f"Курс рубля: {mc_rub}\n{round(usdt*mc_rub, 2)}"


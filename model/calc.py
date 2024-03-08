import database.course as c
### BAT TO RUB ###
def get_bath_to_rub(bath):
    return f"Курс баты: {c.get('thb')}\nКурс рубля: {c.get('rub')}\n{round((bath/round(c.get('thb'),2))*round(c.get('rub'),2),2)}" 

def get_bath_to_rub_marje(bath:float, marje:float):
    mc_thb = round(c.get('thb')*(2-marje),2)
    mc_rub = round(c.get('rub'),2)*marje
    return f"Курс баты: {mc_thb}\nКурс рубля: {mc_rub}\n{round((bath/round(mc_thb,2))*round(mc_rub,2),2)}"

### BAT TO USDT ###
def get_bath_to_usdt(bath: float):
    return f"Курс баты: {c.get('thb')}\n{round(bath/c.get('thb'), 2)}"

def get_bath_to_usdt_marje(bath:float, marje:float):
    mc_thb = round(c.get('thb')*(2-marje),2)
    return f"Курс баты: {mc_thb}\n{round(bath/mc_thb, 2)}"


### RUB TO BAT ###
def get_rub_to_bat(rub):
    return f"Курс баты: {c.get('thb')}\nКурс рубля: {c.get('rub')}\n{round(rub/(c.get('rub')/c.get('thb')),2)}"

def get_rub_to_bat_marje(rub, marje):
    mc_thb = round(c.get('thb')*(2-marje),2)
    mc_rub = round(c.get('rub') ,2)*marje
    return f"Курс баты: {mc_thb}\nКурс рубля: {mc_rub}\n{round(rub/(mc_rub/mc_thb),2)}"

def get_rub_to_usdt(rub):
    return f"Курс рубля: {c.get('rub')} \n{round(rub/c.get('rub'), 2)}"

def get_rub_to_usdt_marje(rub, marje):
    mc_rub = round(c.get('rub') ,2)*marje
    return f"Курс рубля: {mc_rub}\n{round(rub/mc_rub, 2)}"

def get_usdt_to_bat(usdt):
    return f"Курс баты: {c.get('thb')}\n{round(usdt*c.get('thb'), 2)}"

def get_usdt_to_bat_marje(usdt, marje):
    mc_thb = round(c.get('thb')*(2-marje),2)
    return f"Курс баты: {mc_thb}\n{round(usdt*mc_thb, 2)}"

def get_usdt_to_rub(usdt):
    return f"Курс рубля: {c.get('rub')}\n{round(usdt*c.get('rub'), 2)}"

def get_usdt_to_rub_marje(usdt, marje):
    mc_rub = round(c.get('rub') ,2)*marje
    return f"Курс рубля: {mc_rub}\n{round(usdt*mc_rub, 2)}"


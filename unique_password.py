import random
import array
import pandas as pd  
import numpy as np
import generate_password as gp
from  check_duplicate import duplicated, sum

df = pd.DataFrame()


def websites(website):
    """
    Ziyaret edilen web sitelerini tanımlar

    Returns:
        list: Ziyaret edilen websitesi listesi
    """
    password = unique_passwords()


def unique_passwords(websites):
    """
    Benzersiz bir şifre oluşturma
    """
    global df
    password_list = []

    for website in websites:
        password = gp.generate_password()
        while password in password_list:
            password = gp.generate_password()
        password_list.append(password)
        data = {"Website":website, "Password":password}
        df = df.append(data, ignore_index=True)
    return df


website_list = []

for i in range(10000):
    website_list.append("Website_" + str(i))

passwords10000df = unique_passwords(website_list)
    
print("SUM: ", sum(duplicated(passwords10000df['Password'])))


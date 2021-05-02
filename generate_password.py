import random
import array


def generate_password():
    numbers = ['0', '1', '2', '3', '4', '5'] 
    chars = ["A", "B", "C", "D", "E"]
    temp_passs = ""
    temp_pass = ""

    for i in range(4):
        rand_num = random.choice(numbers)
        temp_pass += temp_pass.join(rand_num)
        # rand_chars = random.choice(chars)
    for i in range(4):
        rand_chars = random.choice(chars)
        temp_passs += temp_passs.join(rand_chars)
    return(temp_pass + "-" + temp_passs)

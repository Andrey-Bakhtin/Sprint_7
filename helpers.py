from faker import Faker

faker = Faker('ru_RU')

def generate_courier_body():
    return {
        "firstName": faker.first_name(),
        "login": faker.user_name(),
        "password": faker.password()
    }

def generate_random_login_password():
    return {
        "login": faker.user_name(),
        "password": faker.password()
    }

def generate_order_data(color):
    street = faker.street_name()      
    house = faker.random_int(1, 999)

    if color is None or (isinstance(color, list) and not color):
        color_value = []
    else:
        color_value = color
    return {
        
        "firstName": faker.first_name(),
        "lastName": faker.last_name(),
        "address": f"{street}, {house}",
        "metroStation": faker.random_int(1, 10),
        "phone": '+7' + faker.numerify('###########'),
        "rentTime": faker.random_int(1, 10),
        "deliveryDate": faker.future_datetime(end_date="+10d").isoformat(),
        "comment": faker.text(max_nb_chars=10),
        "color": color_value
    }

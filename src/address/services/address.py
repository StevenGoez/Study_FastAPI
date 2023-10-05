address_id_counter = 0

# Función para obtener el próximo address_id
def get_next_address_id():
    global address_id_counter
    address_id_counter += 1
    return address_id_counter





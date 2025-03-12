import pandas as pd
import random
import csv
import faker
import datetime

# Initialisation
locale = "en_US" ####>>  en_GB (English - Great Britain) // fr_FR (French) // en_US (English - United States)
num_contacts = 10000 # nombre de contacts à générer
nb_cases=5000 # nombre de cases à générer
client_prefix = "LV" ####>> pour préfix les ID des contacts
countries = [
    "France", "UK", "Switzerland", "Germany", "US"
]
product_catalog = [
    {"id": "p001", "name": "Sac Capucines", "category": "bag", "price": 410},
    {"id": "p002", "name": "Montre Tambour", "category": "watch", "price": 7015},
    {"id": "p003", "name": "Porte-monnaie Zippy", "category": "accessory", "price": 6500},
    {"id": "p004", "name": "Ceinture Initiales", "category": "accessory", "price": 485},
    {"id": "p005", "name": "Sneakers LV Trainer", "category": "shoes", "price": 1020},
    {"id": "p006", "name": "Lunettes de soleil Millionaire", "category": "accessory", "price": 650},
    {"id": "p007", "name": "Bracelet Keep It", "category": "accessory", "price": 220},
    {"id": "p008", "name": "Sac Keepall", "category": "bag", "price": 540},
    {"id": "p009", "name": "Sac Noé", "category": "bag", "price": 1700},
    {"id": "p010", "name": "Valise Horizon", "category": "bag", "price": 2800}
]

# creation des data 
test_data = faker.Faker(locale)

# génération d'une date d'achat dans les 3 dernières années
def random_date():
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=3*365)  # 3 years ago
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + datetime.timedelta(days=random_number_of_days)
    return random_date 


contacts = []
for i in range(num_contacts):
    contacts.append({
        "contactid": client_prefix + str(i),
        "firstname": test_data.first_name(),
        "lastname": test_data.last_name(),
        "email": test_data.email(),
        "country": random.choice(countries),
        "age": random.randint(18, 84),
        "hasMobileApp": random.choices([True, False], weights=[0.4, 0.6])[0],
        "emailOptin": random.choices([True, False], weights=[0.78, 0.22])[0],
        "RFM": random.choices([1, 2, 3, 4, 5, 6, 7, 8, 9], weights=[0.02, 0.06, 0.16, 0.19, 0.22, 0.15, 0.09, 0.08, 0.03])[0]
        "Segment": random.choices(["VIC", "Regular", "1-timer", "Inactive"], weights=[0.05, 0.6, 0.1, 0.25])[0]
    })

# Génération des tickets (cases)
case_categories = ["order issue", "product issue", "general question"] # catégorie des cases
cases = []
for i in range(1, nb_cases + 1):
    contact_id = client_prefix + str(random.randint(1, num_contacts))
    creation_date =  random_date()  # 3 dernières années
    status = "closed" if random.random() < 0.75 else "open" # statut des tickets, 75% closed
    end_date = (creation_date + datetime.timedelta(days=random.randint(1, 60))).strftime("%Y-%m-%d") if status == "closed" else ""
    case_category = random.choice(case_categories)
    strcreation_date = creation_date.strftime("%Y-%m-%d")
    cases.append([f"case{i}", contact_id, strcreation_date, status, end_date, case_category])

df_cases = pd.DataFrame(cases, columns=["CaseID", "ContactID", "CreationDate", "Status", "EndDate", "CaseCategory"])


# Generate orders and order lines (modified)
orders = []
order_lines = []
order_id_counter = 1
line_id_counter = 1

for contact in contacts:
    num_orders = random.randint(0, 5) #entre 0 et 4 commandes par contact
    for _ in range(num_orders):
        order_date = random_date()
        order_id = f"order{order_id_counter}"  # Format order ID
        orders.append({
            "orderid": order_id,  # Store the formatted ID
            "order_date": order_date,
            "contactid": contact["contactid"],
            "total_price": 0
        })

        num_lines = random.randint(1, 4)
        added_products = set()
        order_total_price = 0

        for _ in range(num_lines):
            while True:
                product = random.choice(product_catalog)
                if product["id"] not in added_products:
                    added_products.add(product["id"])
                    break

            quantity = random.randint(1, 3) #nombre de produits max par ligne 
            line_price = product["price"] * quantity
            order_total_price += line_price

            line_id = f"L{line_id_counter}"  # Format line ID
            order_lines.append({
                "lineID": line_id,  # Store the formatted ID
                "orderid": order_id,  # Use the formatted order ID
                "productid": product["id"],
                "quantity": quantity
            })
            line_id_counter += 1

        # Mise à jour du montant total de la commande
        for order in orders:
            if order["orderid"] == order_id: # Use the formatted order ID
                order["total_price"] = order_total_price
                break

        order_id_counter += 1

# Function to save data to CSV
def save_to_csv(data, filename, fieldnames):
    df = pd.DataFrame(data, columns=fieldnames)
    df.to_csv(filename, index=False, encoding="utf-8")

# Création des fichiers
save_to_csv(contacts, "contacts.csv", ["contactid", "firstname", "lastname", "email", "country", "age", "hasMobileApp", "emailOptin", "RFM","Segment"])
save_to_csv(product_catalog, "products.csv", ["id", "name", "category", "price"])
save_to_csv(orders, "orders.csv", ["orderid", "order_date", "contactid", "total_price"])
save_to_csv(order_lines, "order_lines.csv", ["lineID", "orderid", "productid", "quantity"])
df_cases.to_csv("cases.csv", index=False, encoding="utf-8")

print("CSV files generated successfully!")



'''
LISTE DES DONNEES POUVANT ETRE GENEREES PAR FAKER

address
 administrative_unit
 am_pm
 android_platform_token
 ascii_company_email
 ascii_email
 ascii_free_email
 ascii_safe_email
 bank_country
 basic_phone_number
 bban
 binary
 boolean
 bothify
 bs
 building_number
 cache_pattern
 catch_phrase
 century
 chrome
 city
 city_prefix
 city_suffix
 color
 color_hsl
 color_hsv
 color_name
 color_rgb
 color_rgb_float
 company
 company_email
 company_suffix
 coordinate
 country
 country_calling_code
 country_code
 credit_card_expire
 credit_card_full
 credit_card_number
 credit_card_provider
 credit_card_security_code
 cryptocurrency
 cryptocurrency_code
 cryptocurrency_name
 csv
 currency
 currency_code
 currency_name
 currency_symbol
 current_country
 current_country_code
 date
 date_between
 date_between_dates
 date_object
 date_of_birth
 date_this_century
 date_this_decade
 date_this_month
 date_this_year
 date_time
 date_time_ad
 date_time_between
 date_time_between_dates
 date_time_this_century
 date_time_this_decade
 date_time_this_month
 date_time_this_year
 day_of_month
 day_of_week
 del_arguments
 dga
 domain_name
 domain_word
 dsv
 ean
 ean13
 ean8
 ein
 email
 emoji
 enum
 factories
 file_extension
 file_name
 file_path
 firefox
 first_name
 first_name_female
 first_name_male
 first_name_nonbinary
 fixed_width
 format
 free_email
 free_email_domain
 future_date
 future_datetime
 generator_attrs
 get_arguments
 get_formatter
 get_providers
 get_words_list
 hex_color
 hexify
 hostname
 http_method
 http_status_code
 iana_id
 iban
 image
 image_url
 internet_explorer
 invalid_ssn
 ios_platform_token
 ipv4
 ipv4_network_class
 ipv4_private
 ipv4_public
 ipv6
 isbn10
 isbn13
 iso8601
 items
 itin
 job
 json
 json_bytes
 language_code
 language_name
 last_name
 last_name_female
 last_name_male
 last_name_nonbinary
 latitude
 latlng
 lexify
 license_plate
 linux_platform_token
 linux_processor
 local_latlng
 locale
 locales
 localized_ean
 localized_ean13
 localized_ean8
 location_on_land
 longitude
 mac_address
 mac_platform_token
 mac_processor
 md5
 military_apo
 military_dpo
 military_ship
 military_state
 mime_type
 month
 month_name
 msisdn
 name
 name_female
 name_male
 name_nonbinary
 nic_handle
 nic_handles
 null_boolean
 numerify
 opera
 optional
 paragraph
 paragraphs
 parse
 passport_dates
 passport_dob
 passport_full
 passport_gender
 passport_number
 passport_owner
 password
 past_date
 past_datetime
 phone_number
 port_number
 postalcode
 postalcode_in_state
 postalcode_plus4
 postcode
 postcode_in_state
 prefix
 prefix_female
 prefix_male
 prefix_nonbinary
 pricetag
 profile
 provider
 providers
 psv
 pybool
 pydecimal
 pydict
 pyfloat
 pyint
 pyiterable
 pylist
 pyobject
 pyset
 pystr
 pystr_format
 pystruct
 pytimezone
 pytuple
 random
 random_choices
 random_digit
 random_digit_above_two
 random_digit_not_null
 random_digit_not_null_or_empty
 random_digit_or_empty
 random_element
 random_elements
 random_int
 random_letter
 random_letters
 random_lowercase_letter
 random_number
 random_sample
 random_uppercase_letter
 randomize_nb_elements
 rgb_color
 rgb_css_color
 ripe_id
 safari
 safe_color_name
 safe_domain_name
 safe_email
 safe_hex_color
 sbn9
 secondary_address
 seed
 seed_instance
 seed_locale
 sentence
 sentences
 set_arguments
 set_formatter
 sha1
 sha256
 simple_profile
 slug
 ssn
 state
 state_abbr
 street_address
 street_name
 street_suffix
 suffix
 suffix_female
 suffix_male
 suffix_nonbinary
 swift
 swift11
 swift8
 tar
 text
 texts
 time
 time_delta
 time_object
 time_series
 timezone
 tld
 tsv
 unique
 unix_device
 unix_partition
 unix_time
 upc_a
 upc_e
 uri
 uri_extension
 uri_page
 uri_path
 url
 user_agent
 user_name
 uuid4
 vin
 weights
 windows_platform_token
 word
 words
 xml
 year
 zip
 zipcode
 zipcode_in_state
 zipcode_plus4
'''



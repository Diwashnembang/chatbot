import psycopg2
import os
from dotenv import load_dotenv

def connectDB(host, user, password, dbname):
    conn = psycopg2.connect(
        host=host,
        database=dbname,
        user=user,
        password=password,
        port=5432
    )
    return conn

def createDBConection():
    conn = connectDB(os.getenv('DB_HOST'), os.getenv('DB_USER'), os.getenv('DB_PASSWORD'), os.getenv('DB_NAME'))
    return conn

def seedResonses():
    conn = connectDB(os.getenv('DB_HOST'), os.getenv('DB_USER'), os.getenv('DB_PASSWORD'), os.getenv('DB_NAME'))
    cur = conn.cursor()
    
    # Create table
    create_table_query = '''
    CREATE TABLE faq (
        id SERIAL PRIMARY KEY,
        question TEXT NOT NULL,
        answer TEXT NOT NULL
    );
    '''
    cur.execute(create_table_query)
    
    # List of FAQs to insert
    faq_data = [
        ('What products do you sell?', 'We specialize in a wide range of tech products, including smartphones, laptops, headphones, smartwatches, gaming accessories, and more! Feel free to browse our categories to find what you\'re looking for.'),
        ('Do you offer international shipping?', 'Yes, we offer international shipping to many countries. You can check if we deliver to your location by entering your address during checkout.'),
        ('How can I track my order?', 'Once your order has shipped, we will send you a tracking number via email. You can also track your order by logging into your account and going to the "My Orders" section.'),
        ('Can I change my order after it\'s been placed?', 'Unfortunately, once an order is confirmed and processed, it can\'t be modified. However, you can contact our customer support for assistance, and we will try our best to help.'),
        ('How do I return an item?', 'If you\'re not satisfied with your purchase, you can return items within 30 days of receiving them. Please visit our Returns & Exchanges page for more details on how to initiate a return.'),
        ('What payment methods do you accept?', 'We accept credit and debit cards, PayPal, and Apple Pay. You can select your preferred payment method during checkout.'),
        ('Is it safe to shop on your website?', 'Yes, we take your security seriously. Our website uses encryption to protect your personal and payment information. You can shop with confidence.'),
        ('Do you offer gift cards?', 'Yes, we offer gift cards in various denominations. You can purchase them directly from our Gift Card section on the website.'),
        ('Do you offer discounts or promotions?', 'We frequently offer sales, discounts, and promotions. You can sign up for our newsletter or check our Promotions page to stay updated on the latest offers.'),
        ('How can I contact customer support?', 'You can reach our customer support team through our Contact Us page or by emailing support@gadgethub.com. We\'re here to help!')
    ]

    # Insert data
    insert_query = 'INSERT INTO faq (question, answer) VALUES (%s, %s);'
    cur.executemany(insert_query, faq_data)
    
    
    conn.commit()
    cur.close()
    conn.close()



if __name__ == '__main__':
    load_dotenv()
    seedResonses()
    print('Database seeded successfully!')
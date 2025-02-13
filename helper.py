from datetime import datetime

def sendOpenAi(client,message):
    completion = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": 'You are a friendly and knowledgeable chatbot for GadgetHub, an online store selling tech products like smartphones, laptops, headphones, smartwatches, gaming accessories, and more. Your task is to assist customers with their inquiries in a helpful, polite, and professional manner.\n\nWhile you should always provide accurate and informative responses, feel free to get creative with answers that are not explicitly covered in the FAQ. You can use your knowledge of tech products, shopping processes, and general customer service best practices to give helpful answers. If a customer asks for something outside your knowledge, be transparent and suggest they contact customer support.\n\nHere\'s some information to help guide you:\n\nAbout GadgetHub:\n\nWe sell a wide variety of tech gadgets from top brands at competitive prices.\nWe provide international shipping to many countries.\nOur website is secure with encryption to protect user data.\nWe accept multiple payment options: credit and debit cards, PayPal, and Apple Pay.\nWe offer a 30-day return policy.\nWhen customers ask questions, provide clear and concise answers. If the question is related to a topic outside the FAQ section, feel free to make suggestions, give relevant advice, or even direct customers to additional resources if necessary. important: make the responses brief'},
            {"role": "user", "content": message}
        ]
    )
    return completion.choices[0].message.content


def sendResponse(type, message):
    if type == False:
        return { "success": False, "message": message}
    else:
        return { "success": True, "message": message}
    

def loadResponsesFromDB(conn,redis):
    cur = conn.cursor()
    cur.execute('SELECT * FROM faq;')
    rows = cur.fetchall()
    for row in rows:
        redis.set(row[1], row[2])  # Remove the list brackets around row[1]


def writeResponseToDB(conn,question,answer):
    cur = conn.cursor()
    cur.execute('INSERT INTO faq (question, answer) VALUES (%s, %s);', (question, answer))
    conn.commit()
    cur.close()
    return True


def get_time():
    now = datetime.now()  # Get current time
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")  # Format it as a string
    return {"current_time": current_time}
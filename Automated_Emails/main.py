#import schedule
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random

smtp_server = "smtp.gmail.com"
smtp_port = 587
sender = "mercedesmotivational9@gmail.com"
pw = "ylkc xrlz xcwx efwf"
recipient = "youngdirk2005@gmail.com"
subject = "Motivational Quote #1"

nouns = [
    "heart", "smile", "soulmate", "life", "dream", "world", "everything", "love", "voice", "match"
]

adjectives = [
    "precious", "amazing", "beautiful", "wonderful", "perfect", "incredible", "lovely", "adorable", "charming", "delightful"
]

verbs = [
    "cherish", "admire", "love", "adore", "treasure", "value", "respect", "honor", "appreciate", "embrace"
]

phrases = [
    "Forever in my", "You are my", "My heart belongs to you", "I am yours", "You complete me", "I am grateful for you"
]

templates = [
    "My {adjective} {noun} belongs to you, {phrase}.",
    "You are my {adjective} {noun}, I {verb} you endlessly.",
    "Every time I think of you, my {noun} fills with {adjective}.",
    "With you, life feels {adjective} and {adjective}.",
    "My {noun} belongs to you, {phrase}, always.",
    "Forever {adjective} in my {noun}, my precious {noun}."
]

def generate_message():
    template = random.choice(templates)
    selected_adjectives = random.sample(adjectives, 2)
    selected_nouns = random.sample(nouns, 2)
    selected_verb = random.choice(verbs)
    selected_phrase = random.choice(phrases)
    
    message = template.format(
        adjective=selected_adjectives[0],
        noun=selected_nouns[0],
        verb=selected_verb,
        phrase=selected_phrase
    )
    
    message = message.replace("{adjective}", selected_adjectives[1], 1)
    message = message.replace("{noun}", selected_nouns[1], 1)
    
    return message.capitalize()

def send_email():
    message = MIMEMultipart()
    message["From"] = sender
    message["To"] = recipient
    message["Subject"] = subject
    body = generate_message()
    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender, pw)
            server.sendmail(sender, recipient, message.as_string())
    except Exception as e:
        print(f"Failed to send email: {e}")

send_email()
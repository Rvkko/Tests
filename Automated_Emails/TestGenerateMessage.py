import re
from main import generate_message

# MainFILE: test_main.py


class TestGenerateMessage:
    
    def test_generate_message_structure(self):
        message = generate_message()
        assert message[0].isupper()
        assert message.endswith('.')
        assert any(word in message for word in ["precious", "amazing", "beautiful", "wonderful", "perfect", "incredible", "lovely", "adorable", "charming", "delightful"])
        assert any(word in message for word in ["heart", "smile", "soulmate", "life", "dream", "world", "everything", "love", "voice", "match"])
        assert any(word in message for word in ["cherish", "admire", "love", "adore", "treasure", "value", "respect", "honor", "appreciate", "embrace"])
        assert any(phrase in message for phrase in ["Forever in my", "You are my", "My heart belongs to you", "I am yours", "You complete me", "I am grateful for you"])

    def test_generate_message_randomness(self):
        messages = {generate_message() for _ in range(100)}
        assert len(messages) > 1
        
        import re
from main import generate_message

# MailFILE: test_main.py


class TestGenerateMessage:
    
    def test_generate_message_structure(self):
        message = generate_message()
        assert message[0].isupper()
        assert message.endswith('.')
        assert any(word in message for word in ["precious", "amazing", "beautiful", "wonderful", "perfect", "incredible", "lovely", "adorable", "charming", "delightful"])
        assert any(word in message for word in ["heart", "smile", "soulmate", "life", "dream", "world", "everything", "love", "voice", "match"])
        assert any(word in message for word in ["cherish", "admire", "love", "adore", "treasure", "value", "respect", "honor", "appreciate", "embrace"])
        assert any(phrase in message for phrase in ["Forever in my", "You are my", "My heart belongs to you", "I am yours", "You complete me", "I am grateful for you"])

    def test_generate_message_randomness(self):
        messages = {generate_message() for _ in range(100)}
        assert len(messages) > 1
from project_chat.server.server import FeedData

byte_str = b'{"action": "msg", "time": 1615116818.8811924, "message": {"account_name": "igorw", "password": ' \
           b'"123"}} '

f = FeedData(byte_str)
t = f.analysis_data()
print(t)
import shelve
import configparser
config=configparser.ConfigParser()
config.add_section("hello")
config.set("hello","name","merlin")
config.write(open(r"C:\Users\30294\Desktop\hg\config.ini","w+"))
result=config.read(r"C:\Users\30294\Desktop\hg\config.ini")
items=dict(config.items("hello"))
print(items)



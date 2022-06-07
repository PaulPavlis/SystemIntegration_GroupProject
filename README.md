# Requirements

Tested with (stomp.py did not work with the newest version for me):

```
python-telegram-bot==13.11
stomp.py==4.1.21
```

You also need to install apache activemq. It is tested with version 5.17.1 (https://activemq.apache.org/components/classic/download/)

# ActiveMQ

### Start ActiveMQ

```
apache-activemq-5.17.1\bin\activemq start
```

### Access WEBUI

```
http://localhost:8161/admin/
```

# Start MessageBroker

```
python Message_Broker\Message_Broker.py
```

# Start IOT Device

```
python Smart_Home_IOT\IOT_device.py --my_name="Lamp 1" -stl=/topic/topic_lamp1 -stl=/topic/topic_all_lamps
```

```
python Smart_Home_IOT\IOT_device.py --my_name="Lamp 2" -stl=/topic/topic_lamp2 -stl=/topic/topic_all_lamps
```

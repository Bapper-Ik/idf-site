
def event_serializer(event_info):
    return {
        "name": event_info.name,
        "start_date": event_info.start_date,
        "end_date": event_info.end_date,
        "venue": event_info.venue,
        "time": event_info.time,
    }
    
    

def image_serializer(image_info):
    return {
        "url": image_info.url,
        "caption": image_info.caption,
    }
    

def user_serializer(user_info):
    return {
        "id": user_info.id,
        "username": user_info.username,
        "role": user_info.role
    }
    
    
    
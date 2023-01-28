from enum import Enum

class MessageType(Enum):
    # Messages sent by the server

    # Special messages
    ping = "ping"
    error = "error"
    
    # Notifications
    game_invitation = "game_invitation"

    # In-game events
    user_joined_game = "user_joined_game"
    player_submitted = "submission_submitted"
    subimission_results = "subimission_results"
    game_results = "game_results"

    # Chat messages
    user_joined_chat = "user_joined_chat"
    user_left_chat = "user_left_chat"
    message_sent = "message_sent"
    message_deleted = "message_deleted"
    message_edited = "messaged_edited"


    # Messages sent by the client

    # Special messages
    pong = "pong"
    
    # In-game Events
    watch_game = "watch_game"

    # Chat messages
    join_chat = "join_chat"
    leave_chat = "leave_chat"
    send_message = "send_message"
    delete_message = "delete_message"
    edit_message = "edit_message"
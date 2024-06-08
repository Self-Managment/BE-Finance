import json

from typing import Any

class Commands:
    create_user = "create_user"
    
    @staticmethod
    def get_command_message(command: str, data: Any, dump: bool = False) -> dict:
        message = {
            "command": command,
            "data": data,
        }
        
        if dump:
            message = json.dumps(message)
            
        return message
    
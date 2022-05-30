import socket

class Rcon():
    def __init__(self, ip: str, port: int, password: int, timeout: float = 0.7) -> None:
        """Initialize rcon connection

        Args:
            ip (str): Server ip adress
            port (int): Rcon port
            password (int): Rcon password
            timeout (float, optional): Defaults to 0.7.
        """

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.ip = ip
        self.port = port
        self.password = password 
        
        self.socket.connect((self.ip, self.port))
        self.socket.settimeout(timeout)
        
        
    def __del__(self) -> None:
        "Close rcon connection on object destruction"
        self.socket.close()
    
    
    def recv(self):
        "Gets server response"
        return self.socket.recv(8192)
    
    
    def send(self, command: str) -> str:
        """Send rcon command

        Args:
            command (str): Rcon command to send

        Returns:
            str: Rcon responce
        """
        
        buffer = 0xFFFFFFFF.to_bytes(4, byteorder='big') # magic code
        buffer += bytes('rcon ', 'utf-8')
        buffer += bytes(self.password, 'utf-8')
        buffer += bytes(' ', 'utf-8')
        buffer += bytes(command, 'utf-8')
        
        self.socket.send(buffer)
        try:
            respoce = self.recv()
        except Exception:
            respoce = None
            
        if respoce :
            if str(respoce[4:])[:8] == "b'print " and str(respoce[4:])[8:-3] != "": return str(respoce[4:])[8:-3].replace('\\n','\n')
            else:  return 0
        else: return 0
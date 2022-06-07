import socket
import traceback
import re


class Whale:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.w = True

    def getTemplate(self, TamplatePath, parmer={}):
        path = TamplatePath
        if 'template/' not in path:
            path = 'template/'+path
        with open(path)as f:
            r = f.read()
        compil = r'\{\{.{1,}\}\}'
        for x in re.findall(compil, r):
            x1 = x[2:-2]
            r = r.split('\n')
            try:
                for i in range(len(r)):
                    y = r[i]
                    for z in range(0, len(x)):
                        if y[z:len(x)+z] == x:
                            y = y[:z]+str(parmer[x1])+y[len(x)+z:]
                            r[i] = y
            except Exception:
                self.run('', error=True)
        s = ''
        for x in r:
            s += x
        return s

    def close(self):
        self.w = False
        self.s.close()

    def run(self, req, listen=5, host=socket.gethostname(), port=8080, error=False):
        while True:
            try:
                self.s.bind((host, port))
                break
            except OSError:
                port += 1
        print('host:'+str(host)+'\nport:' +
              str(port)+'\n', str(host)+':'+str(port))
        if error:
            while 1:
                e = traceback.format_exc().split('\n')
                e1 = ''
                for x in e:
                    e1 += '<p>'+x+'</p>'
                    print(e1)
                    error = '''
    <!DOCTYPE html>
    <html lang="en">

    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>error</title>
    </head>

    <body>
        {}
    </body>

    </html>
    '''.format(e1)
                self.s.listen(listen)
                conn, addr = self.s.accept()
                print('\033[92m'+conn.recv(1024).decode('utf-8')+'\033[0m')
                conn.send(b'Http/1.1 200 ok\r\n\r\n')
                conn.send(error.encode('utf-8'))
                conn.close()
        while self.w:
            try:
                self.s.listen(listen)
                conn, addr = self.s.accept()
                print('\033[92m'+conn.recv(1024).decode('utf-8')+'\033[0m')
                conn.send(b'Http/1.1 200 ok\r\n\r\n')
                conn.send(req.encode('utf-8'))
                conn.close()
            except Exception:
                while 1:
                    e = traceback.format_exc().split('\n')
                    e1 = ''
                    for x in e:
                        e1 += '<p>'+x+'</p>'
                    print(e1)
                    error = '''
    <!DOCTYPE html>
    <html lang="en">

    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>error</title>
    </head>

    <body>
        {}
    </body>

    </html>
    '''.format(e1)
                    self.s.listen(listen)
                    conn, addr = self.s.accept()
                    print('\033[92m'+conn.recv(1024).decode('utf-8')+'\033[0m')
                    conn.send(b'Http/1.1 200 ok\r\n\r\n')
                    conn.send(error.encode('utf-8'))
                    conn.close()

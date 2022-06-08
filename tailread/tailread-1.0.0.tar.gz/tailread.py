from io import BufferedReader



def readlines(bytesio, batch_size=1024, keepends=True, **encoding_kwargs):
    '''bytesio: file path or BufferedReader
       batch_size: size to be processed
    '''
    path = None
    
    if isinstance(bytesio, str):
        path = bytesio
        bytesio = open(path, 'rb')
    elif not isinstance(bytesio, BufferedReader):
        raise TypeError('The first argument to readlines must be a file path or a BufferedReader')

    bytesio.seek(0, 2)
    end = bytesio.tell()

    buf = b""
    for p in reversed(range(0, end, batch_size)):
        bytesio.seek(p)
        lines = []
        remain = min(end-p, batch_size)
        while remain > 0:
            line = bytesio.readline()[:remain]
            lines.append(line)
            remain -= len(line)

        cut, *parsed = lines
        for line in reversed(parsed):
            if buf:
                line += buf
                buf = b""
            if encoding_kwargs:
                line = line.decode(**encoding_kwargs)
            yield from reversed(line.splitlines(keepends))
        buf = cut + buf
    
    if path:
        bytesio.close()

    if encoding_kwargs:
        buf = buf.decode(**encoding_kwargs)
    yield from reversed(buf.splitlines(keepends))
# ch05_netapi.py
# Define a class NetAPI to utilize NetworkIO to send/recv data.
import socket, struct, sys, os


def server(host, port):
    typename = { int:'int', str:'str', bytes:'bytes', float:'float' }  # dict
    listeningSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listeningSock.bind( (host, port) )
    listeningSock.listen()
    print("Listening at", listeningSock.getsockname())

    while True:
        sock, sockname = listeningSock.accept()
        handle = NetAPI(sock)
        while True:
            data = handle.recv_file()   # It will receive a dict (P.5-8,5-24)
            if not data:
                break
            print('receive  from {}\n{}'.format(sockname, data))
            handle.save_file(data, os.path.join(handle.savePath, sockname[0]))
        sock.close()

    listeningSock.close()

def client(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect( (host, port) )

    handle = NetAPI(sock)
    while True:
        f = input("Input filename to transmit -- ")
        if f == '':
            break
        handle.send_file(f)

    sock.close()

class NetAPI:
    # Constants defined in P.5-4
    FILE_TAG_SIZE       = 8
    FILE_END_TAG        = b'FILEEND0'
    FILE_NAME_TAG       = b'FILENAME'
    FILE_SIZE_TAG       = b'FILESIZE'
    FILE_CONTENT_TAG    = b'FILEDATA'
    FILE_ABORT_TAG      = b'FILEABRT'
    FILE_BLOCKS_TAG     = b'FILEBLKS'

    def __init__(self, iHandle=None, oHandle=None):
        if not iHandle:
            iHandle     = b''
        if not oHandle:
            oHandle     = iHandle
        from ch05_networkio import NetworkIO
        self.iHandle    = NetworkIO(iHandle)
        self.oHandle    = NetworkIO(oHandle)
        self.savePath   = './'       # 存檔目錄
        self.maxSize    = 2147483647            # 最大檔案限制
        self.blockSize  = 1024                  # 區塊大小

    def save_file(self, file_info, dir):
        import os
        import shutil
        filename = file_info.get(self.FILE_NAME_TAG)
        filesize = file_info.get(self.FILE_SIZE_TAG)
        content = file_info.get(self.FILE_CONTENT_TAG)
        tempFile = file_info.get(self.FILE_BLOCKS_TAG)
        if not filename or not filesize:
            return False
        if not content and not tempFile:
            return False
        else:
            fullname = os.path.join(dir, filename)
            dirname = os.path.dirname(fullname)
            if not os.path.exists(dirname):
                os.makedirs(dirname)
            if content:
                if len(content) != filesize:
                    raise RuntimeError('size mismatches')
                with open(fullname, 'wb') as fp:
                    fp.write(content)
            else:
                if os.path.getsize(tempFile) != filesize:
                    raise RuntimeError('size mismatches')
                shutil.move(tempFile, fullname)
            return True

    def send_tag(self, tag):    self.oHandle.write_raw(tag)
    
    def recv_tag(self): return self.iHandle.read_raw(self.FILE_TAG_SIZE)

    def send_data(self, data):  self.oHandle.write(data)
    
    def recv_data(self): return self.iHandle.read()

    def send_size(self, n):     return self.send_data(n)
    
    def recv_size(self):
        size = self.recv_data()
        if not isinstance(size, int):   # 檢查類別是否為 int
            raise TypeError('Invalid size type %s' % type(size))
        return size

    def send_name(self, s):     return self.send_data(s)
    
    def recv_name(self):
        path = self.recv_data()
        if not isinstance(path, str):   # 檢查是否為 str
            raise TypeError('Invalid size type %s' % type(path))
        return path

    def send_content(self, d):  return self.send_data(d)
    
    def recv_content(self):     return self.recv_data()

    def send_file(self, path):
        import os
        filename = path
        filesize = os.path.getsize(path)
        try:
            self.send_tag(self.FILE_NAME_TAG)
            self.send_name(filename)
            self.send_tag(self.FILE_SIZE_TAG)
            self.send_size(filesize)
            if filesize > self.blockSize:
                self.send_tag(self.FILE_BLOCKS_TAG)
                self.send_blocks(filename)
            else:
                filedata = open(path, 'rb').read()
                self.send_tag(self.FILE_CONTENT_TAG)
                self.send_content(filedata)
            self.send_tag(self.FILE_END_TAG)
            return True
        except Exception as e:
            print(str(e))
            self.send_tag(self.FILE_ABORT_TAG)
            return False

    def recv_file(self):
        result = {}
        while True:
            tag = self.recv_tag()
            print(tag)
            if not tag or tag in [self.FILE_END_TAG, self.FILE_ABORT_TAG]: break
            if tag == self.FILE_BLOCKS_TAG:
                tempFile = self.recv_blocks()
                result[tag] = tempFile
            else:
                data = self.recv_data()
                if not data: break
                if tag in self.FILE_NAME_TAG:
                    data = data.replace(":\\", "/").replace("\\", "/")
                    data = data[1:] if data[0] in "/" else data
                    
                    if ".." in data:
                        raise ValueError("Dangerous path.")
                result[tag] = data
        return result

    def send_blocks(self, fileName):
        fp = open(fileName, 'rb')
        blockID = 0
        totalSize = 0
        print("[DEBUG] Sending blocks")
        while True:
            block = fp.read(self.blockSize)
            if not block:
                break
            blockID += 1
            self.send_data(blockID)
            print("[DEBUG] sending block #{}: ".format(blockID), end=' ')
            self.send_data(block)
            print(block)
            totalSize += len(block)
        self.send_data(0)
        return totalSize

    def recv_blocks(self):
        import time
        totalSize = 0
        lastBlockID = 0
        fileName = os.path.abspath(os.path.join(self.savePath,
                                                'TEMP%x' % int(time.time())))
        dirname = os.path.dirname(fileName)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        with open(fileName, 'wb') as fp:
            while True:
                blockID = self.recv_data()
                print("[DEBUG]", blockID)
                assert isinstance(blockID, int), \
                    TypeError(f'invalid type of block id {type(blockID)}')
                if blockID == 0:       # End of blocks
                    break
                assert lastBlockID + 1 == blockID, \
                    ValueError(f'block ID error. Last: {lastBlockID} current: {blockID}')
                lastBlockID = blockID
                block = self.recv_data()
                print("[DEBUG]", block)
                assert isinstance(block, bytes), \
                    TypeError(f'invalid type of block {type(block)}')
                print("[DEBUG] {} <= {}".format(
                    len(block) + totalSize, self.maxSize))
                assert len(block) + totalSize <= self.maxSize, \
                    RuntimeError(f'exceed max file size limit {self.maxSize}')
                totalSize += len(block)
                fp.write(block)
        return fileName
    
    
def main():
    msg = "Usage: %s {server|client} host port" % sys.argv[0]
    if len(sys.argv) != 4:
        print(msg)
    else:
        host = sys.argv[2]
        port = int(sys.argv[3])
        if sys.argv[1] == "server":
            server(host, port)
        elif sys.argv[1] == "client":
            client(host, port)
        else:
            print(msg)

if __name__ == "__main__":
    main()


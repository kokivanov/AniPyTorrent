# import asyncio

# async def main():
#     print("Hi!")

# if __name__ == "__main__":
#     main()


from collections import OrderedDict
from client.utils.bencoder import Decoder
from client import Client

t = Client()
t.add_from_file("./_test/multifile.torrent")
print(list(t.torrentsQ.values())[0].files[0])
print(len(list(t.torrentsQ.values())[0].pieces[0]))


a : OrderedDict
with open('./_test/multifile.torrent', 'rb') as f:
    decode = Decoder(f.read())
    a = decode.decode()
print(a[b'info'][b'files'])

# print(list(t.fileQ.values())[0].info.pieces[0].hash)

# res = b''.join([i.value for i in list(t.fileQ.values())[0].info.pieces])
# # print(len(res))
# # print(len(b[b'info'][b'pieces']))
# # print(b[b'info'][b'pieces'])
# print(res == b[b'info'][b'pieces'])
# # print(res)

# print(res == )


# print(f"{[i.path for i in m.info.files]}")


# print(b[b'announce'])

# for k, v in b.items():
#     if k == b'pieces':
#         continue

#     print(k, v)


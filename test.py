import asyncio

async def main():
    print("Hi!")

if __name__ == "__main__":
    main()













# from utils.bencoder import Decoder
# import meta

# a : Decoder
# with open("./multifile.torrent", 'rb') as f:
#     a = Decoder(f.read())

# b = a.decode()
# m = meta.Meta(b)


# print(f"{m.info.files}")




# print(b[b'announce'])

# for k, v in b.items():
#     if k == b'pieces':
#         continue
    
#     print(k, v)
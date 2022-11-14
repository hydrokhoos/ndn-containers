from random import randbytes


def make_fake_data(size: int, name: str):
    size *= 1024
    data = randbytes(size)
    with open(name, 'wb') as f:
        f.write(data)


if __name__ == '__main__':
    sizes = [i for i in range(0, 1025, 64)]
    sizes.pop(0)
    sizes = [1] + sizes
    for i, size in enumerate(sizes):
        name = 'data' + str(i)
        make_fake_data(size, name)

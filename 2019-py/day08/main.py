width = 25
height = 6
layer_size = width*height
inp = open("i.txt").read()
layer = [inp[i:i+layer_size] for i in range(0, len(inp), layer_size)]
min_zero_layer = min(layer, key=lambda x: x.count('0'))
print(min_zero_layer.count('1') * min_zero_layer.count('2'))

def render_image(image_data, width, height):
    layer_size = width * height
    layers = [image_data[i:i + layer_size] for i in range(0, len(image_data), layer_size)]

    final_image = ['2'] * layer_size

    for layer in layers:
        for i, pixel in enumerate(layer):
            if final_image[i] == '2':
                final_image[i] = pixel

    rendered_image = [final_image[i:i + width] for i in range(0, layer_size, width)]

    return rendered_image

rendered = render_image(inp, width, height)

for row in rendered:
    print(''.join(row).replace('0', ' ').replace('1', '█'))
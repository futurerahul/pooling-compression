import os
from statistics import mean
from PIL import Image

def convet_img_to_matrix(path):
    """
    function to convert image to RGB matrix
    """
    img_mat = []
    with Image.open(path) as img:
        width,height = img.size
        print(f'Original image dimension: {width}x{height}')
        for x in range(width):
            row = []
            for y in range(height):
                img_rgb = img.getpixel((x,y))
                row.append(img_rgb)
            img_mat.append(row)
    return (img_mat,width,height)

def avg_pooling(img_mat, width, height):
    """
    Apply avg pooling 2x2 on image matrix
    """
    width = width if width%2==0 else width-1
    height = height if height%2==0 else height-1
    pooled = []
    for i in range(0, width, 2):
        x = []
        for j in range(0, height, 2):
            r = mean([img_mat[i][j][0], img_mat[i][j+1][0], img_mat[i+1][j][0], img_mat[i+1][j+1][0]])
            g = mean([img_mat[i][j][1], img_mat[i][j+1][1], img_mat[i+1][j][1], img_mat[i+1][j+1][1]])
            b = mean([img_mat[i][j][2], img_mat[i][j+1][2], img_mat[i+1][j][2], img_mat[i+1][j+1][2]])
            x.append((round(r),round(g),round(b)))
        pooled.append(x)
    return pooled

def generate_compressed_img(pooled, file_name):
    """
    function to generate and save compressed image
    """
    new_width = round(len(pooled))
    new_height = round(len(pooled[0]))

    new_img = Image.new(mode="RGB", size=(new_width, new_height))
    for x in range(new_width):
        for y in range(new_height):
            new_img.putpixel((x,y),pooled[x][y])

    new_img.save(f'{file_name}_compressed.jpg')
    print(f'Compressed image dimension: {new_width}x{new_height}')

def main(path, file_name):
    img_mat,width,height = convet_img_to_matrix(path)
    pooled_img_matrix = avg_pooling(img_mat,width,height)
    generate_compressed_img(pooled_img_matrix,file_name)


if __name__ == "__main__":
    path = input('Enter the image path: ')
    file_name, ext = os.path.splitext(path)
    if ext != '.jpg':
        print('Invalid JPG image file')
    else:
        main(path, file_name)
        compression_ratio = (1.0 - (os.stat(f'{file_name}_compressed.jpg').st_size/os.stat(path).st_size))*100
        print(f'Image compressed by {round(compression_ratio,2)}%')

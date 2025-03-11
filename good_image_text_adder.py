from PIL import Image, ImageDraw, ImageFont
import os


sub_folder = "/"
folder = f"./images{sub_folder}"
image_files = os.listdir(folder)

final_folder = folder.replace("./", "./new_")

# will have to add the subfolder.


# all file names need to be jpg. so that is replaced at the beginning of the script.

for i, real_image_name in enumerate(image_files):

    # if i < 15:
    #     continue

    # if "95" not in real_image_name:
    #     continue

    real_image_name = real_image_name.replace(".jpg", "")
    img = Image.open(f"{folder}/{real_image_name}.jpg").convert("RGBA")
    image_name = real_image_name.replace(" - dina4", "")
    # font = ImageFont.truetype('WorkSans-Regular.ttf', 282)
    # font = ImageFont.truetype("impact.ttf",25)
    # font = ImageFont.FreeTypeFont("arial.ttf",36)

    font = ImageFont.truetype("fonts/arial.ttf", 98)  # ImageFont.load_default()
    x, y = img.size

    # print(txt_layer.size)
    # print(img.size)
    txt_layer = Image.new("RGBA", (x, y), (255, 255, 255, 0))
    draw = ImageDraw.Draw(txt_layer)

    text_w, text_h = draw.textsize(image_name, font=font)

    # Calculate the font size that you need to use
    font_size = int(min((x) * 0.9 / text_w, (y) * 0.9 / text_h) * font.size)

    draw.text(
        ((x - text_w) / 2, (y - text_h) / 1.5),
        image_name,
        font=font,
    )

    good_font = ImageFont.truetype("fonts/arial.ttf", font_size)

    new_txt_layer = Image.new("RGBA", (x, y), (255, 255, 255, 0))
    new_draw = ImageDraw.Draw(new_txt_layer)

    position = (x / 8, y / 4)

    new_draw.text(
        position,
        image_name,
        font=good_font,
        fill=(
            0,
            0,
            0,
            25,
            # 2,157,229, 130 # 130
        ),
    )

    # new_txt_layer.save("test.png","PNG")

    new_img = Image.alpha_composite(img, new_txt_layer)
    # new_img.show()
    new_img.save(f"{final_folder}/{real_image_name}.png")

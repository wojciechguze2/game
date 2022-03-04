import cv2


def resize_image(image_path, width, height) -> True:
    img = cv2.imread(image_path, 1)

    resized_image = cv2.resize(img, (width, height))

    cv2.imwrite(image_path, resized_image)

    return True

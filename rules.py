import cv2

import const


def resize_image(image_path: str, width: float, height: float, resized_image_path=const.RESIZED_IMAGE_PATH) -> str:
    img = cv2.imread(image_path, 1)

    resized_image = cv2.resize(img, (width, height))

    cv2.imwrite(resized_image_path, resized_image)

    return resized_image_path

#cv.py

import cv2
import tempfile
import shutil
import os
import numpy as np
from datetime import datetime
from typing import List, Callable, Union

class ImageManager:
    def __init__(self) -> None:
        """
        Initializes the ImageManager with a temporary file path for saving processed images.
        """
        self.temp_file_path: Union[str, None] = None

    def _save_temp_image(self, image: np.ndarray) -> None:
        """
        Saves the given image to a temporary file and stores the file path.
        
        Parameters:
        - image (np.ndarray): The image to save.
        """
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
            self.temp_file_path = temp_file.name
            cv2.imwrite(self.temp_file_path, image)
        print(f"Temporary image saved to: {self.temp_file_path}")

    def set_cropped(
        self, 
        supported_files: List[str], 
        current_index: int, 
        settings: List[int], 
        load_image_callback: Callable[[str], None]
    ) -> None:
        """
        Crops the image based on the specified coordinates.
        
        Parameters:
        - supported_files (List[str]): List of image files to process.
        - current_index (int): Index of the current image in the list.
        - settings (List[int]): Coordinates for cropping (start_x, start_y, end_x, end_y).
        - load_image_callback (Callable[[str], None]): Callback to load the processed image.
        """
        input_file = supported_files[current_index]
        frame = cv2.imread(input_file)

        s_x, s_y, e_x, e_y = settings
        if not (0 <= s_x < e_x <= frame.shape[1] and 0 <= s_y < e_y <= frame.shape[0]):
            print(f"Invalid coordinates for cropping in {input_file}. Skipping cropping.")
            return

        cropped_frame = frame[s_y:e_y, s_x:e_x].copy()
        self._save_temp_image(cropped_frame)
        load_image_callback(self.temp_file_path)

    def set_resize(
        self, 
        supported_files: List[str], 
        current_index: int, 
        settings: List[int], 
        load_image_callback: Callable[[str], None]
    ) -> None:
        """
        Resizes the image to the specified width and height.
        
        Parameters:
        - supported_files (List[str]): List of image files to process.
        - current_index (int): Index of the current image in the list.
        - settings (List[int]): New width and height for resizing.
        - load_image_callback (Callable[[str], None]): Callback to load the processed image.
        """
        input_file = supported_files[current_index]
        frame = cv2.imread(input_file)

        width, height = settings
        if width <= 0 or height <= 0:
            print(f"Invalid resize dimensions for {input_file}. Skipping resizing.")
            return

        resized_frame = cv2.resize(frame, (width, height))
        self._save_temp_image(resized_frame)
        load_image_callback(self.temp_file_path)

    def set_brightness(
        self, 
        supported_files: List[str], 
        current_index: int, 
        settings: List[float], 
        load_image_callback: Callable[[str], None]
    ) -> None:
        """
        Adjusts the brightness of the image using the specified factor.
        
        Parameters:
        - supported_files (List[str]): List of image files to process.
        - current_index (int): Index of the current image in the list.
        - settings (List[float]): Brightness adjustment factor.
        - load_image_callback (Callable[[str], None]): Callback to load the processed image.
        """
        input_file = supported_files[current_index]
        frame = cv2.imread(input_file)

        frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        factor = settings
        frame_hsv[:, :, 2] = np.clip(frame_hsv[:, :, 2] * factor, 0, 255)
        frame = cv2.cvtColor(frame_hsv, cv2.COLOR_HSV2BGR)

        self._save_temp_image(frame)
        load_image_callback(self.temp_file_path)

    def set_saturation(
        self, 
        supported_files: List[str], 
        current_index: int, 
        settings: List[float], 
        load_image_callback: Callable[[str], None]
    ) -> None:
        """
        Adjusts the saturation of the image using the specified factor.
        
        Parameters:
        - supported_files (List[str]): List of image files to process.
        - current_index (int): Index of the current image in the list.
        - settings (List[float]): Saturation adjustment factor.
        - load_image_callback (Callable[[str], None]): Callback to load the processed image.
        """
        input_file = supported_files[current_index]
        frame = cv2.imread(input_file)

        frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        factor = settings
        frame_hsv[:, :, 1] = np.clip(frame_hsv[:, :, 1] * factor, 0, 255)
        frame = cv2.cvtColor(frame_hsv, cv2.COLOR_HSV2BGR)

        self._save_temp_image(frame)
        load_image_callback(self.temp_file_path)

    def set_rotate_90(
        self, 
        supported_files: List[str], 
        current_index: int, 
        settings: int, 
        load_image_callback: Callable[[str], None]
    ) -> None:
        """
        Rotates the image by 90 degrees, the number of times specified by settings.
        
        Parameters:
        - supported_files (List[str]): List of image files to process.
        - current_index (int): Index of the current image in the list.
        - settings (int): Number of 90-degree rotations (1, 2, 3).
        - load_image_callback (Callable[[str], None]): Callback to load the processed image.
        """
        input_file = supported_files[current_index]
        frame = cv2.imread(input_file)

        angle = settings
        if 0 < angle < 4:
            frame = np.rot90(frame, angle)
        else:
            print(f"Invalid dimensions for rotation in {input_file}. Skipping rotation.")

        self._save_temp_image(frame)
        load_image_callback(self.temp_file_path)

    def set_flip(
        self, 
        supported_files: List[str], 
        current_index: int, 
        settings: str, 
        load_image_callback: Callable[[str], None]
    ) -> None:
        """
        Flips the image either vertically or horizontally.
        
        Parameters:
        - supported_files (List[str]): List of image files to process.
        - current_index (int): Index of the current image in the list.
        - settings (str): The flip direction ('vertically' or 'horizontally').
        - load_image_callback (Callable[[str], None]): Callback to load the processed image.
        """
        input_file = supported_files[current_index]
        frame = cv2.imread(input_file)

        if settings == 'vertically':
            frame = np.flipud(frame)
        elif settings == 'horizontally':
            frame = np.fliplr(frame)
        else:
            print(f"Invalid flip option in {input_file}. Skipping flip.")
            return

        self._save_temp_image(frame)
        load_image_callback(self.temp_file_path)
    
    def save_image(
        self, 
        supported_files: List[str], 
        current_index: int
    ) -> None:
        """
        Saves the processed image to the file system.
        
        Parameters:
        - supported_files (List[str]): List of image files to process.
        - current_index (int): Index of the current image in the list.
        """
        if not supported_files:
            print("No images to process.")
            return

        if current_index >= len(supported_files):
            print("Invalid current index. Cannot find the image.")
            return

        if self.temp_file_path is None:
            print("No processed image available to save.")
            return

        current_image_path = supported_files[current_index]
        destination_path = (
            os.path.splitext(current_image_path)[0]
            + '_'
            + datetime.now().strftime("%Y%m%d_%H%M%S")
            + os.path.splitext(current_image_path)[1]
        )

        try:
            shutil.copyfile(self.temp_file_path, destination_path)
            print(f"Image successfully saved as: {destination_path}")
        except Exception as e:
            print(f"Error occurred while saving the image: {e}")

image_manager = ImageManager()

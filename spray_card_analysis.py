import os
import cv2
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt

class SprayCardAnalyzer:
    """
    A class to analyze spray cards by computing the sprayed area percentage 
    in sections of the card image.

    Attributes:
        image_path (str): Path to the spray card image file.
        original_image (Image): Original image loaded using PIL.
        gray_image (numpy.ndarray): Grayscale representation of the original image.
        thresholded_image (numpy.ndarray): Binary thresholded image separating white from non-white areas.
        visualized_image (numpy.ndarray): Image with analysis visualization.
        non_white_areas (list): List storing the percentage of non-white pixels for each section.
    """

    def __init__(self, image_path: str):
        """
        Initializes SprayCardAnalyzer with an image path and loads the image.

        Parameters:
            image_path (str): Path to the spray card image.
        """
        self.image_path = image_path
        self.original_image = Image.open(image_path)
        self.gray_image = None
        self.thresholded_image = None
        self.visualized_image = None
        self.non_white_areas = []

    def convert_to_grayscale(self):
        """Converts the original image to grayscale."""
        self.gray_image = cv2.cvtColor(np.array(self.original_image), cv2.COLOR_RGB2GRAY)

    def apply_threshold(self):
        """Applies Otsu's binary thresholding to separate non-white (sprayed) areas from white areas."""
        _, self.thresholded_image = cv2.threshold(
            self.gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )

    def analyze_sections(self, sections=10):
        """
        Divides the thresholded image into specified sections, calculates the percentage of non-white pixels 
        (spray coverage) per section, and visualizes these sections with percentage labels.

        Parameters:
            sections (int): Number of vertical sections to divide the image into.
        """
        height, width = self.thresholded_image.shape
        section_width = width // sections
        self.visualized_image = cv2.cvtColor(self.thresholded_image, cv2.COLOR_GRAY2BGR)

        for i in range(sections):
            section = self.thresholded_image[:, i * section_width:(i + 1) * section_width]
            non_white_pixels = np.sum(section < 255)
            total_pixels = section.size
            non_white_area_percentage = (non_white_pixels / total_pixels) * 100
            self.non_white_areas.append(non_white_area_percentage)

            # Draw rectangle around section
            cv2.rectangle(
                self.visualized_image,
                (i * section_width, 0),
                ((i + 1) * section_width - 1, height - 1),
                (0, 0, 0),
                20
            )

            # Add text annotation for non-white area percentage
            cv2.putText(
                self.visualized_image,
                f"Sec {i+1}: {non_white_area_percentage:.1f}%",
                (i * section_width + section_width // 4, height // 2),
                cv2.FONT_HERSHEY_SIMPLEX, 
                12,
                (0, 0, 255),
                50,
                cv2.LINE_AA
            )

    def save_visualization(self, filename="thresholded_image_with_sections.png"):
        """
        Saves the visualization image highlighting the sections and their corresponding 
        spray coverage percentages.

        Parameters:
            filename (str): Filename for saving the analyzed image visualization.
        """
        output_path = self.image_path.replace(".jpeg", f"_analyzed.jpeg")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        plt.figure(figsize=(10, 2))
        plt.title("Spray Coverage percentage in each section", fontsize=10)
        plt.imshow(cv2.cvtColor(self.visualized_image, cv2.COLOR_BGR2RGB))
        plt.axis("off")
        plt.savefig(
            output_path,
            dpi=400,
            bbox_inches="tight",
            pad_inches=0
        )

spray_card_path = "/Users/navjotsingh/Documents/spray_card_analysis/spray_card_images/_BN187 Full Res.jpeg"
analyzer = SprayCardAnalyzer(spray_card_path)
analyzer.convert_to_grayscale()
analyzer.apply_threshold()
analyzer.analyze_sections()
analyzer.save_visualization()

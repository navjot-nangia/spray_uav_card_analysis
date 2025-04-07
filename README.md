
# Spray Card Analyzer

This script analyzes spray cards by dividing an image into vertical sections and calculating the percentage of sprayed (non-white) areas within each section. It also generates a visualization highlighting the sprayed area percentages.

## Features
- Converts color images to grayscale.
- Uses Otsu's thresholding method for accurate spray coverage detection.
- Divides the image into customizable vertical sections.
- Calculates and annotates each section with its spray coverage percentage.
- Saves a visual representation of analysis results.

## Usage

1. Update the `spray_card_path` variable with the path to your spray card image:

```python
spray_card_path = "/path/to/your/spray_card_image.jpeg"
```

2. Run the script:

```bash
python spray_card_analyzer.py
```

The analyzed visualization image will be saved automatically in the same directory as your original image, with `_analyzed.jpeg` appended to the filename.

## Author

Navjot Singh

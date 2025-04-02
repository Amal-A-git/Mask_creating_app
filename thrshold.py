import streamlit as st
from PIL import Image
import numpy as np
import io
import os

def crop_image(image, crop_height):
    """Crop the image horizontally from the bottom."""
    width, height = image.size
    cropped_height = max(0, height - crop_height)
    return image.crop((0, 0, width, cropped_height))

def create_mask(image, threshold):
    """Convert image to grayscale and apply threshold."""
    gray = image.convert("L")
    mask = np.array(gray) > (threshold * 255)
    return Image.fromarray((mask * 255).astype(np.uint8))

def main():
    st.title("Image Mask Generator with Cropping")
    st.markdown("Upload images, crop them horizontally from the bottom, adjust threshold to generate binary masks.")

    # Sidebar controls
    with st.sidebar:
        threshold = st.slider("Mask Threshold", 
                               min_value=0.0, 
                               max_value=1.0, 
                               value=0.18,
                               step=0.01,
                               help="Adjust sensitivity for mask generation")
        crop_height = st.slider("Crop Height (pixels)", 
                                min_value=0, 
                                max_value=1000, 
                                value=50,
                                step=10,
                                help="Crop the image horizontally from the bottom")

    # Image upload section
    uploaded_files = st.file_uploader("Upload Images", 
                                      type=["png", "jpg", "jpeg","tif"],
                                      accept_multiple_files=True)

    if uploaded_files:
        for uploaded_file in uploaded_files:
            col1, col2 = st.columns(2)
            
            with col1:
                # Display original image
                image = Image.open(uploaded_file)
                st.image(image, caption="Original Image", use_column_width=True)
            
            with col2:
                # Crop and generate mask
                cropped_image = crop_image(image, crop_height)
                mask = create_mask(cropped_image, threshold)
                
                # Display cropped image and mask
                st.image(cropped_image, caption=f"Cropped Image (Height: {image.height - crop_height}px)", use_column_width=True)
                st.image(mask, caption=f"Mask (Threshold: {threshold:.2f})", use_column_width=True)
                
                # Create folders if not exist
                os.makedirs("cropped_images", exist_ok=True)
                os.makedirs("masks", exist_ok=True)
                
                # Save cropped image in 'cropped_images' folder
                cropped_path = os.path.join("cropped_images", uploaded_file.name)
                cropped_image.save(cropped_path)
                
                # Save mask in 'masks' folder
                mask_path = os.path.join("masks", uploaded_file.name)
                mask.save(mask_path)
                
                # Download button for cropped image
                with open(cropped_path, "rb") as cropped_file:
                    st.download_button(
                        label="Download Cropped Image",
                        data=cropped_file,
                        file_name=uploaded_file.name,
                        mime="image/png",
                        key=f"cropped_{uploaded_file.name}"
                    )
                
                # Download button for mask
                with open(mask_path, "rb") as mask_file:
                    st.download_button(
                        label="Download Mask",
                        data=mask_file,
                        file_name=uploaded_file.name,
                        mime="image/png",
                        key=f"mask_{uploaded_file.name}"
                    )

if __name__ == "__main__":
    main()

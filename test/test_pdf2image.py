import pdf2image

def test_convert_from_path():
    # ✅ remove the extra quotes
    images = pdf2image.convert_from_path(r"C:/Users/NamNamNam/Downloads/JD- AI Dev (Python).pdf")
    
    # ✅ save each page
    for i, image in enumerate(images):
        image.save(f"output_page_{i+1}.png", "PNG")

test_convert_from_path()

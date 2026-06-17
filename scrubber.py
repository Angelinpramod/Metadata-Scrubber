from PIL import Image, ExifTags
import os
import argparse
from pypdf import PdfReader, PdfWriter

def analyze_metadata(exif_data, gps_data):
    warnings = []
    if gps_data:
        warnings.append("GPS Location detected! Privacy risk!")
    for tag_id, value in exif_data.items():
        tag_name = ExifTags.TAGS.get(tag_id, tag_id)
        if tag_name in ["Make", "Model"]:
            warnings.append(f"Device info found: {tag_name} = {value}")
        if tag_name == "Software":
            warnings.append(f"Software info found: {value}")
        if tag_name == "DateTime":
            warnings.append(f"Timestamp found: {value}")
        if tag_name in ["Author", "Artist"]:
            warnings.append(f"Author info found: {value}")
    return warnings

def clean_metadata(input_path):
    img = Image.open(input_path)
    clean = Image.new(img.mode, img.size)
    clean.putdata(list(img.getdata()))
    name, ext = os.path.splitext(input_path)
    output_path = f"{name}_cleaned{ext}"
    clean.save(output_path)
    print(f"Cleaned file saved as: {output_path}")
    return output_path

def main():
    parser = argparse.ArgumentParser(
        description="🔍 MetaScrubber — Metadata Detection & Removal Tool"
    )
    parser.add_argument("--input",   required=True, help="Path to input file")
    parser.add_argument("--analyze", action="store_true", help="Analyze metadata")
    parser.add_argument("--clean",   action="store_true", help="Clean metadata")
    parser.add_argument("--output",  help="Custom output path (optional)")
    
    args = parser.parse_args()
    
    detect_and_process(args.input, analyze=args.analyze, clean=args.clean)
    
    # Step 1 - Open image using args
    image = Image.open(args.input)
    exif_data = image.getexif()
    gps_data = exif_data.get_ifd(34853)
    
    # Step 2 - If --analyze flag passed
    if args.analyze:
        print("\n EXTRACTING METADATA...")
        for tag_id, value in exif_data.items():
            tag_name = ExifTags.TAGS.get(tag_id, tag_id)
            print(f"{tag_name:25} : {value}")
        for tag_id, value in gps_data.items():
            gps = ExifTags.GPSTAGS.get(tag_id, tag_id)
            print(f"{gps:25} : {value}")
        
        warnings = analyze_metadata(exif_data, gps_data)
        if warnings:
            print("\nTHREAT ANALYSIS REPORT")
            print("-" * 40)
            for warning in warnings:
                print(warning)
        else:
            print("No sensitive metadata found!")
    
    # Step 3 - If --clean flag passed
    if args.clean:
        print("\n Starting sanitization...")
        cleaned_path = clean_metadata(args.input)
        
        # Verify
        print("\nVerifying...")
        cleaned_image = Image.open(cleaned_path)
        cleaned_exif = cleaned_image.getexif()
        if not cleaned_exif:
            print("VERIFICATION PASSED — Zero metadata found!")
        else:
            print(f"WARNING — {len(cleaned_exif)} fields still present!")
    
    # Step 4 - If neither flag passed
    if not args.analyze and not args.clean :
        print("Please specify --analyze or --clean")
        print("Example: python3 scrubber.py --input photo.jpg --analyze --clean")

def extract_pdf_metadata(input_path):
    reader = PdfReader(input_path)
    metadata = reader.metadata
    
    print("\n PDF METADATA:")
    print("-" * 40)
    for key, value in metadata.items():
        print(f"{key:25} : {value}")
    
    warnings = []
    sensitive = ["/Author", "/Creator", "/Producer"]
    
    for field in sensitive:
        if sensitive in metadata:   
            warnings.append(f"Sensitive field found: {field} = {metadata[field]}")
    
    if warnings:
        print("\n PDF THREAT REPORT ")
        print("-" * 40)
        for w in warnings:
            print(w)
    
    return metadata

def clean_pdf_metadata(input_path):
    reader = PdfReader(input_path)
    writer = PdfWriter()
    
 
    for page in reader.pages:
        writer.add_page(page)
        
    writer.add_metadata({})
    
    name, ext = os.path.splitext(input_path)
    output_path = f"{name}_cleaned{ext}"
    
    with open(output_path, "wb") as f:
        writer.write(f)
    
    print(f"Cleaned PDF saved as: {output_path}")
    return output_path
    
if __name__ == "__main__":
    main()

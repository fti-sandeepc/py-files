import os
import time
import json
import boto3


base_folder = "/home/sandip/Downloads/data1" 
bucket_name = "sandy-s3-a" 
aws_access_key_id = "AKIA3U7N46YG52KLM7"
aws_secret_access_key = "TXWNcpFe7Kp66I9NJW2b5biWo9nrJodLMAd1x"
aws_region = "us-east-1"


s3 = boto3.client("s3", aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=aws_region)

def create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path, exist_ok=True)

def create_s3_folder_if_not_exists(folder_name):
    try:
        s3.head_object(Bucket=bucket_name, Key=f"{folder_name}/")
    except:
        s3.put_object(Bucket=bucket_name, Key=f"{folder_name}/")

def upload_file_to_s3(file_path, folder_name):
    try:
        file_name = os.path.basename(file_path)
        s3_key = f"{folder_name}/{file_name}"
        s3.upload_file(file_path, bucket_name, s3_key)
        s3_url = f"https://{bucket_name}.s3.amazonaws.com/{s3_key}"
        print(f"Uploaded file {file_name} to S3 bucket in folder {folder_name}.")
        return s3_url
    except Exception as e:
        print(f"Error uploading file {file_name} to S3: {e}")
        return None

def create_metadata_file(file_path, folder_name, s3_url):
    try:
        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)
        file_type = file_name.split(".")[-1]
        metadata = {
            "file_name": file_name,
            "file_size": file_size,
            "file_type": file_type,
            "upload_location": s3_url
        }
        metadata_folder = os.path.join(base_folder, "meta-data")
        create_folder_if_not_exists(metadata_folder)
        metadata_file_path = os.path.join(metadata_folder, f"{file_name}.json")
        with open(metadata_file_path, "w") as metadata_file:
            json.dump(metadata, metadata_file)
        print(f"Created metadata file for {file_name}.")
    except Exception as e:
        print(f"Error creating metadata file for {file_name}: {e}")

def delete_file(file_path):
    try:
        os.remove(file_path)
        print(f"Deleted file {os.path.basename(file_path)} from the local folder.")
    except Exception as e:
        print(f"Error deleting file {os.path.basename(file_path)}: {e}")

def monitor_data_folder():
    """
    Monitors the 'data' folder and uploads new files to S3.
    """
    print("Monitoring 'data' folder for new files...")

    texts_folder = os.path.join(base_folder, "texts")
    images_folder = os.path.join(base_folder, "images")
    videos_folder = os.path.join(base_folder, "videos")
    metadata_folder = os.path.join(base_folder, "meta-data")

    create_folder_if_not_exists(texts_folder)
    create_folder_if_not_exists(images_folder)
    create_folder_if_not_exists(videos_folder)
    create_folder_if_not_exists(metadata_folder)

    create_s3_folder_if_not_exists("texts")
    create_s3_folder_if_not_exists("images")
    create_s3_folder_if_not_exists("videos")

    uploaded_text_files = set()
    uploaded_image_files = set()
    uploaded_video_files = set()

    while True:
        # Sleep for a while before checking again
        time.sleep(5)

        # Process files in 'texts' folder
        for file in os.listdir(texts_folder):
            if file not in uploaded_text_files:
                file_path = os.path.join(texts_folder, file)
                s3_url = upload_file_to_s3(file_path, "texts")
                if s3_url:
                    create_metadata_file(file_path, "texts", s3_url)
                    delete_file(file_path)
                    uploaded_text_files.add(file)

        # Process files in 'images' folder
        for file in os.listdir(images_folder):
            if file not in uploaded_image_files:
                file_path = os.path.join(images_folder, file)
                s3_url = upload_file_to_s3(file_path, "images")
                if s3_url:
                    create_metadata_file(file_path, "images", s3_url)
                    delete_file(file_path)
                    uploaded_image_files.add(file)

        # Process files in 'videos' folder
        for file in os.listdir(videos_folder):
            if file not in uploaded_video_files:
                file_path = os.path.join(videos_folder, file)
                s3_url = upload_file_to_s3(file_path, "videos")
                if s3_url:
                    create_metadata_file(file_path, "videos", s3_url)
                    delete_file(file_path)
                    uploaded_video_files.add(file)
                    
                    
monitor_data_folder()

import os

def get_folder_size(folder_path):
    total_size = 0
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            total_size += os.path.getsize(file_path)
    return total_size

def insertion_sort(folders):
    for i in range(1, len(folders)):
        key = folders[i]
        j = i - 1
        while j >= 0 and folders[j][1] > key[1]:
            folders[j + 1] = folders[j]
            j -= 1
        folders[j + 1] = key

def initialize_buckets(folders):
    if len(folders) == 0:
        return [], 0, 0

    max_size = max(folders, key=lambda x: x[1])[1]
    min_size = min(folders, key=lambda x: x[1])[1]

    bucket_count = len(folders)
    bucket_range = (max_size - min_size) / bucket_count
    buckets = [[] for _ in range(bucket_count)]

    return buckets, min_size, bucket_range

def distribute_folders_to_buckets(folders, buckets, min_size, bucket_range):
    bucket_count = len(buckets)
    
    for folder in folders:
        index = int((folder[1] - min_size) / bucket_range)
        if index >= bucket_count:
            index = bucket_count - 1
        buckets[index].append(folder)

def bucket_sort(folders):
    buckets, min_size, bucket_range = initialize_buckets(folders)
    distribute_folders_to_buckets(folders, buckets, min_size, bucket_range)
        
    sorted_folders = []
    for bucket in buckets:
        sorted_folders.extend(bucket)
    
    return sorted_folders, buckets, min_size, bucket_range

def get_folders_with_sizes(folder_path):
    folders = []
    for foldername in os.listdir(folder_path):
        folder_full_path = os.path.join(folder_path, foldername)
        if os.path.isdir(folder_full_path):
            folder_size = get_folder_size(folder_full_path)
            folders.append((foldername, folder_size))
    return folders

def sort_folders_by_size(folder_path):
    folders = get_folders_with_sizes(folder_path)
    sorted_folders, buckets, min_size, bucket_range = bucket_sort(folders)
    
    insertion_sort(sorted_folders)
    
    return sorted_folders, buckets, min_size, bucket_range

def save_buckets_to_txt(buckets, min_size, bucket_range, output_file_path):
    with open(output_file_path, 'w', encoding='utf-8') as file:
        for i, bucket in enumerate(buckets):
            lower_bound = min_size + i * bucket_range
            upper_bound = lower_bound + bucket_range
            file.write(f"Bucket {i} (Range: {lower_bound:.2f} - {upper_bound:.2f} bytes):\n")
            file.write("Unsorted:\n")
            for foldername, size in bucket:
                file.write(f"  {foldername}: {size} bytes\n")
            
            sorted_bucket = sorted(bucket, key=lambda x: x[1])
            file.write("\nSorted:\n")
            for foldername, size in sorted_bucket:
                file.write(f"  {foldername}: {size} bytes\n")
            
            file.write("\n")

def save_sorted_folders_to_txt(sorted_folders, output_file_path):
    with open(output_file_path, 'w', encoding='utf-8') as file:
        for foldername, size in sorted_folders:
            file.write(f"{foldername}: {size} bytes\n")

if __name__ == "__main__":
    folder_path = r'C:\Perkuliahan'
    sorted_folders, buckets, min_size, bucket_range = sort_folders_by_size(folder_path)

    for foldername, size in sorted_folders:
        print(f"{foldername}: {size} bytes")

    sorted_output_file_path = "sorted_folders.txt"
    save_sorted_folders_to_txt(sorted_folders, sorted_output_file_path)
    print(f"Sorted folder list saved to {sorted_output_file_path}")

    buckets_output_file_path = "buckets_details.txt"
    save_buckets_to_txt(buckets, min_size, bucket_range, buckets_output_file_path)
    print(f"Buckets details saved to {buckets_output_file_path}")

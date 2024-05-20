import os

def insertion_sort(files):
    for i in range(1, len(files)):
        key = files[i]
        j = i - 1
        while j >= 0 and files[j][1] > key[1]:
            files[j + 1] = files[j]
            j -= 1
        files[j + 1] = key

def initialize_buckets(files):
    if len(files) == 0:
        return [], 0, 0

    # Menemukan ukuran minimum dan maksimum untuk menentukan kisaran ukuran file
    max_size = max(files, key=lambda x: x[1])[1]
    min_size = min(files, key=lambda x: x[1])[1]

    # Membuat bucket dengan rentang yang sesuai
    bucket_count = len(files)
    bucket_range = (max_size - min_size) / bucket_count
    buckets = [[] for _ in range(bucket_count)]

    return buckets, min_size, bucket_range

def distribute_files_to_buckets(files, buckets, min_size, bucket_range):
    bucket_count = len(buckets)
    
    # Mendistribusikan file ke dalam bucket berdasarkan ukurannya
    for file in files:
        index = int((file[1] - min_size) / bucket_range)
        if index >= bucket_count:
            index = bucket_count - 1  # Memastikan file berukuran maksimal masuk ke bucket terakhir
        buckets[index].append(file)

def bucket_sort(files):
    buckets, min_size, bucket_range = initialize_buckets(files)
    distribute_files_to_buckets(files, buckets, min_size, bucket_range)
        
    # Menggabungkan file di setiap bucket (file belum terurut)
    sorted_files = []
    for bucket in buckets:
        sorted_files.extend(bucket)
    
    return sorted_files, buckets, min_size, bucket_range

def get_files_with_sizes(folder_path):
    files = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            file_size = os.path.getsize(file_path)
            files.append((filename, file_size))
    return files

def sort_files_by_size(folder_path):
    files = get_files_with_sizes(folder_path)
    sorted_files, buckets, min_size, bucket_range = bucket_sort(files)
    
    # Mengurutkan file menggunakan insertion sort setelah pengurutan bucket
    insertion_sort(sorted_files)
    
    return sorted_files, buckets, min_size, bucket_range

def save_buckets_to_txt(buckets, min_size, bucket_range, output_file_path):
    with open(output_file_path, 'w', encoding='utf-8') as file:
        for i, bucket in enumerate(buckets):
            lower_bound = min_size + i * bucket_range
            upper_bound = lower_bound + bucket_range
            file.write(f"Bucket {i} (Range: {lower_bound:.2f} - {upper_bound:.2f} bytes):\n")
            file.write("Unsorted:\n")
            for filename, size in bucket:
                file.write(f"  {filename}: {size} bytes\n")
            
            # Mengambil bucket yang telah diurutkan
            sorted_bucket = sorted(bucket, key=lambda x: x[1])
            file.write("\nSorted:\n")
            for filename, size in sorted_bucket:
                file.write(f"  {filename}: {size} bytes\n")
            
            file.write("\n")


def save_sorted_files_to_txt(sorted_files, output_file_path):
    with open(output_file_path, 'w', encoding='utf-8') as file:
        for filename, size in sorted_files:
            file.write(f"{filename}: {size} bytes\n")

if __name__ == "__main__":
    folder_path = r'C:\Users\USER\Downloads'
    sorted_files, buckets, min_size, bucket_range = sort_files_by_size(folder_path)

    # Menampilkan file yang telah terurut
    for filename, size in sorted_files:
        print(f"{filename}: {size} bytes")

    # Menyimpan tampilan file yang telah terurut di file txt
    sorted_output_file_path = "sorted_files_bucket_insertion.txt"
    save_sorted_files_to_txt(sorted_files, sorted_output_file_path)
    print(f"Sorted file list saved to {sorted_output_file_path}")

    # Menyimpan detail bucket ke dalam file txt
    buckets_output_file_path = "buckets_details_insertion.txt"
    save_buckets_to_txt(buckets, min_size, bucket_range, buckets_output_file_path)
    print(f"Buckets details saved to {buckets_output_file_path}")
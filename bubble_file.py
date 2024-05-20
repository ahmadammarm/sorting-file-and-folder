import os

def bubble_sort(files):
    n = len(files)
    for i in range(n):
        for j in range(0, n - i - 1):
            if files[j][1] > files[j + 1][1]:
                files[j], files[j + 1] = files[j + 1], files[j]

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
    bubble_sort(files)
    return files

def save_sorted_files_to_txt(sorted_files, output_file_path):
    with open(output_file_path, 'w', encoding='utf-8') as file:
        for filename, size in sorted_files:
            file.write(f"{filename}: {size} bytes\n")

if __name__ == "__main__":
    folder_path = r'C:\Users\USER\Downloads'
    sorted_files = sort_files_by_size(folder_path)

    # Menampilkan file yang sudah terurut
    for filename, size in sorted_files:
        print(f"{filename}: {size} bytes")

    # Menyimpan file yang sudah terurut ke dalam file txt
    sorted_output_file_path = "sorted_files_bubble.txt"
    save_sorted_files_to_txt(sorted_files, sorted_output_file_path)
    print(f"Sorted file list saved to {sorted_output_file_path}")

python3 LabelDataConverter.py -i [InputDirectory] -o [OutputDirectory] -m [Mode] -wd [WrongDirectory]

InputDirectory: Đường dẫn folder chứa dữ liệu nguồn (Images, Json file) Cấu trúc file có thể nhiều tầng
OutputDirectory: Đường dẫn folder cần lưu dữ liệu đầu ra
Mode: Chọn chức năng
        mode = 1  ===> Script chạy chức năng convert từ json sang data dạng txt
        mode = 2  ===> Script chạy chức năng filter từ txt file
WrongDirectory: Đường dẫn thư mục chứa các file images lalbe sai

(Tất cả các folder output không cần thiết phải tạo trước)


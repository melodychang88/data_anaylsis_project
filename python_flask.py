# import Flask, request, render_template
from flask import Flask, request, render_template
import os
from DM_digestibility_analysis import (
    read_csv,
    raw_data_to_dict,
    multiply_data,
    subtract_data,
    calculate_DM_digestibility,
)

# bulit application object
app = Flask(__name__)

# create a dict, the filename use as the key and file_path use as the value
file_path_dict = {}


# create route"/" and reponse to function upload_file()
# http allow GET and POST method
@app.route("/", methods=["GET", "POST"])
def upload_file():
    # upload_successful default is False
    upload_successful = False
    # define filepath_dict to global varible
    global file_path_dict
    # if client use POST method to request server
    if request.method == "POST":
        #
        uploaded_file_list = request.files.getlist("file")

        for uploaded_file in uploaded_file_list:
            uploaded_file_name = uploaded_file.filename
            file_path = os.path.join(app.config["file_uploads"], uploaded_file_name)
            uploaded_file.save(file_path)
            file_path_dict[uploaded_file_name] = file_path

        if uploaded_file_list is not None:
            # 上傳成功
            upload_successful = True
        else:
            upload_successful = False

    if upload_successful:
        return render_template("index2.html")
    else:
        return render_template("index.html")


app.config[
    "file_uploads"
] = "C:\\Users\\melod\\OneDrive\\data_analysis_project\\file_upload"


# 處理路徑 /show_data 的對應函式
@app.route("/show_data")
def show_data():
    file_csv_dict = {}
    for file_name, file_path in file_path_dict.items():
        file_csv = read_csv(file_path)
        file_csv_dict[file_name] = file_csv

    return render_template("show_data_page.html", data=file_csv_dict)


@app.route("/data_analysis")
def data_analysis():
    data_result_dict = {}
    for file_name, file_path in file_path_dict.items():
        file_csv = read_csv(file_path)
        data_dict = raw_data_to_dict(file_csv)
        data_multiply = multiply_data(
            data_dict, new_key="Diet_DM", key1="Diet_weight", key2="Diet_DM_percentage"
        )
        data_substract = subtract_data(
            data_dict,
            new_key="Digesta_weight",
            key1="Freeze_dry_weight",
            key2="Tube_weight",
        )
        data_result = calculate_DM_digestibility(data_multiply, data_substract)

        data_result_dict[file_name] = data_result
    return render_template("show_data_analysis_result.html", data=data_result_dict)


# 啟動網站伺服器，可透過"port"參數指定port
app.run(host="0.0.0.0", port=3000)

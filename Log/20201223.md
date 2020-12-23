Vị trí: The Zero Coffee
Ngày: 23/12/2020

Nội dung:
    - Ghi lại description của model:
        + State: chứa thông tin CO2_Air, CO2_Top, VP_Air, VP_Top, những thông số output dự báo thông qua solver của GreenHouseModel.
        + Parameters: thông số mô tả của một GreenHouse, không thay đổi theo thời gian, truyền Parameter vào Contructor của GreenHouseModel lúc khởi tạo model.
        + SetPoint: thông số có thể thay đổi trong quá trình vận hành của GreenHouseModel (theo thời gian), để điều chỉnh mức độ ảnh hưởng của các thành phần trong GreenHouseModel, được truyền vào mỗi lần dự đoán state tiếp theo.(Note: có thể dùng để bật tắt các thành phần trong model).
        + Constant: các hằng số tự nhiên được sử dụng trong model.
        + Environment: điều kiện Môi trường của GreenHouseModel có thể thay đổi theo thời gian, chứa các Nhiệt độ (T_Air, T_Top, ...), CO2_out, VP_out, được truyền vào mỗi khi dự đoán state.
        + GreenHouse: Instance của nó đại diện cho một nhà kính cụ thể, mà với một bộ:
            _ Constant, Parameter: truyền vào khởi tạo Instance.
            _ Setpoint, Environment, State(hiện tại): truyền vào mỗi lúc dự đoán.
        cụ thể dự đoán được đạo hàm của State hiện tại.
    - Code lại Environment.
    - Chia nhiệm vụ tiếp theo:
            Bách, Thịnh, Toàn: 1a, 1b, 1c, 2a.
            Duy, Nguyên: 1d, 1e, 4a.
    * DEADLINE: 12PM: 26/12/2020.

    - Next meeting: 27/12/2020.
    - Fix CO2 model.

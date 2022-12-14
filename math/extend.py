def scal(data, sec_dis):
    """多边形等距缩放

    Args:
        data: 多边形按照逆时针顺序排列的的点集
        sec_dis: 缩放距离

    Returns:
        缩放后的多边形点集
    """
    num = len(data)
    scal_data = []
    for i in range(num):
        x1 = data[(i) % num][0] - data[(i - 1) % num][0]
        y1 = data[(i) % num][1] - data[(i - 1) % num][1]
        x2 = data[(i + 1) % num][0] - data[(i) % num][0]
        y2 = data[(i + 1) % num][1] - data[(i) % num][1]

        d_A = (x1 ** 2 + y1 ** 2) ** 0.5
        d_B = (x2 ** 2 + y2 ** 2) ** 0.5

        Vec_Cross = (x1 * y2) - (x2 * y1)

        sin_theta = Vec_Cross / (d_A * d_B)

        dv = sec_dis / sin_theta

        v1_x = (dv / d_A) * x1
        v1_y = (dv / d_A) * y1

        v2_x = (dv / d_B) * x2
        v2_y = (dv / d_B) * y2

        PQ_x = v1_x - v2_x
        PQ_y = v1_y - v2_y

        Q_x = data[(i) % num][0] + PQ_x
        Q_y = data[(i) % num][1] + PQ_y
        scal_data.append([Q_x, Q_y])
    return scal_data


#
# data = [[2.0056, 0.9829], [6.9787, 0.9829], [4.0369, 2.3365], [3.4765, 3.7834], [4.4571, 5.4871], [6.6986, 6.7706],
#         [2.6593, 6.7706]]

data = [
[.036, 0.685],
[-0.292, 0.748],
[-0.208, 0.608],
[-0.374, 0.595],
[-0.330, 0.465],
[-0.464, 0.468],
[-0.428, 0.412],
[-0.560, 0.395],
[-0.488, 0.310],
[-0.612, 0.243],
[-0.564, 0.190],
[-0.710, 0.060],
[-0.560, 0.038],
[-0.636, -0.192],
[-0.534, -0.145],
[-0.476, -0.417],
[-0.438, -0.303],
[-0.518, -0.562],
[-0.328, -0.705],
[-0.176, -0.680],
[-0.164, -0.405],
[.014, -0.625],
[.160, -0.565],
[.188, -0.368],
[.262, -0.308],
[.472, -0.485],
[.726, -0.640],
[.976, -0.515],
[.834, -0.228],
[.742, -0.233],
[.696, -0.072],
[.822, 0.123],
[.814, 0.282],
[.600, 0.222],
[.564, 0.438],
[.526, 0.632],
[.374, 0.635 ]

]

data1 = scal(data, 0.2)
for item in data1:
    print(item)

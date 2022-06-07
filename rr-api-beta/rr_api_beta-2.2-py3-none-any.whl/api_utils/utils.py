from api_utils.constants import Keys


def get_position(conn, query):
    data = conn.get_data(query=query)[0]
    if data:
        return data[0][0].replace("[", '').replace("]", '').replace("'", '')
    return 'Not found data.'


def get_mv_data(data):
    age = '-'
    mv = '-'
    mv_type = '-'
    try:
        mv = data.mv.values[0]
        if mv:
            mv = int(mv)
        mv_type = data.mv_type.values[0]
        if mv_type:
            mv_type = mv_type.replace('.00', '')
        age = data.age.values[0]
        if age:
            age = int(age)

    except Exception as e:
        e
    return {Keys.AGE: age, Keys.MARKET_VALUE: mv, Keys.MARKET_VALUE_TYPE: mv_type}

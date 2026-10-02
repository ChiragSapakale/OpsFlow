def validate_required_columns(df, required_columns):
    missing_columns = []

    for column in required_columns:
        if column not in df.columns:
            missing_columns.append(column)

    return missing_columns

def find_missing_required_values(df, required_columns):
    invalid_rows = df[df[required_columns].isnull().any(axis=1)]

    return invalid_rows

def find_negative_values(df, columns):
    invalid_rows = df[(df[columns] < 0).any(axis=1)]

    return invalid_rows
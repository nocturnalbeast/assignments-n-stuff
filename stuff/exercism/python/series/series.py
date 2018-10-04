def slices(series, length):
    if (len(series) == 0) | (length <= 0) | (len(series) < length):
    	raise ValueError("Error!")
    se_list = []
    for i in range(len(series)-length+1):
    	se_list.append(series[i:i+length:])
    return se_list
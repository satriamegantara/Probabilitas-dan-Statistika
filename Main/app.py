from flask import Flask, render_template, request
import pandas as pd

data = pd.read_csv('tes.csv')

app = Flask(__name__)

def filter_pemain(game):
    filtered_data = data[data['game'] == game]
    if filtered_data.empty:
        return []
    players = []
    for idx, row in enumerate(filtered_data.iterrows(), start=1):
        _, row_data = row   
        players.append({
            'no': idx,
            'nama': row_data['name'],
            'lokasi': row_data['location'],
            'gender': row_data['gender'],
            'usia': row_data['age']
        })
    ages = filtered_data['age'].tolist()
    return players, ages

def bubbleSort(arr):
    n = len(arr)
    for i in range(n):
        swapped = False

        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                swapped = True
    return arr

def hitung_total(numbers):
    total = 0
    for i in numbers:
        total += i
    return total

def hitung_min_max(numbers):
    min_val = numbers[0]
    max_val = numbers[0]
    for num in numbers:
        if num < min_val:
            min_val = num
        if num > max_val:
            max_val = num
    return min_val, max_val

def hitung_mean(numbers):
    total = hitung_total(numbers)
    count = 0
    for _ in numbers:
        count += 1
    return round(total / count, 2)

def hitung_median(numbers):
    count = 0
    for _ in numbers:
        count += 1
    
    sorted_numbers = bubbleSort(numbers.copy())
    
    if count % 2 == 0:
        median = (sorted_numbers[count//2 - 1] + sorted_numbers[count//2]) / 2
    else:
        median = sorted_numbers[count//2]
    
    return round(median, 2)

def hitung_mode(numbers):
    frequency = {}
    for num in numbers:
        if num in frequency:
            frequency[num] += 1
        else:
            frequency[num] = 1
    
    max_frequency = 0
    mode = numbers[0]
    for num, freq in frequency.items():
        if freq > max_frequency:
            max_frequency = freq
            mode = num
    
    return mode

def hitung_std_dev(numbers, mean):
    count = 0
    variance_sum = 0
    for num in numbers:
        count += 1
        variance_sum += (num - mean) ** 2
    
    return round((variance_sum / count) ** 0.5, 2)

def persentile(data, p):
    count = 0
    for _ in data:
        count += 1
    
    position = (count - 1) * (p / 100)
    floor_position = int(position)
    ceil_position = floor_position + 1
    
    if ceil_position >= count:
        return data[floor_position]
    
    if floor_position == position:
        return data[floor_position]
    else:
        return data[floor_position] + (data[ceil_position] - data[floor_position]) * (position - floor_position)

def statistik(ages):
    if not ages:
        return {
            'mean': None, 'median': None, 'mode': None, 'min': None, 'max': None, 
            'total': 0, 'sorted_ages': [], 'std_dev': None, 'range': None, 
            'mid_range': None, 'q1': None, 'q2': None, 'q3': None, 'iqr': None
        }
    
    sorted_ages = bubbleSort(ages.copy())
    
    mean = hitung_mean(sorted_ages)
    median = hitung_median(sorted_ages)
    mode = hitung_mode(sorted_ages)
    min_age, max_age = hitung_min_max(sorted_ages)
    std_dev = hitung_std_dev(sorted_ages, mean)
    
    count = 0
    for i in sorted_ages:
        count += 1
    
    range_val = max_age - min_age if (max_age is not None and min_age is not None) else None
    mid_range = round((min_age + max_age) / 2, 2) if (min_age is not None and max_age is not None) else None
    
    q1 = round(persentile(sorted_ages, 25), 2) if count > 0 else None
    q2 = round(persentile(sorted_ages, 50), 2) if count > 0 else None
    q3 = round(persentile(sorted_ages, 75), 2) if count > 0 else None
    iqr = round(q3 - q1, 2) if (q1 is not None and q3 is not None) else None
    
    stats = {
        'mean': mean, 'median': median, 'mode': mode, 'min': min_age, 
        'max': max_age, 'total': count, 'sorted_ages': sorted_ages, 
        'std_dev': std_dev, 'range': range_val, 'mid_range': mid_range, 
        'q1': q1, 'q2': q2, 'q3': q3, 'iqr': iqr
    }
    return stats

@app.route('/', methods=['GET', 'POST'])
def home():
    players = None
    stats = None
    game = None
    if request.method == 'POST':
        game = request.form['game']
        players, ages = filter_pemain(game)
        stats = statistik(ages)
    return render_template('index1.html', players=players, stats=stats, game=game)

if __name__ == '__main__':
    app.run(debug=True)
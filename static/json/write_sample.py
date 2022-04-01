import json

def writeSample():
    with open('chart_data_sample.json', 'r') as f:
        chartData = json.load(f)
        
    with open('chart_data.json', 'w') as f:
        json.dump(chartData, f)
    
if __name__ == '__main__':
    writeSample()
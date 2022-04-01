import json

def clearData():
    emptyData = {'imgSize': [], 'PSNR': [], 'SSIM': []}
        
    with open('chart_data.json', 'w') as f:
        json.dump(emptyData, f)
    
if __name__ == '__main__':
    clearData()
# coding:utf-8
 
from flask import Flask, render_template, request, redirect, url_for, make_response,jsonify
from werkzeug.utils import secure_filename
import os
import cv2
import time
import json
import math
import PSNR
import SSIM
 
from datetime import timedelta
 
#设置允许的文件格式
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp', 'BMP'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
 
app = Flask(__name__)
# 设置静态文件缓存过期时间
app.send_file_max_age_default = timedelta(seconds=1)
 

@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')

@app.route('/encode', methods=['POST', 'GET'])
def encode():
    import encoder_main
    encoder_main.main()
    return render_template('index.html')

@app.route('/decode', methods=['POST', 'GET'])
def decode():
    import decoder_main
    decoder_main.main()
    return render_template('index.html')

@app.route('/analyze', methods=['POST', 'GET'])
def analyze():
    if request.method == 'POST':
        img1 = request.files['img1']
        img2 = request.files['img2']
        
        if not (img1 and img2):
            return render_template('analyze.html', msg="请上传两张图片！")
            
        ext1 = img1.filename.split('.')[1]
        ext2 = img2.filename.split('.')[1]            
            
        if not (ext1 == ext2 and allowed_file(img1.filename) and allowed_file(img2.filename)):
            return render_template('analyze.html', msg="请检查上传的图片类型！两张图片扩展名需相同且仅限于 .png .jpg .bmp")

        basepath = os.path.dirname(__file__)  # 当前文件所在路径
        
        upload_path1 = os.path.join(basepath, 'static/images', secure_filename('img1.'+ ext1))
        upload_path2 = os.path.join(basepath, 'static/images', secure_filename('img2.'+ ext2))  
        
        img1.save(upload_path1)
        img2.save(upload_path2)
 
        # 使用OpenCV转换一下图片格式和名称
        img1 = cv2.imread(upload_path1)
        img2 = cv2.imread(upload_path2)
        
        if not (img1.shape[0] == img2.shape[0] and img1.shape[1] == img2.shape[1]):
            return render_template('analyze.html', msg="两张图片尺寸需相同!")
        
        res1 = str(img1.shape[0]) + " x " + str(img1.shape[1])
        res2 = round(PSNR.psnr(img1, img2), 3)
        res3 = round(SSIM.ssim(img1, img2), 3)
        
        with open('static/json/chart_data.json', 'r') as f:
            chartData = json.load(f)
        
        chartData['imgSize'].insert(0,res1)
        chartData['PSNR'].insert(0,res2)
        chartData['SSIM'].insert(0,res3)
        
        while(len(chartData['imgSize']) > 10):
            chartData['imgSize'].pop()      
        while(len(chartData['PSNR']) > 10):
            chartData['PSNR'].pop()
        while(len(chartData['SSIM']) > 10):
            chartData['SSIM'].pop()
        
        with open('static/json/chart_data.json', 'w') as f:
            json.dump(chartData, f)
        
        return render_template('analyzed.html', timestamp=time.time(), ext=ext1, imgSize=res1, psnr=res2, ssim=res3)
 
    return render_template('analyze.html')
 
@app.route('/echart', methods=['POST', 'GET'])
def echart():
    if (request.method == 'POST' and request.form.get('clear')=='清空记录'):
        emptyData = {'imgSize': [], 'PSNR': [], 'SSIM': []}
        with open('static/json/chart_data.json', 'w') as f:
            json.dump(emptyData, f)
        return render_template(
                'echart.html',
                psnrData=[],
                ssimData=[],
                minYAxis=0,
                maxYAxis=4
            )
        
    with open('static/json/chart_data.json', 'r') as f:
        chartData = json.load(f)
    
    minPsnr=maxPsnr=2
    
    if not(len(chartData['PSNR'])==0):
        psnrDataSorted=sorted(chartData['PSNR'])
        
        for val in psnrDataSorted:
            if(val!=float('inf')):
                minPsnr=val
                break
    
        for val in reversed(psnrDataSorted):
            if(val!=float('inf')):
                maxPsnr=val
                break
   
    return render_template(
            'echart.html',
            psnrData=chartData['PSNR'],
            ssimData=chartData['SSIM'],
            minYAxis=math.floor(minPsnr-2),
            maxYAxis=math.floor(maxPsnr+2)
        )

@app.route('/intro', methods=['POST', 'GET'])
def intro():
    return render_template('intro.html')

@app.route('/intro2', methods=['POST', 'GET'])
def intro2():
    return render_template('intro2.html')

@app.route('/effect', methods=['POST', 'GET'])
def effect():
    if request.method == 'POST':
        for index in range(1,7):
            if(request.form.get('effect'+str(index))):
                with open('static/json/effect_data'+str(index)+'.json', 'r') as f:
                    chartData = json.load(f)
                minPsnr=maxPsnr=2
                
                if not(len(chartData['PSNR'])==0):
                    psnrDataSorted=sorted(chartData['PSNR'])
                    
                    for val in psnrDataSorted:
                        if(val!=float('inf')):
                            minPsnr=val
                            break
                
                    for val in reversed(psnrDataSorted):
                        if(val!=float('inf')):
                            maxPsnr=val
                            break

                return render_template(
                    'effect_chart.html',
                    psnrData=chartData['PSNR'],
                    ssimData=chartData['SSIM'],
                    xAxis=chartData['xAxis'],
                    imgSize=chartData['imgSize'][0],
                    minYAxis=math.floor(minPsnr-2),
                    maxYAxis=math.floor(maxPsnr+2)
                )
    return render_template('effect_index.html')

if __name__ == '__main__':
    # app.debug = True
    app.run(host='0.0.0.0', port=8987, debug=True)
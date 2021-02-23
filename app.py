import os
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
import joblib
import base64

app = Flask(__name__)
api = Api(app)


class MakePrediction(Resource):
    @staticmethod
    def post():
        posted_data = request.get_json()
        posted_base64_image = posted_data['base64_image_stream']
        posted_base64_image_name = posted_data['base64_image_stream_imagename']
        imgdata = base64.b64decode(posted_base64_image)
        #print(imgdata)
        filename = os.path.join(os.path.dirname("requestedImage/"),posted_base64_image_name+".jpg")  
        with open(filename, 'wb') as f:
            f.write(imgdata)
        #print(filename)
        
        try:
            #print("python3 model/detect_mask_image.py --image " + filename)
            new_path_join = os.path.join(os.path.dirname('convertedImage/'), "rect_out_"+os.path.basename(filename))
            os.system('python3 model/detect_mask_image.py --image '+ filename)
            with open(new_path_join, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read())
            ret_img_base64 = encoded_string
            #print(ret_img_base64)
        except:
            ret_img_base64 = "Failed"
        

        try:
            return jsonify({
            'IMAGE': ret_img_base64.decode()
            })
        except:
            return jsonify({
                'Process':"Failed"
            })


api.add_resource(MakePrediction, '/image')


if __name__ == '__main__':
    app.run(debug=True)
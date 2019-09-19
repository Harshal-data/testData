from tempfile import NamedTemporaryFile

import cv2
from flask import Flask
from gcloud import storage

client = storage.Client.from_service_account_json('/.json')
# specify google bucket name
bucket = client.get_bucket('hp_bucket-1')

app = Flask(__name__)
# api = Api(app)


@app.route("/capImg/<cus_id>")
def capture_image(cus_id):
    cam = cv2.VideoCapture(0)

    cv2.namedWindow("Capture")

    img_counter = 0

    while True:
        ret, frame = cam.read()
        cv2.imshow("Capture", frame)
        if not ret:
            break
        key_press = cv2.waitKey(1)

        if key_press % 256 == 27:
            # ESC press
            print("ESC key hit ..Closing")
            cam.release()
            cv2.destroyAllWindows()
            return "ESC key hit ..Closing"
            break
        elif key_press % 256 == 32:
            # SPACE hit
            with NamedTemporaryFile() as temp:
                # add JPEG format to the NamedTemporaryFile
                i_name = "".join([str(temp.name), ".jpg"])

            # img_name = "opencv_frame_{}.jpg".format(img_counter)
            # cv2.imwrite(img_name, frame)
            cv2.imwrite(i_name, frame)
            print("{} written!!".format(i_name))

            # Name of the file in the bucket
            blob = bucket.blob(i_name)
            # Type of file being uploaded
            blob.upload_from_filename(i_name, content_type='image/jpeg')

            img_counter += 1
            cam.release()
            cv2.destroyAllWindows()
            print("{} - image captured!!", cus_id)
            return "<input type=\"submit\" value=\"Submit\">"

    cam.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    app.run(debug=True)

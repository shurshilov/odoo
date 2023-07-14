# Copyright 2019 Artem Shurshilov
import classify
import cv2
import preprocess
import time
from scipy import misc

classifier = classify.Classify()
preprocessor = preprocess.PreProcessor()

cv2.namedWindow("Terminator EYE")
camera = cv2.VideoCapture(0)
i = 0
start = time.time()
while True:
    name = "NO FACE"
    return_value, image = camera.read()
    # cv2.imwrite('opencv'+str(i)+'.png', image)
    # bb = (preprocessor.align('opencv'+str(i)+'.png'))
    # сохраняем весь кадр
    cv2.imwrite("opencv.png", image)
    # детекстируем лицо с помощью mtcnn и сохраняем в temp.png
    bb = preprocessor.align("opencv.png")

    # рисуем прямоугольник на картинке
    # start_point , end_point, color, Line thickness of 5 px
    cv2.rectangle(image, (bb[0], bb[1]), (bb[2], bb[3]), (0, 255, 0), 5)
    # try:
    # непосредстенно сам поиск в FACE NET по натренированной сети распознование
    # name = classifier.predict('temp.png')

    # счетчик уникальних лиц (посетителей) по базе из папки
    min_dist = classifier.predict_db("temp.png", "db/")
    # если НЕ нашли лицо
    if preprocessor.filename == "1.png":
        name = "no face"
    # если лицо нашли и при этом база пустая, сохраняем фото
    elif min_dist == 100:
        name = "new"
        misc.imsave(preprocessor.filename, preprocessor.scaled)
    # если лицо нашли и при этом похожее есть в базе
    elif min_dist < 1:
        name = "old"
    # если лицо нашли и похоже в базе еще нет, добавляем
    else:
        name = "new"
        misc.imsave(preprocessor.filename, preprocessor.scaled)

    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(
        image,
        "FIND face: " + name,
        (50, 50),
        font,
        0.8,
        (0, 255, 0),
        2,
        cv2.LINE_AA,
    )
    cv2.imshow("Terminator EYE", image)
    # cv2.imwrite('opencv'+str(i)+'.png', image)
    # сохраняем только лицо
    cv2.imwrite("opencv.png", image)
    # except:
    #     continue
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    i += 1
end_time = time.time()
print(i / (end_time - start))

# When everything done, release the capture
camera.release()
cv2.destroyAllWindows()
print(classifier.predict("temp.png"))

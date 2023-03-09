import cv2
import numpy as np

class Road:
    
    def road(img: np.ndarray) -> np.ndarray:
        
    # В серый для контраста
        gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Размытие, чтобы удалить шум
        blur_gauss = cv2.GaussianBlur(img,(5,5),3)
    # Находим границы, что бы найти границы дороги
    # Параметры выбраны перебором
        edges = cv2.Canny(blur_gauss,100,200)
    # Создаем маску для выделения области    
        mask = np.zeros_like(edges)
        ignore_mask_color = 255  
    # Определяем область где должна находиться дорога
        imshape = img.shape
        vertices = np.array([[(0,imshape[0]),(500, 235), (400, 235), (imshape[1],imshape[0])]], dtype=np.int32)
        cv2.fillPoly(mask, vertices, ignore_mask_color)
        masked_edges = cv2.bitwise_and(edges, mask)
    # Параметры для поиска линий Хафа  
        rho = 5 # расстояние в пикселях сетки
        theta = np.pi/180 # угол
        threshold = 15     # минимальное пересечение
        min_line_length = 50 #минимальное число пикселей для линии
        max_line_gap = 40    # максимальный зазор в пикселях между соединяемыми отрезками линии
        line_image = np.copy(img)*0 # полотно для отрисовки
    
    
    # Находим линии    
        lines = cv2.HoughLinesP(masked_edges, rho, theta, threshold, np.array([]),
                                min_line_length, max_line_gap)
    
        # Перебераем линии и отрисовываем их
        points = []
        for line in lines:
            points.append(line[0][0:2])
            points.append(line[0][2:4])
            for x1,y1,x2,y2 in line:
                cv2.line(line_image,(x1,y1),(x2,y2),(120,0,120),30)
        
        lines_edges = cv2.addWeighted(img, 0.8, line_image, 100, 1)
        return  lines_edges
    

    def road_mask(img: np.ndarray) -> np.ndarray:
        # Маска для сокрытия всего кроме плоскости дороги
        
        gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur_gauss = cv2.GaussianBlur(img,(5,5),3)
        edges = cv2.Canny(blur_gauss,100,200)  
        mask = np.zeros_like(edges)
        ignore_mask_color = 255  

        imshape = img.shape
        vertices = np.array([[(0,imshape[0]),(500, 235), (400, 235), (imshape[1],imshape[0])]], dtype=np.int32)
        cv2.fillPoly(mask, vertices, ignore_mask_color)
        masked_edges = cv2.bitwise_and(edges, mask)   
        rho = 5 # расстояние в пикселях сетки
        theta = np.pi/180 # угол
        threshold = 15     # минимальное пересечение
        min_line_length = 50 #минимальное число пикселей для линии
        max_line_gap = 40    # максимальный зазор в пикселях между соединяемыми отрезками линии
        line_image = np.copy(img)*0 # полотно для отрисовки
        lines = cv2.HoughLinesP(masked_edges, rho, theta, threshold, np.array([]),
                                min_line_length, max_line_gap)
    
        # Перебераем линии и отрисовываем их
        points = []
        for line in lines:
            points.append(line[0][0:2])
            points.append(line[0][2:4])
            for x1,y1,x2,y2 in line:
                cv2.line(line_image,(x1,y1),(x2,y2),(120,0,120),30)
        
        lines_edges = cv2.addWeighted(img, 0.8, line_image, 100, 1)
        
        M =  np.ones(img.shape, dtype = "uint8")  
        pts = np.array(points, np.int32)
        a = cv2.polylines(M, [pts], True, (255,255,255), 150)
   
        subtracted = cv2.subtract(a, img) 
        return  subtracted


if __name__ == '__main__':
    video_name = 'trm.169.007.avi'
    cap = cv2.VideoCapture('trm.169.007.avi')
    while cap.isOpened():
        succeed, frame = cap.read()
        if succeed:
            frame = Road.road_mask(frame)
            cv2.imshow(video_name, frame)
        else:
            cv2.destroyAllWindows()
            cap.release()
        cv2.waitKey(1)
        
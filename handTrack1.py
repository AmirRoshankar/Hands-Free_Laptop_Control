import cv2
import numpy as np
import pickle
import random
from matplotlib import pyplot as plot
import pyautogui
import math
import time

#from object_tracker import startX, startY, endY, endX
hand_hist = None
traverse_point = []
total_rectangle = 16
hand_rect_one_x = None
hand_rect_one_y = None

hand_rect_two_x = None
hand_rect_two_y = None

have_background = False
background = None

defHands = []
newHands = []
lengthColec = []

cx = 200
cy = 200
bx = 200
by = 300
sx = 0
sy = 0





cropped = None

areaHand = 7000

startX = 0
endX = 0

width = 0
height = 0

startY = 0
endY = 0

backDivY = 10
backDivX = 17
backgroundHists = None

oldX = 0
oldY = 0
firstRun = 0
sameCount = 0

resetCount = 100
handFound = False

fWidth = 0
fHeight = 0

frameWidth = 0
frameHeight = 0

def rescale_frame(frame, wpercent=130, hpercent=130):
    global fWidth, fHeight
    fWidth = int(frame.shape[1] * wpercent / 100)
    fHeight = int(frame.shape[0] * hpercent / 100)

    print(str(fWidth))
    print(str(fHeight))


    return cv2.resize(frame, (fWidth, fHeight), interpolation=cv2.INTER_AREA)


def contours(frame, hist_mask_image):
    #gray_hist_mask_image = cv2.cvtColor(hist_mask_image, cv2.COLOR_BGR2GRAY)
    #ret, thresh = cv2.threshold(gray_hist_mask_image, 0, 255, 0)
    '''
    hsv = cv2.cvtColor(hist_mask_image,cv2.COLOR_BGR2HSV)
    ave = [0, 0, 0]
    allPixR = []
    allPixB = []
    allPixG = []
    for i in (0,len(hsv)-1):
        for j in (0,len(hsv[0])-1):
            ave += hsv[i][j]
            allPixR.append(hsv[i][j][0])
            allPixB.append(hsv[i][j][1])
            allPixG.append(hsv[i][j][2])
    ave = ave/(len(allPixR))
    stdr = np.std(allPixR)+10
    stdb = np.std(allPixB)+10
    stdg = np.std(allPixG)+10
    lower = np.array([int(ave[0]-stdr), int(ave[1]-stdb), int(ave[2]-stdg)])
    upper = np.array([int(ave[0]+stdr), int(ave[1]+stdb), int(ave[2]+stdg)])
    thresh = cv2.inRange(hsv, lower, upper)
    '''
    gray_hist_mask_image = cv2.cvtColor(hist_mask_image, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray_hist_mask_image, 0, 255,0)# cv2.ADAPTIVE_THRESH_MEAN_C)
    #colour_mask = cv2.inRange(hsv,)
    cont, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


    #hull = cv2.convexHull(cont, returnPoints=False)
    #defects = cv2.convexityDefects(cont, hull)

    #if (len(defects) >= 2):
        #cv2.drawContours(frame, cont, -1, (0,255,0), 3)
    return cont


def max_contour(frame, contour_list):
    global bx, by, sx, sy, handFound
    global defHands
    global newHands
    global lengthColec
    global areaHand, cropped
    global fWidth, fHeight
    global resetCount
    neededHands = 0

    neededHands = 0

    exMatch = None

    max_i = -1
    max_area = 0
    min = 7000
    max = 30000
    tempx = 0
    tempy = 0


    with open("Hands.txt", "rb") as fp:
        defHands = pickle.load(fp)
    print("\n\n numHands" +str(len(defHands)) + "\n\n")

    #print("\n\n cont list " +str(len(defHands)) + "\n\n")

    for i in range(len(contour_list)):
        #time.sleep(1)
        cnt = contour_list[i]

        area_cnt = cv2.contourArea(cnt)
        hull = cv2.convexHull(cnt, returnPoints=False)
        defects = cv2.convexityDefects(cnt, hull)

        moment = cv2.moments(cnt)
        if moment['m00'] != 0:
            tempx = int(moment['m10'] / moment['m00']) + sx
            tempy = int(moment['m01'] / moment['m00']) + sy

        peri = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.01 * peri, True)
        #if (len(cnt)>4):
            #print(str(cv2.fitEllipse(cnt)))
        #print("Num of sides: " + str(len(approx)))
        #lengthColec.append(len(approx))
        center = (bx,by)
        colourCenter = (10,10,10)
        cv2.circle(frame, center, 10,colourCenter,2)

        numMatch = 0

        for j in ((defHands)):
                if (cv2.matchShapes(j, cnt, 1, 0.0) < 0.02) and abs(cv2.contourArea(j)-cv2.contourArea(cnt))<7000:
                    numMatch+=1
                    exMatch = j
                    if numMatch > neededHands:
                        break
                #print("matchAve so far: " + str(matchAve))
        if len(defHands) > 0:
            pMatch = numMatch/ len(defHands)
        else:
            pMatch = -1
        #print("\n\n match is: " + str(matchAve) +"\n\n")

        try:
            #if ( len(approx == 3) or (len(approx) >= 11 and len (aprox) < 14) or (len(approx) >= 8 and len (aprox) <= 9) or (len(approx) >= 18 and len (aprox) <= 19)) and len(defects) >=2 and area_cnt > 9000 and moment['m00'] != 0 and ((tempx-bx)**2 + (tempy-by)**2 < 200**2):#area_cnt>min and area_cnt<max and len(defects)>=2:
            cv2.drawContours(cropped, cnt, -1, (0,0,255), 3)

            #print("Center: " + str(tempx) + ", "+ str(tempy))
            #print("Should be : " + str(bx) + ", "+ str(by))


            #print("bad")
            #cv2.circle(frame, bx,by, 10,[10,10,10]
            print("num matched: " +str(numMatch))

            if numMatch >neededHands and area_cnt > 2000 and len(approx)>=5 and len(approx) <=19 and len(defects) >=2 and  ((tempx-bx)**2 + (tempy-by)**2 < 100**2) :#and (areaHand == -1 or abs(area_cnt -areaHand) <2000) and moment['m00'] != 0 and ((tempx-bx)**2 + (tempy-by)**2 < 100**2):#area_cnt>min and area_cnt<max and len(defects)>=2:
                handFound = True
            #if numMatch > 0 :#and ((tempx-bx)**2 + (tempy-by)**2 < 100**2):

            #area_cnt>max_area

                #print("\n\n in \n\n")
                cv2.drawContours(cropped, cnt, -1, (0,255,0), 3)
                cv2.drawContours(cropped, exMatch, -1, (255,0,255), 3)
                newHands.append(cnt)
                areaHand = area_cnt
                bx = tempx
                by = tempy

                '''
                if bx < int(width/2)+20:
                    bx = int(width/2)
                if bx > fWidth-int(width/2):
                    bx = fWidth-int(width/2)
                if by < int(height/2):
                    by = int(height/2)
                if by > fHeight-int(height/2):
                    by = fHeight-int(height/2)
                '''

                print("Center: " + str(bx) + ", "+ str(by))
                max_area = area_cnt
                max_i = i
                print("accepted area" + str(area_cnt))
                #cv2.drawContours(frame, cnt, -1, (0,255,0), 3)

                #peri = cv2.arcLength(cnt, True)
                #approx = cv2.approxPolyDP(cnt, 0.01 * peri, True)
                print("Num of sides: " + str(len(approx)))
                lengthColec.append(len(approx))
                #maxDef =max(defects[0].depth, defects[1].depth)
                #print("convexityDefectDepth: " + str(maxDef))
                #defHands.appned(cnt)
            else:
                handFound = False
                return void
            if max_i != -1:
                return contour_list[max_i]
            return None

        except:
            print("do nothin")
            if max_i != -1:
                return contour_list[max_i]
            return None
        #print("cont area average? lol: " + str(max_area))

        return contour_list[max_i]


def draw_rect(frame):
    rows, cols, _ = frame.shape
    global total_rectangle, hand_rect_one_x, hand_rect_one_y, hand_rect_two_x, hand_rect_two_y

    hand_rect_one_x = np.array(
        [6 * rows / 40, 6 * rows / 40, 6 * rows / 40, 6 * rows / 40, 9 * rows / 40, 9 * rows / 40, 9 * rows / 40, 9 * rows / 40, 12 * rows / 40,
         12 * rows / 40, 12 * rows / 40, 12 * rows / 40, 15 * rows / 40, 15 * rows / 40, 15 * rows / 40, 15 * rows / 40], dtype=np.uint32)

    hand_rect_one_y = np.array(
        [9 * cols / 40, 10 * cols / 40, 11 * cols / 40, 12 * cols / 40 , 9 * cols / 40, 10 * cols / 40, 11 * cols / 40, 12 * cols / 40, 9 * cols / 40,
         10 * cols / 40, 11 * cols / 40, 12 * cols / 40, 9 * cols / 40, 10 * cols / 40, 11 * cols / 40, 12 * cols / 40], dtype=np.uint32)

    hand_rect_two_x = hand_rect_one_x + 10
    hand_rect_two_y = hand_rect_one_y + 10

    for i in range(total_rectangle):
        cv2.rectangle(frame, (hand_rect_one_y[i], hand_rect_one_x[i]),
                      (hand_rect_two_y[i], hand_rect_two_x[i]),
                      (0, 255, 0), 1)

    return frame


def hand_histogram(frame):
    global hand_rect_one_x, hand_rect_one_y

    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    roi = np.zeros([160, 10, 3], dtype=hsv_frame.dtype)

    for i in range(total_rectangle):
        roi[i * 10: i * 10 + 10, 0: 10] = hsv_frame[hand_rect_one_x[i]:hand_rect_one_x[i] + 10,
         hand_rect_one_y[i]:hand_rect_one_y[i] + 10]

    hand_hist = cv2.calcHist([roi], [0, 1], None, [180, 256], [0, 180, 0, 256])
    return cv2.normalize(hand_hist, hand_hist, 0, 255, cv2.NORM_MINMAX)


def hist_masking(backFrame, frame, hist):
    global fWidth, fHeight
    global bx, by, areaHand, cropped, sx, sy, width, height
    range = (int)((7000**(1/2)))
    width = 2*int(range*1)
    height = 2* int(range*1) * 1.5
    sx = bx-int(width/2)
    ex = bx + int(width/2)
    sy = by-int(height/2)
    ey = by + int(height/2)

    if (sx < 0):
        sx = 0+10
        ex = width+10
        bx = int((ex+sx)/2)

    if (sy < 0):

        sy = 0+10
        ey = height+10
        by = int((ey+sy)/2)

    if (ex > fWidth):
        ex = fWidth-10
        sx = ex - width-10
        bx = int((ex+sx)/2)
    if (ey > fHeight):
        ey = fHeight-10
        sy = ey - height-10
        by = int((ey+sy)/2)


    sx = int(sx)
    sy = int(sy)
    ex = int(ex)
    ey = int (ey)
    start = (int(sx),int(sy))
    end = (int(ex),int(ey))
    colour = (100,100,100)
    cv2.rectangle(frame, start, end, colour, 1)

    if len(frame[sy:ey, sx : ex])>0:
        cropped = frame[sy:ey, sx : ex]

    hsv = cv2.cvtColor(cropped, cv2.COLOR_BGR2HSV)
    dst = cv2.calcBackProject([hsv], [0, 1], hist, [0, 180, 0, 256], 1)

    disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (20, 20))
    #disc = cv2.erode(disc, (5,5))
    cv2.filter2D(dst, -1, disc, dst)

    ret, thresh = cv2.threshold(dst, 150, 255, cv2.THRESH_BINARY)

    # thresh = cv2.dilate(thresh, None, iterations=5)

    thresh = cv2.merge((thresh, thresh, thresh))

    return cv2.bitwise_and(cropped, thresh)
    #return cv2.bitwise_and(cv2.bitwise_not(backFrame),cv2.bitwise_and(frame, thresh))




def centroid(max_contour):
    global bx, by
    moment = cv2.moments(max_contour)
    if moment['m00'] != 0:
        tempX = int(moment['m10'] / moment['m00'])
        tempY = int(moment['m01'] / moment['m00'])
        if ((bx-tempX)**2 + (by-tempY)**2 <= 100**2):
            bx = tempX
            by = tempY
        #return cx, cy
    #else:
        #return None


def farthest_point(defects, contour, centroid):
    global bx, by
    if defects is not None and centroid is not None:
        s = defects[:, 0][:, 0]
        #cx, cy = centroid
        centroid

        x = np.array(contour[s][:, 0][:, 0], dtype=np.float)
        y = np.array(contour[s][:, 0][:, 1], dtype=np.float)

        xp = cv2.pow(cv2.subtract(x, bx), 2)
        yp = cv2.pow(cv2.subtract(y, by), 2)
        dist = cv2.sqrt(cv2.add(xp, yp))

        dist_max_i = np.argmax(dist)

        if dist_max_i < len(s):
            farthest_defect = s[dist_max_i]
            farthest_point = tuple(contour[farthest_defect][0])
            return farthest_point
        else:
            return None


def draw_circles(frame, traverse_point):
    if traverse_point is not None:
        for i in range(len(traverse_point)):
            cv2.circle(frame, traverse_point[i], int(5 - (5 * i * 3) / 100), [0, 255, 255], -1)

def cover_face (frame):
    start_p = (startX, startY)
    end_p = (endX, endY)
    color = (255, 0, 0)
    cv2.rectangle(frame, start_p, end_p, color, 1)

def manage_image_opr(backFrame, frame, hand_hist):
    global cx, cy, cropped, fWidth, fHeight
    hist_mask_image = hist_masking(backFrame, frame, hand_hist)
    contour_list = contours(frame, hist_mask_image)
    max_cont = max_contour(frame, contour_list)

    #cnt_centroid =
    centroid(max_cont)
    cnt_centroid = cx, cy
    cv2.circle(cropped, cnt_centroid, 5, [255, 0, 255], -1)

    if max_cont is not None:
        hull = cv2.convexHull(max_cont, returnPoints=False)
        defects = cv2.convexityDefects(max_cont, hull)
        far_point = farthest_point(defects, max_cont, cnt_centroid)#cx, cy)#cnt_centroid)
        print("Centroid : " + str(cnt_centroid) + ", farthest Point : " + str(far_point)) #should be cnt_centroid
        cv2.circle(frame, far_point, 5, [0, 0, 255], -1)

        #get display resolution
        width, height = pyautogui.size()

        #split far point into integers
        if (str(far_point) != "None"):
            endX = int(str(far_point).find(","))
            #pointX = int(str(far_point)[1:endX], 10)
            pointX = bx

            endY = str(far_point).find(")")
            #pointY = int(str(far_point)[endX + 2:endY], 10)
            pointY = by

            #coordinate = (str(far_point)).split()
            #print (coordinate[0])
            #print (coordinate([1]))

            print ("point x: ", pointX, "point y: ", pointY)
            print(width, "width")

            speed = math.floor((fHeight/2 - pointY)//4)
            #print("height", height)
            print("scroll speed ", speed)

            if (speed < 20 or speed > 30): #region verically for scroll
                speed-=10
                pyautogui.scroll(speed) #scrolls faster depending on height
            else:
                speed = math.floor((fWidth/2 - pointX)//4)
                print("zoom speed ", speed)
                if (speed > 35):
                    speed-=10
                    pyautogui.keyDown('ctrl')
                    pyautogui.press('+')
                    pyautogui.keyUp('ctrl')
                if (speed < 10):
                    pyautogui.keyDown('ctrl')
                    pyautogui.press('-')
                    pyautogui.keyUp('ctrl')

            '''#move mouse
            pyautogui.moveTo(width - 2*pointX, 2*pointY, 0)
            #noneCount = 0

            global firstRun
            global sameCount
            global oldX
            global oldY

            if (firstRun == 0):
                firstRun = 1
            else:
                if (pointX - oldX < 15 and pointY - oldY < 15):
                #if the centroid stays many times in the same position, click
                    sameCount = sameCount + 1
                else:
                    sameCount = 0

            oldX = pointX
            oldY = pointY

            if (sameCount == 5):
                #pyautogui.click()
                print("click")
                sameCount = 0'''





        if len(traverse_point) < 20:
            traverse_point.append(far_point)
        else:
            traverse_point.pop(0)
            traverse_point.append(far_point)

        draw_circles(frame, traverse_point)
        cover_face(frame)
def getBack (frame):
    global background
    global have_background
    if have_background == False:
        background = frame
    #else:
       #cv2.accumulateWeighted(frame, background,0.5);

    have_background = True

def cutOutFace (frame):
    global startX
    global startY
    global endX
    global endY
    if (startX == None):
        return frame
    for i in range(startX, endX):
        for j in range (startY, endY):
            frame[i,j] = 0

    return frame

def getBackHist (frame):
    global backgroundHists
    global backDivX
    global backDivY
    global hand_rect_one_x, hand_rect_one_y

    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    roi = np.zeros([90, 10, 3], dtype=hsv_frame.dtype)
    for i in range(total_rectangle):
        roi[i * 10: i * 10 + 10, 0: 10] = hsv_frame[hand_rect_one_x[i]:hand_rect_one_x[i] + 10, hand_rect_one_y[i]:hand_rect_one_y[i] + 10]

    hand_hist = cv2.calcHist([roi], [0, 1], None, [180, 256], [0, 180, 0, 256])
    return cv2.normalize(hand_hist, hand_hist, 0, 255, cv2.NORM_MINMAX)

def plotHand():
    global lengthColec

    data = np.random.normal(0, 21, 100)

    bins = np.arange(0, 21, 1)

    plot.xlim([min(data)-.5, max(data)+.5])

    plot.hist(data, bins=bins, alpha=0.5)
    plot.title('metaData plot')
    plot.xlabel('side lengths)')
    plot.ylabel('Number of occurance')

    plot.show()



def main():
    global hand_hist, resetCount, handFound
    #global background
    #global have_background
    global cx
    global cy,bx,by
    global defHands, newHands

    is_hand_hist_created = False
    capture = cv2.VideoCapture(0)


    while capture.isOpened():
        if resetCount <=0:
            bx = 200
            by =300

        print("Reset data: " + str(bx) + " " + str(resetCount) + " " + str(by))

        pressed_key = cv2.waitKey(1)
        _, frame = capture.read()

        if pressed_key & 0xFF == ord('z'):
            #getBack(frame)
            is_hand_hist_created = True
            #frame = cutOutFace(frame)
            hand_hist = hand_histogram(frame)
            cx = int(frame.shape[0]/2)
            cy = int(frame.shape[1]/2)

        #if pressed_key & 0xFF == ord('r'):
            #have_background = False
            #getBack(frame)

        if pressed_key & 0xFF == ord('e') and len(defHands)>0:
            sum = 0
            with open("Hands.txt", "wb") as fp:
                all = newHands+ defHands
                pickle.dump(all, fp)
                sum += len(newHands)
                print("   tot sum " + str(sum))
            break

        if is_hand_hist_created:
            manage_image_opr(background, frame, hand_hist)
            if handFound:
                resetCount = 100
            else:
                resetCount -=1

        else:
            frame = draw_rect(frame)

        cv2.imshow("Live Feed", cv2.flip(rescale_frame(frame),1))

        if pressed_key == 27:
            #plotHand()
            break

    cv2.destroyAllWindows()
    capture.release()


if __name__ == '__main__':
    main()

import cv2 import  skimageimport matplotlib.pyplot as plt import numpy as npfrom skimage.metrics import mean_squared_errorfrom skimage.metrics import structural_similarity as ssimimport os import pandas as pdsource_path="data_1"ind=source_path.rsplit("_")[-1]try:    res_path=f'./res_{ind}'    os.mkdir(res_path)except:    passref=cv2.imread(f"./{source_path}/ref.png")cap=cv2.imread(f"./{source_path}/cap1.png")fig,(ax1,ax2)=plt.subplots(1,2,figsize=(10,5))ax1.imshow(ref)ax2.imshow(cap)ax1.set_xlabel('reference image')ax2.set_xlabel('capture image')fig.show()fig.savefig(os.path.join(res_path,"raw_image.jpg"))gray_ref=cv2.cvtColor(ref, cv2.COLOR_BGR2GRAY)gray_cap=cv2.cvtColor(cap, cv2.COLOR_BGR2GRAY)fig,(ax1,ax2)=plt.subplots(1,2,figsize=(10,5))ax1.imshow(gray_ref,"gray")ax2.imshow(gray_cap,"gray")ax1.set_xlabel('reference grayscaled image')ax2.set_xlabel('capture grayscaled image')fig.show()fig.savefig(os.path.join(res_path,"grayscaled_image.jpg"))GB_ref = cv2.GaussianBlur(gray_ref,(5,5),1.4)GB_cap = cv2.GaussianBlur(gray_cap,(5,5),1.4)fig,(ax1,ax2)=plt.subplots(1,2,figsize=(10,5))ax1.imshow(GB_ref,"gray")ax2.imshow(GB_cap,"gray")ax1.set_xlabel('reference GaussianBlur image')ax2.set_xlabel('capture GaussianBlur image')fig.show()fig.savefig(os.path.join(res_path,"GaussianBlur_image.jpg"))edges_ref = cv2.Canny(GB_ref,50,170)edges_cap = cv2.Canny(GB_cap,50,170)fig,(ax1,ax2)=plt.subplots(1,2,figsize=(10,5))ax1.imshow(edges_ref,"gray")ax2.imshow(edges_cap,"gray")ax1.set_xlabel('reference edge detected image')ax2.set_xlabel('capture edge detected image')fig.show()fig.savefig(os.path.join(res_path,"edge_detected_image.jpg"))mse_const = mean_squared_error(edges_cap, edges_ref)ssim_const = ssim(edges_cap, edges_ref,                  data_range=edges_ref.max() - edges_ref.min())density1=round(np.clip(100-100*(np.count_nonzero(edges_ref)/np.count_nonzero(edges_cap)),0,100),2)mask=cv2.imread(f'./{source_path}/mask.png')mask=cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)_, mask = cv2.threshold(mask, 60, 255, cv2.THRESH_BINARY)diff_image=cv2.absdiff(ref, cap)ret, thresh = cv2.threshold(diff_image, 40, 255, cv2.THRESH_BINARY)gray_thresh=cv2.cvtColor(thresh, cv2.COLOR_BGR2GRAY)# plot image after thresholdingfig,([ax1,ax2],[ax3,ax4])=plt.subplots(2,2,figsize=(10,10))# ax1.imshow(GB_ref, cmap = 'gray')ax1.imshow(cap, cmap = 'gray')ax2.imshow(diff_image, cmap = 'gray')ax3.imshow(gray_thresh, cmap = 'gray')ax4.imshow(mask, cmap = 'gray')# ax1.set_xlabel('reference image')ax1.set_xlabel('capture image')ax2.set_xlabel('images difference')ax3.set_xlabel('images threshold')ax4.set_xlabel('mask')fig.show()fig.savefig(os.path.join(res_path,"diff_img_method2.jpg"))density2=round(np.count_nonzero(thresh)/np.count_nonzero(mask)*100,2)acc=round(((100)-abs(density1-density2))/100,3)df=pd.DataFrame([density1,density2,acc],columns=["value"],index=["Density 1","Density 2","Accuracy"])df.to_csv(os.path.join(res_path,"result.csv"))cap = cv2.VideoCapture(f'./{source_path}/movie.avi')car_cascade = cv2.CascadeClassifier('cars.xml')frame_width = int(cap.get(3))frame_height = int(cap.get(4))   size = (frame_width, frame_height)out = cv2.VideoWriter(f'./{res_path}/output.mp4', cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), 15, size)d1_lst,d2_lst=[],[]counter=0c_lst=[]while(cap.isOpened()):    counter+=1    # reads frames from a video    ret, frames = cap.read()        if ret:        c_lst.append(counter)        # compute density of each frames        gray = cv2.cvtColor(frames, cv2.COLOR_BGR2GRAY)        GB = cv2.GaussianBlur(gray,(5,5),1.4)        edges = cv2.Canny(GB,50,170)        density_1=round(np.clip(100-100*(np.count_nonzero(edges_ref)/np.count_nonzero(edges)),0,100),2)                diff=cv2.absdiff(ref, frames)        thresh = cv2.cvtColor(cv2.threshold(diff, 60, 255, cv2.THRESH_BINARY)[1],cv2.COLOR_BGR2GRAY)        density_2=round(1.3*np.count_nonzero(thresh)/np.count_nonzero(mask)*100,2)            d1_lst.append(density_1)        d2_lst.append(density_2)        acc=round(((100)-abs(density_1-density_2))/100,3)                # Detects cars of different sizes in the input image        cars = car_cascade.detectMultiScale(gray, 1.1, 1)                     # To draw a rectangle in each cars        for (x,y,w,h) in cars:            cv2.rectangle(frames,(x,y),(x+w,y+h),(0,0,255),2)                                font                   = cv2.FONT_HERSHEY_SIMPLEX        bottomLeftCornerOfText1 = (5,10)        bottomLeftCornerOfText2 = (5,20)        bottomLeftCornerOfText3 = (5,30)        fontScale              = .3        fontColor              = (0,0,255)        thickness              = 1        lineType               = 2                cv2.putText(frames,f"Method 1 Density : {density_1}",             bottomLeftCornerOfText1,             font,             fontScale,            fontColor,            thickness,            lineType)                cv2.putText(frames,f"Method 2 Density : {density_2}",             bottomLeftCornerOfText2,             font,             fontScale,            fontColor,            thickness,            lineType)                cv2.putText(frames,f"Accuracy : {acc}",             bottomLeftCornerOfText3,             font,             fontScale,            fontColor,            thickness,            lineType)                 # Display frames in a window         out.write(frames)        cv2.imshow('video2', frames)                  # Wait for Esc key to stop        if cv2.waitKey(1) & 0xFF == ord('q'):            break    else:        break     # De-allocate any associated memory usagecap.release()out.release()cv2.destroyAllWindows()fig,ax=plt.subplots(1,1,figsize=(10,5))ax.plot(d1_lst,color="red")ax.plot(d2_lst,color="blue")fig.legend(["Method 1 density",            "Method 2 density"])fig.show()fig.savefig(os.path.join(res_path,"Density_plot.jpg"))
import argparse
from PIL import Image
import numpy as np 
import os
from os import listdir
import errno
import sys
from stable_diffusion_xl import sdxl_main
from stable_diffusion_xl import add_sd_params
SUCCESS = 0
ERROR = 1
UNKNOWN_FAILURE = 2


def compare(platform, thresholds, corelation_factor, verbosity):
    
    num_threshold = len (thresholds)
    if num_threshold == 0:
        return UNKNOWN_FAILURE
        
    goldenImageDir = "./goldenImages/"
    generatedImageDir = "./generatedImages"
    
    if(platform == "MTL"):
        goldenImageDir = goldenImageDir + "MTL"
    else:
        goldenImageDir = goldenImageDir + "DG2"
    err_code = SUCCESS
    for imageName in os.listdir(goldenImageDir):
          if (imageName.endswith(".png")):
            
            goldenImgPath = goldenImageDir + "/" + imageName;
            generatedImgPath = generatedImageDir + "/" + imageName;
            if not os.path.isfile(generatedImgPath):
                raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), generatedImgPath)
                sys.exit(1)
                
            img_a_pixels = Image.open(goldenImgPath).getdata()
            img_b_pixels = Image.open(generatedImgPath).getdata()
            if(len(img_a_pixels) != len(img_b_pixels)):
                if verbosity:
                    print("FAIL : Image shapes do not match between ", goldenImgPath, " and ", generatedImgPath)
                return UNKNOWN_FAILURE
                
            img_a_array = np.array(img_a_pixels)
            img_b_array = np.array(img_b_pixels)
            #difference = (img_a_array != img_b_array).sum()
            size = img_a_array.size
            if size == 0:
                return UNKNOWN_FAILURE
                
            for threshold in thresholds:
                difference_with_threshold  = 0
                difference_with_threshold = (np.abs(img_a_array - img_b_array) >= threshold).sum()
                if threshold == 0 and difference_with_threshold > 0:
                    err_code = ERROR
                    if verbosity:
                        print("Threshold = ", threshold, "Fail!")
                        print("Pixel mismatch percentage : ", float(difference_with_threshold/size)*100, " %")
                    continue
                elif threshold == 0:
                    continue
                    
                corr_frac = float(corelation_factor/threshold) if float(corelation_factor/threshold) < 1 else 1 
                if( float(difference_with_threshold/size) <= corr_frac):
                    if verbosity:
                        print("Threshold = ", threshold, "Pass!")
                        print("Pixel mismatch percentage : ", float(difference_with_threshold/size)*100, " %")
                else:
                    if verbosity:
                        print("Threshold = ", threshold, "Fail!")
                        print("Pixel mismatch percentage : ", float(difference_with_threshold/size)*100, " %")
                    err_code = ERROR
          
          else:
            return UNKNOWN_FAILURE
    return err_code
            
          
     

def run_comparator(platform, thresholds, corr_const, verbosity):
    
    #compare generated image with golden image
    print("Comparing generated image with golden image...")
    ret_code = compare(platform, thresholds, corr_const, verbosity)
    print("code : ", ret_code)
    if verbosity:
        if ret_code == SUCCESS:
            print("PASS!")
        elif ret_code == ERROR:
            print("ERROR!")
        else:
            print("Unknown Failure!")   
    return ret_code
    
def add_image_compare_params(parser):
    parser.add_argument("--thresholds", default=[25.0, 20.0, 15.0], nargs="*", type=float, help="Maximum difference between two pixel. ")
    parser.add_argument("--correlation_const", default=2.5, type=float, help="When a threshold value is small, corelation constant should be higher")
    parser.add_argument("--platform", default="DG2", type=str, help="Platform: DG2 or MTLH")
    parser.add_argument("--verbosity", action="store_true", help="Print error details")
## main function for other script    
def main():
    parser = argparse.ArgumentParser()
    img_com_group = parser.add_argument_group(title="image comparator params")
    stable_diffusion_group = parser.add_argument_group(title="stable diffusion params")
    add_image_compare_params(img_com_group)
    add_sd_params(stable_diffusion_group)
    args = parser.parse_args()
    #create image using stable diffusion 
    sdxl_main(args);
    
    return run_comparator(args.platform, args.thresholds, args.correlation_const, args.verbosity)
    
if __name__ == "__main__":
    main()

 
    


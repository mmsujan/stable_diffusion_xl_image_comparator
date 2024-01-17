## Installation

 - Clone "stable_diffusion_xl_image_comparator"
 - Open Anaconda prompt ( Recommended)
 - cd to "stable_diffusion_image_comparator" directory
 
Run following command to create conda environment
 
```
conda create -n sd_xl
conda activate sd-xl
pip install .
pip install -r requirements-sdxl.txt
```
For python environment, open command prompt, and cd to "stable_diffusion_image_comparator" directory. Run following command:
```
pip install .
pip install -r requirements-sdxl.txt
```
## Run Test
 - Copy Stable Diffusion 1.5 models from [SD_XL_models]() 
 - Unzip " models" directory and put it inside "stable_diffusion_image_comparator"
 - From conda or command prompt, cd path to "stable_diffusion_image_comparator" directory  
 
 Sample Run: 
 ```
 python image_compare.py
 ```
 
 - You can set different threshold values as per requirement. For an example:
 ```
 python image_compare.py --thresholds 15.0 10.0 5.0
 ```
 - Command line argument options:
 
```
usage: image_compare.py [-h] [--thresholds [THRESHOLDS [THRESHOLDS ...]]] [--correlation_const CORRELATION_CONST]
                        [--platform PLATFORM] [--verbosity]

optional arguments:
  -h, --help            show this help message and exit
  --thresholds [THRESHOLDS [THRESHOLDS ...]]
                        Maximum difference between two pixel.
  --correlation_const CORRELATION_CONST
                        When a threshold value is small, corelation constant should be higher
  --platform PLATFORM   Platform: DG2 or MTL
  --verbosity           Print error details
 
```
 - Note : E2E Performance information is reported as it/s (but sometimes as s/it  <- CI folks need to aware of it)
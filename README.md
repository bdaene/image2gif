# image2gif
Transform images in a directory to a gif.

## Installation

Create the environment using the `requirements.yml` file.

For example using conda: `conda env create -f requirements.yml`

That's all :) 

## Usage

`python main.py <source directory> <target file>`

Where the `<source directory>` is the directory containing the images and `<target file>` is the file where the gif will be stored.  

Notes:
* All images have to have the same dimensions.
* You can add the duration in hundreds of second at the end of the image name. For example `image_85.png` would last 0.85s. Default to 1s.

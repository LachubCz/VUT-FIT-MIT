/*
	input: 
		input_image 		[image pathname]
		kernel_size			[1, 3, 7, ...]
		noise_type			[gauss, sp]
		noise_parameter	[stdev for Gaussian noise, percentage of noisy pixels for Salt&Pepper noise]
		
	output: list of parameters and PSNR (Peak signal-to-noise ratio) values

	usage example:
		./mt01 lena.png 3 gauss 0.1
		
Uloha
	Doplnte chybejici kusy zdrojoveho kodu:
		- telo funkce pro vypocet "Peak signal-to-noise ratio" hodnoty
		- nacitani a ukladani obrazku
		- filtraci medianovym a Gaussovym filtrem
	
	Kod doplnujte pouze na vyhrazena mista.
	Vysledny program nesmi vypisovat nic navic (nic vic, nez vypisuje pripravena kostra programu). 
	
	
*/

#include <iostream> // for standard I/O
#include <string>   // for strings
#include <iomanip>  // for controlling float print precision
#include <sstream>  // string to number conversion

#include <opencv2/core/core.hpp>        // Basic OpenCV structures (cv::Mat, Scalar)
#include <opencv2/imgproc/imgproc.hpp>  // Gaussian Blur
#include <opencv2/highgui/highgui.hpp>  // OpenCV window I/O

using namespace std;
using namespace cv;

double getPSNR(const Mat& I1, const Mat& I2);
void addGaussianNoise(const Mat& I, Mat& O, double mean = 0.0, double stdev = 0.05);
void addSPNoise(const Mat& I, Mat& O, double p = 0.1);

int main(int argc, char *argv[])
{
	if (argc < 5)
	{
		cout << "Not enough parameters" << endl;
		return -1;
	}

	Mat origI, noiseI;
	int kernel_size = 3;
	string noise_type;
	double noise_param;

	origI = Mat::zeros(Size(512,512),CV_8U);

	/*  Working area - begin */

	// load image to origI, use first argument, load as grayscale image
    std::string img_path = ""; 
    img_path = std::string(argv[1]);
	origI = imread(img_path, IMREAD_GRAYSCALE);

	/*  Working area - end */

	if(! origI.data )                              
	{
		cout <<  "Could not open or find the original image" << endl ;
		return -1;
	}

	// load test parameters and noise the original image
 	stringstream conv;
  	conv << argv[2] << endl << argv[3] << endl << argv[4];
  	conv >> kernel_size >> noise_type >> noise_param;
		
	if (noise_type == "gauss")
	{
		addGaussianNoise(origI, noiseI, 0.0, noise_param);
	}
	else if (noise_type == "sp")
	{
		addSPNoise(origI, noiseI, noise_param);
	} else
	{
		cout <<  "Wrong noise parameters." << endl ;
	   return -1;
	}
	
	// output variables
	double psnrO = 0.0, psnrG = 0.0, psnrM = 0.0;
	Mat denoiseIG, denoiseIM;
	string odpoved = "";

	denoiseIG = noiseI.clone();
	denoiseIM = noiseI.clone();
		
	// compute PSNR of original and noise images
	psnrO = getPSNR(origI, noiseI);

	/*  Working area - begin */
	
	// save the noise image (noiseI) to "noise.png" file (use this exact name and path)
	// ...

	cv::imwrite("noise.png", noiseI);

	// suppress noise using Gaussian blur and compute PSNR to psnrG variable
	// use denoiseIG image as the result of denoising
	// save the image to "denoiseG.png" file (use this exact name and path)
	// ...

    cv::GaussianBlur(noiseI, denoiseIG, Size( kernel_size, kernel_size ), 0, 0);
    psnrG = getPSNR(origI, denoiseIG);
	cv::imwrite("denoiseG.png", denoiseIG);

	// suppress noise using median filter and compute PSNR to psnrM variable
	// use denoiseIM image as the result of denoising
	// save the image to "denoiseM.png" file (use this exact name and path)
	// ...

    cv::medianBlur(noiseI, denoiseIM, kernel_size);
    psnrM = getPSNR(origI, denoiseIM);
    cv::imwrite("denoiseM.png", denoiseIM);

	/*
		Otazka: Je originalni a zasumeny obraz. Je-li hodnota 
		PSNR originalniho a filtrovaneho obrazu vyrazne vetsi po 
		filtraci medianem nez po filtraci Gaussovym filtrem, jakym 
		typem sumu je pravdepodobne obraz zkreslen?
	*/
	// doplnte "gauss" nebo "sp"
	odpoved = "sp";		
	
	/*  Working area - end */

	// print parameters, PSNR values and answer 
	cout << kernel_size << "; ";
	cout << noise_type  << "; ";
	cout << noise_param << "; ";
	cout << setiosflags(ios::fixed) << setprecision(3) << psnrO << "; ";
	cout << setiosflags(ios::fixed) << setprecision(3) << psnrG << "; ";
	cout << setiosflags(ios::fixed) << setprecision(3) << psnrM << "; ";
	cout << odpoved << "; ";
	cout << endl;
  
	return 0;
}
     
double getPSNR(const Mat& I1, const Mat& I2)
{
	double psnr = 0.0;
	/*  Working area - start */
	
	// reference:	http://docs.opencv.org/2.4/doc/tutorials/highgui/video-input-psnr-ssim/video-input-psnr-ssim.html#image-similarity-psnr-and-ssim
	// copying opencv tutorial code is allowed 
    Mat s1;
    absdiff(I1, I2, s1);       // |I1 - I2|
    s1.convertTo(s1, CV_32F);  // cannot make a square on 8 bits
    s1 = s1.mul(s1);           // |I1 - I2|^2

    Scalar s = sum(s1);         // sum elements per channel

    double sse = s.val[0] + s.val[1] + s.val[2]; // sum channels

    if( sse <= 1e-10) // for small values return zero
        return 0;
    else
    {
        double  mse =sse /(double)(I1.channels() * I1.total());
        double psnr = 10.0*log10((255*255)/mse);
        return psnr;
    }
	/*  Working area - end */

	return psnr;
}


// I is the grayscale of the input image
void addGaussianNoise(const Mat& I, Mat& O, double mean, double stdev)
{
	
	Mat noise = Mat(I.size(),CV_64F);
	Mat r1    = Mat(I.size(),CV_64F);
	normalize(I, r1, 0.0, 1.0, CV_MINMAX, CV_64F);
	randn(noise, mean, stdev);
	r1 = r1 + noise;
	r1.convertTo(O, I.type(), 255.0);
	return;
}


void addSPNoise(const Mat& I, Mat& O, double p)
{
	Mat sp_noise = Mat::zeros(I.size(),CV_8U);
	randu(sp_noise,0,255);

	int limit_approx = floor(p*256);

	Mat black = sp_noise < limit_approx;
	Mat white = sp_noise > 256-limit_approx;
	
	O = I.clone();
	O.setTo(255,white);
	O.setTo(0,black);
	return;
}


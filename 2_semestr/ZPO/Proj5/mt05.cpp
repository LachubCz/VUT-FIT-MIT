#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <iostream>

#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>



//  Funkce pro generování šumu typu pepř a sůl.
//  Parametr pokrytí udává, jaké procento pixelů v obraze bude šumem zkresleno a je v rozsahu 0.0-1.0.
void peprAsul( const cv::Mat& src, cv::Mat& dst, float pokryti )
{
	dst = src.clone();
	// Na náhodné pozice v obraze vygenerujte šum typu pepř a sůl.
	// Množství zašuměných pixelů musí odpovídat pokryti 
	/*  Working area - begin */
    int counter = 0;
    cv::RNG randomChooser;
    int balance[src.cols * src.rows];

    for (int i=0; i < src.rows; ++i){
        for (int j=0; j < src.cols; ++j){
            if (randomChooser.uniform(0.f,1.f) <= pokryti){
                balance[counter] = 1;
            }
            else{
                balance[counter] = 0;
            }
            counter += 1;
        }
    }

    counter = 0;
    for (int i=0; i < src.rows; ++i){
        for (int j=0; j < src.cols; ++j){
            if (1 == balance[counter]){
                if (randomChooser.uniform(0.f,1.f) <= 0.5){
                    dst.at<unsigned char>(i,j) = int(0);
                }
                else{
                    dst.at<unsigned char>(i,j) = int(255);
                }
            }
            counter += 1;
        }
    }
	/*  Working area - end */
}


//  Funkce pro filtraci obrazu pomocí mediánového filtru.
//     - velikost filtru v pixelech

void median( const cv::Mat& src, cv::Mat& dst, int velikost )
{
	// velikost - chceme liché číslo, minimálně 3
	int stred = velikost/2;
	stred = MAX(1,stred);
	velikost = 2*stred+1;
	
	// zvětšíme obraz a okopírujeme krajní hodnoty do okrajů
	cv::Mat srcBorder;
	copyMakeBorder( src, srcBorder, stred, stred, stred, stred, cv::BORDER_REPLICATE );

	// připravíme výstupní obraz
	dst = cv::Mat( src.size(), src.type() );

	// implementujte ručně mediánový filtr, výsledek uložte do výstupního obrazu dst
	// k řazení lze využít funkce std::sort()
	/*  Working area - begin */
    int index = 0;
    int size = velikost * velikost;
    int balance[size];

    for (int i=0; i < dst.rows; ++i){
        for (int j=0; j < dst.cols; ++j){

            int counter = 0;
            for (int k = 0; k < velikost; ++k)
            {
                for (int p = 0; p < velikost; ++p)
                {
                    balance[counter] = srcBorder.at<unsigned char>(i+k, j+p);
                    counter += 1;
                }
            }

            std::sort(balance, balance+size); 
            index = (velikost*velikost)/2;
            dst.at<unsigned char>(i,j) = int(balance[index]);
        }
    }
	/*  Working area - end */

	return;
}



/* Vyhodnocení/porovnání výsledku s referenčním obrazem. */
void checkDifferences( const cv::Mat test, const cv::Mat ref, std::string tag, bool save = false);


//---------------------------------------------------------------------------
//---------------------------------------------------------------------------

//
// Examples of input parameters
// ./mt-05 ../../data/garden.png 0.05 7

int main(int argc, char* argv[])
{
    std::string img_path = "";
	float noise_amount = 0.05;
    int filter_size = 7;

	// check input parameters
	if( argc > 1 ) img_path = std::string( argv[1] );
	if( argc > 2 ) noise_amount = atof( argv[2] );
	if( argc > 3 ) filter_size = atoi( argv[3] );

	// load testing images
	cv::Mat src_rgb = cv::imread( img_path );

	// check testing images
	if( src_rgb.empty() ) {
		std::cout << "Failed to load image: " << img_path << std::endl;
		return -1;
	}

	cv::Mat src_gray;
	cv::cvtColor( src_rgb, src_gray, CV_BGR2GRAY );

	//---------------------------------------------------------------------------

	cv::Mat zasum, medi, medi_ref;

	peprAsul( src_gray, zasum, noise_amount );

	median( zasum, medi, filter_size );
	cv::medianBlur( zasum, medi_ref, filter_size );

	// vyhodnocení
	checkDifferences( zasum, src_gray, "05_noise", true );
	checkDifferences( medi,  medi_ref, "05_median", true );
	std::cout << std::endl;
	
    return 0;
}
//---------------------------------------------------------------------------




void checkDifferences( const cv::Mat test, const cv::Mat ref, std::string tag, bool save )
{
	double mav = 255., err = 255., nonzeros = 255.;
	cv::Mat diff;

	if( !test.empty() && !ref.empty() ) {
		cv::absdiff( test, ref, diff );
		cv::minMaxLoc( diff, NULL, &mav );
		err = ( cv::sum(diff).val[0] / (diff.rows*diff.cols) );
		nonzeros = 1. * cv::countNonZero( diff ) / (diff.rows*diff.cols);
	}
	
	if( save ) {
		if( !test.empty() ) { cv::imwrite( (tag+".png").c_str(), test ); }
		if( !diff.empty() ) { diff *= 255;	cv::imwrite( (tag+"_err.png").c_str(), diff ); }
	}

	printf( "%s %.2f %.2f %.2f ", tag.c_str(), err, nonzeros, mav );

	return;
}



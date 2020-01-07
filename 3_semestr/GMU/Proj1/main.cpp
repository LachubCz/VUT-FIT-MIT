/**
* @file main.cpp
* @author Václav Martinka a Petr Buchal
* @date 07. 01. 2020 (21:54)
* @brief
*/


#include <stdlib.h>
#include <stdio.h>
#include <stdarg.h>
#include <string.h>
#include "oclHelper.h"

#include <CL/cl.hpp>

#include "parser.hpp"
#include "Coord.hpp"
#include "Spheres.hpp"
#include "BoundingSphere.hpp"

#define SUBCUBES_IN_LINE 8
#define DIMENSION_SIZE (SUBCUBES_IN_LINE * SUBCUBES_IN_LINE * SUBCUBES_IN_LINE)
#define DEVIATION 0.0000001

#ifndef DISTANCE_LIMIT
	#define DISTANCE_LIMIT 0.000001
#endif


using namespace std;

int main(int argc, char* argv[]) {
	if (argc != 2) {
		printf("Spatne argumenty. Pouzijte pouze jeden argument se jmenem vstupniho souboru\n");
		getchar();
		return 1;
	}

	Spheres spheres = parse(argv[1]);
	//
	/////////////////////////////////////////
	// Spustim vypocet na CPU
	double cpuStart = getTime();

	BoundingSphere boundingSphere(spheres);
	Sphere cpuResultSphere = boundingSphere.getBoundingSphere();

	double cpuEnd = getTime();
	/////////////////////////////////////////


	// Pocet kouli
	const size_t COUNT = spheres.count();

	cl_int errMsg;


	// Pripravim data
	vector<cl_float> xData(COUNT);
	vector<cl_float> yData(COUNT);
	vector<cl_float> zData(COUNT);
	vector<cl_float> radiusData(COUNT);

	for (size_t i = 0; i < COUNT; ++i) {
		xData[i] = spheres.getX(i);
		yData[i] = spheres.getY(i);
		zData[i] = spheres.getZ(i);
		radiusData[i] = spheres.getRadius(i);
	}

	vector<cl_float> resultsGPU(DIMENSION_SIZE);

	vector<cl_float> xCoord(DIMENSION_SIZE);
	vector<cl_float> yCoord(DIMENSION_SIZE);
	vector<cl_float> zCoord(DIMENSION_SIZE);

	Coord from, to;
	boundingSphere.getBoundingBlock(from, to);
	cl_float fromX = from.x;
	cl_float fromY = from.y;
	cl_float fromZ = from.z;
	cl_float toX = to.x;
	cl_float toY = to.y;
	cl_float toZ = to.z;

	const cl_float distanceLimit = static_cast<float>(DISTANCE_LIMIT);
	const cl_int subcubesInLine = SUBCUBES_IN_LINE;



	// Ziskam GPU
	std::vector<cl::Platform> platforms;
	std::vector<cl::Device> devices;
	
	clPrintErrorExit(cl::Platform::get(&platforms), "cl::Platform::get");
	platforms[0].getDevices(CL_DEVICE_TYPE_GPU, &devices);

	cl::Device gpuDevice = devices[0];
	platforms.clear();


	// Vytvorim context a queue se zapnutym profilovanim
	cl::Context context(gpuDevice);
	cl::CommandQueue queue(context, gpuDevice, CL_QUEUE_PROFILING_ENABLE);


	// Nactu zdrojovy kod programu
	char *programSource = readFile("gpuBoundingSphere.cl");
	cl::Program::Sources sources;
	sources.push_back(std::pair<const char *, size_t>(programSource, strlen(programSource)));


	// Vytvorim program
	cl::Program program(context, sources);
	//clPrintErrorExit(errMsg, "clCreateProgramWithSource");


	// Kompiluji program
	if ((errMsg = program.build(std::vector<cl::Device>(1, gpuDevice), "", NULL, NULL)) == CL_BUILD_PROGRAM_FAILURE) {
		cl_int errMsg2;
		printf("Build log:\n %s", program.getBuildInfo<CL_PROGRAM_BUILD_LOG>(gpuDevice, &errMsg2).c_str());
		clPrintErrorExit(errMsg2, "cl::Program::getBuildInfo<CL_PROGRAM_BUILD_LOG>");
	}
	clPrintErrorExit(errMsg, "clBuildProgram");


	// Vytvorim kernel
	cl::Kernel kernel(program, "boundingSphere", &errMsg);
	clPrintErrorExit(errMsg, "cl::Kernel");


	//===========================================================================================
	// Vytvorim buffery
	cl::Buffer xDataBuffer(context, CL_MEM_READ_WRITE, COUNT * sizeof(cl_float));
	cl::Buffer yDataBuffer(context, CL_MEM_READ_WRITE, COUNT * sizeof(cl_float));
	cl::Buffer zDataBuffer(context, CL_MEM_READ_WRITE, COUNT * sizeof(cl_float));
	cl::Buffer radiusDataBuffer(context, CL_MEM_READ_WRITE, COUNT * sizeof(cl_float));

	cl::Buffer xCoordBuffer(context, CL_MEM_READ_WRITE, DIMENSION_SIZE * sizeof(cl_float));
	cl::Buffer yCoordBuffer(context, CL_MEM_READ_WRITE, DIMENSION_SIZE * sizeof(cl_float));
	cl::Buffer zCoordBuffer(context, CL_MEM_READ_WRITE, DIMENSION_SIZE * sizeof(cl_float));

	cl::Buffer resultBuffer(context, CL_MEM_READ_WRITE, DIMENSION_SIZE * sizeof(cl_float));
	cl::Buffer runBuffer(context, CL_MEM_READ_WRITE, sizeof(cl_bool));

	cl_int spheresCount = static_cast<cl_int>(COUNT);
	cl_int dimensionsCount = DIMENSION_SIZE;


	// Nastavim velikosti skupin
	// FIXME
	cl::NDRange local = 256;
	cl::NDRange global = alignTo(DIMENSION_SIZE, 256);


	//===========================================================================================
	// nastavim parametry spusteni kernelu
	cl_uint i = 0;
	kernel.setArg(i++, xDataBuffer);
	kernel.setArg(i++, yDataBuffer);
	kernel.setArg(i++, zDataBuffer);
	kernel.setArg(i++, radiusDataBuffer);

	kernel.setArg(i++, xCoordBuffer);
	kernel.setArg(i++, yCoordBuffer);
	kernel.setArg(i++, zCoordBuffer);

	kernel.setArg(i++, fromX);
	kernel.setArg(i++, fromY);
	kernel.setArg(i++, fromZ);
	kernel.setArg(i++, toX);
	kernel.setArg(i++, toY);
	kernel.setArg(i++, toZ);

	kernel.setArg(i++, resultBuffer);
	kernel.setArg(i++, spheresCount);
	kernel.setArg(i++, distanceLimit);
	kernel.setArg(i++, subcubesInLine);
	kernel.setArg(i++, dimensionsCount);
	kernel.setArg(i++, runBuffer);


	//double gpuStart = getTime();

	//===========================================================================================
	// Vytvorim casovac
	cl::UserEvent boundingSphereKernelEvent(context, &errMsg);
	clPrintErrorExit(errMsg, "clCreateUserEvent saxpy_ndrange_kernel_event");


	//===========================================================================================
	// Nahraji datove buffery
	queue.enqueueWriteBuffer(xDataBuffer, false, 0, COUNT * sizeof(cl_float), xData.data(), NULL, NULL);
	queue.enqueueWriteBuffer(yDataBuffer, false, 0, COUNT * sizeof(cl_float), yData.data(), NULL, NULL);
	queue.enqueueWriteBuffer(zDataBuffer, false, 0, COUNT * sizeof(cl_float), zData.data(), NULL, NULL);
	queue.enqueueWriteBuffer(radiusDataBuffer, false, 0, COUNT * sizeof(float), radiusData.data(), NULL, NULL);


	// Spustim kernel
	queue.enqueueNDRangeKernel(kernel, 0, global, local, NULL, &boundingSphereKernelEvent);
	//queue.enqueueNDRangeKernel(kernel, 0, global, local, NULL, NULL);


	// Ziskam vysledky
	queue.enqueueReadBuffer(resultBuffer, false, 0, DIMENSION_SIZE * sizeof(cl_float), resultsGPU.data(), NULL, NULL);


	// Synchronizace
	clPrintErrorExit(queue.finish(), "clFinish");

	Sphere gpuResultSphere = {resultsGPU[0], resultsGPU[1], resultsGPU[2], resultsGPU[3]};

	//double gpuEnd = getTime();
	////////////////////////////////////////////////



	// Kotrola vysledku
	typedef enum {NONE, CPU, GPU} ErrorType;
	for (size_t i = 0; i < COUNT; ++i) {
		ErrorType error = NONE;
		if (distanceSpheresCenters(cpuResultSphere, spheres.get(i)) > cpuResultSphere.radius) {
			error = CPU;
		}
		
		if (distanceSpheresCenters(gpuResultSphere, spheres.get(i)) > gpuResultSphere.radius) {
			error = GPU;
		}

		if (error != NONE) {
			printf("ERROR: koule %.3f  %.3f  %.3f  %.3f  nelezi v %s obalovaci kouli\n", spheres.get(i).x, spheres.get(i).y, spheres.get(i).z, spheres.get(i).radius, error == CPU ? "CPU" : "GPU");
		}
	}


	if (distanceSpheresCenters(cpuResultSphere, gpuResultSphere) > DEVIATION) {
		printf("Vysledek GPU neodpovida vysledku CPU!\nCPU:\n");
		printSphere(cpuResultSphere);
		printf("GPU:\n");
		printSphere(gpuResultSphere);
	}
	else {
		printf("Vysledek:\n");
		printSphere(gpuResultSphere);
	}


	// Vytisknu vysledky mereni
	printf("\nVysledny cas:\n");
	printf(" GPU cas: %fs\n", getEventTime(boundingSphereKernelEvent));
	printf(" CPU cas: %fs\n", cpuEnd - cpuStart);

	getchar();

	return 0;
}


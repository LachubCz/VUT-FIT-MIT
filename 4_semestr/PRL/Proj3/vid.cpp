/**
 * @author Petr Buchal
 * @date 19_04_2020
 * @file vid.cpp
 * @brief Viditelnost algorithm implementation
 */

#include <mpi.h>
#include <cmath>
#include <vector>
#include <string>
#include <sstream>

int main(int argc, char *argv[]){
    int my_id;
    int processors_count;

    MPI_Init(&argc,&argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &my_id);
    MPI_Comm_size(MPI_COMM_WORLD, &processors_count);

    //master will parse data and send them
    if (my_id == 0){
        std::vector<int> heights;
        std::stringstream ss(argv[1]);

        for (int i; ss >> i;) {
            heights.push_back(i);    
            if (ss.peek() == ',')
                ss.ignore();
        }

        for (int i = 0; i < processors_count; ++i) {
            MPI_Send(&heights[0], 1, MPI_INT, i, 0, MPI_COMM_WORLD); //send base value
            MPI_Send(&heights[i], 1, MPI_INT, i, 1, MPI_COMM_WORLD); //send my value
        }
    }

    int my_value;
    int base_value;
    MPI_Status status;
    MPI_Recv(&base_value, 1, MPI_INT, 0, 0, MPI_COMM_WORLD, &status); //recieve base value
    MPI_Recv(&my_value, 1, MPI_INT, 0, 1, MPI_COMM_WORLD, &status); //recieve my value
    
    float my_angle = atan((my_value-base_value)/float(my_id+1));

    //max_prev_angle
    float max_prev_angle;
    for (int i = 0; i < processors_count; ++i) {
        if (my_id == 0 && i == 0 && processors_count > 1) {
            MPI_Send(&my_angle, 1, MPI_INT, i+1, 0, MPI_COMM_WORLD);
        }
        else if (my_id == i && i != 0) {
            float neighbour_angle;
            MPI_Recv(&neighbour_angle, 1, MPI_INT, i-1, 0, MPI_COMM_WORLD, &status); //recieve value from previous neighbour

            max_prev_angle = neighbour_angle;
            if (neighbour_angle < my_angle) {
                neighbour_angle = my_angle;
            }
            if (i != (processors_count - 1)){
                MPI_Send(&neighbour_angle, 1, MPI_INT, i+1, 0, MPI_COMM_WORLD); //send value to next neighbour
            }
        }
    }

    if (my_id != 0) {
        if (my_angle > max_prev_angle) {
            char result = 'v'; //seen
            MPI_Send(&result, 1, MPI_INT, 0, 0, MPI_COMM_WORLD);
        }
        else {
            char result = 'u'; //unseen
            MPI_Send(&result, 1, MPI_INT, 0, 0, MPI_COMM_WORLD);
        }
    }

    if (my_id == 0) {//master will recieve data and print them
        char recieved_value;
        std::vector<char> values;
        values.push_back('_'); //first value
        //recieve
        for (int i = 1; i < processors_count; ++i) {
            MPI_Recv(&recieved_value, 1, MPI_INT, i, 0, MPI_COMM_WORLD, &status);
            values.push_back(recieved_value);
        }
        //print
        for (int i = 0; i < processors_count; ++i) {
            std::cout << values[i];
        }
        std::cout << std::endl;
    }

    MPI_Finalize();

    return 0;
}

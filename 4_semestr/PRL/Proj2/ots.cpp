/**
 * @author Petr Buchal
 * @date 27_03_2020
 * @file ots.cpp
 * @brief Odd-even transposition sort algorithm implementation
 */

#include <mpi.h>
#include <vector>
#include <fstream>

int recieve_and_compare(int my_id, int my_value, MPI_Status status) {
    int recieved_value;
    
    MPI_Recv(&recieved_value, 1, MPI_INT, my_id - 1, 0, MPI_COMM_WORLD, &status); //recieve value
        
    //compare values
    if (recieved_value > my_value) {
        MPI_Send(&my_value, 1, MPI_INT, my_id - 1, 0, MPI_COMM_WORLD);
        my_value = recieved_value;
    }
    else {
        MPI_Send(&recieved_value, 1, MPI_INT, my_id - 1, 0, MPI_COMM_WORLD);
    }
    
    return my_value;
}


int main(int argc, char *argv[]){
    int my_id;
    int processors_count;
    int values_count = atoi(argv[1]);

    MPI_Init(&argc,&argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &my_id);
    MPI_Comm_size(MPI_COMM_WORLD, &processors_count);

    if (processors_count != values_count){
        if (my_id == 0){
            std::cerr << "Count of numbers doesn't match count of processors." << std::endl;
        }
        MPI_Finalize();
        return 0;
    }

    //master will load data
    if (my_id == 0){
        int to_send;
        std::fstream fs;
        fs.open("numbers", std::fstream::in);

        for (int i = 0; i < values_count; ++i) {
            to_send = fs.get();
            MPI_Send(&to_send, 1, MPI_INT, i, 0, MPI_COMM_WORLD);
            std::cout << to_send << " ";
        }
        std::cout << std::endl;
        fs.close();
    }
    
    int my_value;
    MPI_Status status;
    MPI_Recv(&my_value, 1, MPI_INT, 0, 0, MPI_COMM_WORLD, &status);

    int recieved_value;
    for (int i = 0; i < (values_count / 2); ++i) {
        //odd sort, but even processes
        //sender
        if ((my_id % 2 == 0) && (my_id < ((2 * (values_count / 2)) - 1))) {
            MPI_Send(&my_value, 1, MPI_INT, my_id + 1, 0, MPI_COMM_WORLD); //send value
            MPI_Recv(&my_value, 1, MPI_INT, my_id + 1, 0, MPI_COMM_WORLD, &status); //recieve lesser value
        }
        else {
            //reciever
            if (my_id <= ((2 * (values_count / 2)) - 1)) {
                MPI_Recv(&recieved_value, 1, MPI_INT, my_id - 1, 0, MPI_COMM_WORLD, &status); //recieve value
                
                //compare values
                if (recieved_value > my_value) {
                    MPI_Send(&my_value, 1, MPI_INT, my_id - 1, 0, MPI_COMM_WORLD);
                    my_value = recieved_value;
                }
                else {
                    MPI_Send(&recieved_value, 1, MPI_INT, my_id - 1, 0, MPI_COMM_WORLD);
                }
            }
        }

        //even sort, but odd processes
        if ((my_id % 2 == 1) && (my_id < (2 * ((values_count - 1) / 2)))) {
            MPI_Send(&my_value, 1, MPI_INT, my_id + 1, 0, MPI_COMM_WORLD); //send value
            MPI_Recv(&my_value, 1, MPI_INT, my_id + 1, 0, MPI_COMM_WORLD, &status); //recieve lesser value
        }
        else {
            if ((my_id <= (2 * ((values_count - 1) / 2))) && (my_id != 0)) {
                MPI_Recv(&recieved_value, 1, MPI_INT, my_id - 1, 0, MPI_COMM_WORLD, &status); //recieve value
            
                //compare values
                if (recieved_value > my_value) {
                    MPI_Send(&my_value, 1, MPI_INT, my_id - 1, 0, MPI_COMM_WORLD);
                    my_value = recieved_value;
                }
                else {
                    MPI_Send(&recieved_value, 1, MPI_INT, my_id - 1, 0, MPI_COMM_WORLD);
                }
            }
        }
    }

    //send values to master
    for (int i = 0; i < values_count; ++i) {   
        if (my_id == i) {
            MPI_Send(&my_value, 1, MPI_INT, 0, 0, MPI_COMM_WORLD);
        }
    }

    //master will recieve values and print them
    std::vector<int> values;
    if (my_id == 0) {
        //recieve
        for (int i = 0; i < values_count; ++i) {
            MPI_Recv(&recieved_value, 1, MPI_INT, i, 0, MPI_COMM_WORLD, &status);
            values.push_back(recieved_value);
        }
        //print
        for (int i = 0; i < values.size(); ++i) {
            std::cout << values[i] << " " << std::endl;
        }
    }

    MPI_Finalize();

    return 0;
}

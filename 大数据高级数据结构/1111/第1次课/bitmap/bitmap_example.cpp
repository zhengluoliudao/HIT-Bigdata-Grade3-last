#include <iostream>
using namespace std;
#include "bitmap.hpp"

int main(int argc, char ** argv)
{
    int array[] = { 9, 5, 4, 6, 7, 8, 0, 1, 55, -100 };

    int min = array[0];
    int max = array[0];
    cout << "array: ";
    for (int i = 0; i < sizeof(array)/sizeof(array[0]); ++i) {
        if (array[i] > max) {
            max = array[i];
        }
        else if (array[i] < min) {
            min = array[i];
        }
        cout << array[i] << ' ';
    }
    cout << endl;

    BitMap bitmap(min, max);
    for (int i = 0; i < sizeof(array)/sizeof(array[0]); ++i) {
        bitmap.set(array[i]);
    }

    cout << "sorted:";
    for (int value = min; value <= max; ++value) {
        if (bitmap.test(value)) {
            cout << value << ' ';
        }
    }
    cout << endl;

    return(0);
}

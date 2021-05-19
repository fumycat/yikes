#include <iostream>

using namespace std;

void open_read_input_file(const char* filename)
{
    cout << filename << endl;
}

int main(int argc, const char *argv[])
{
    // ./e out_name input0 input1 ...
    // 0   1        2      3      ...
    if (argc == 1)
    {
        cout << "input files not specified" << endl;
        cout << "example: " << argv[0] << " output.txt input0.txt input1.txt ..." << endl;
        return -1;
    }
    cout << "Output: " << argv[1] << endl;
    for (int i = 2; i < argc; ++i)
    {
        open_read_input(argv[i]);
    }
    return 0;
}
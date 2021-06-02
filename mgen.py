x_includes = '''#include <thrust/device_vector.h>
#include <thrust/host_vector.h>
#include <thrust/execution_policy.h>
#include <thrust/transform.h>
#include <thrust/sequence.h>
#include <thrust/copy.h>
#include <thrust/fill.h>
#include <thrust/replace.h>
#include <thrust/functional.h>
#include <iostream>
#include <fstream>'''

x_functors = ''

x_main = '''int main(int argc, char const *argv[])
{
    std::ofstream fs(argv[1]);
'''

def x_vector_h(_type, _name, _len):
    return f'thrust::device_vector<{_type}> {_name}({_len});'

def x_vector_init_seq(_name, _init, _step):
    return f'thrust::sequence({_name}.begin(), {_name}.end(), {_init}, {_step});'

def x_vector_init_fill(_name, _f):
    return f'thrust::fill({_name}.begin(), {_name}.end(), {_f});'

def x_vector_init_custom(_name, _data):
    raise Exception('not implemented yet') # TODO

def x_transform_1(_p1, _out, _functor):
    # functor: thrust::negate<int>
    return f'thrust::transform({_p1}.begin(), {_p1}.end(), {_out}.begin(), {_functor}());'

def x_transform_2(_p1, _p2, _out, _functor):
    # functor: thrust::multiplies<float>
    return f'thrust::transform({_p1}.begin(), {_p1}.end(), {_p2}.begin(), {_out}.begin(), {_functor}());'

def x_of_file(_name, _type, _stream='fs'):
    return f'thrust::copy({_name}.begin(), {_name}.end(), std::ostream_iterator<{_type}>({_stream}, " "));'

x_close = '''return 0;
}'''


def construct(source_file_name, arrays, flow, functors):
    code = [x_includes, x_functors, x_main]
    ...
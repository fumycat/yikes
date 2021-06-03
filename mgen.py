import uuid

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
    return f'thrust::device_vector<{_type}> {_name}({_len});\n'

def x_vector_init_seq(_name, _init, _step):
    return f'thrust::sequence({_name}.begin(), {_name}.end(), {_init}, {_step});\n'

def x_vector_init_fill(_name, _f):
    return f'thrust::fill({_name}.begin(), {_name}.end(), {_f});\n'

def x_vector_init_custom(_name, _data):
    raise Exception('not implemented yet') # TODO

def x_transform_1(_p1, _out, _functor):
    # functor: thrust::negate<int>
    return f'thrust::transform({_p1}.begin(), {_p1}.end(), {_out}.begin(), {_functor}());\n'

def x_transform_2(_p1, _p2, _out, _functor):
    # functor: thrust::multiplies<float>
    return f'thrust::transform({_p1}.begin(), {_p1}.end(), {_p2}.begin(), {_out}.begin(), {_functor}());\n'

def x_of_file(_name, _type, _stream='fs'):
    return f'thrust::copy({_name}.begin(), {_name}.end(), std::ostream_iterator<{_type}>({_stream}, " "));\n'

x_close = '''return 0;
}'''


def construct(source_file_name, arrays, flow, functors, ttype, gout):
    code = [x_includes, x_functors, x_main]
    for arr in arrays:
        code.append(x_vector_h(ttype, arr['name'], arr['len']))
    for arr in arrays:
        if arr['type'] == 'sequence':
            code.append(x_vector_init_seq(arr['name'], arr['init'], arr['step']))
        elif arr['type'] == 'fill':
            code.append(x_vector_init_fill(arr['name'], arr['f']))
        elif arr['type'] == 'custom':
            code.append(x_vector_init_custom(arr['name'], arr['value']))
        else:
            pass # undefined

    for act in sorted(flow, key=lambda x: x['order']):
        tfunct = act['functor'].replace('<T>', f'<{ttype}>')
        if len(act['in']) == 1:
            code.append(x_transform_1(act['in'][0], act['out'], tfunct))
        elif len(act['in']) == 2:
            code.append(x_transform_2(act['in'][0], act['in'][1], act['out'], tfunct))
        else:
            raise Exception('bad input (length of params in flow)')

    code.append(x_of_file(gout, ttype))

    code.append(x_close)

    with open(source_file_name, 'w') as file:
        file.write('\n'.join(code))

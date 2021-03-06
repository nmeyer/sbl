from os import system


class StaticVisualizationGenerator():
    def generate(self,*args,**kwargs):
        raise Exception('Uh oh!','This is not implemented!')


class DigraphGenerator(StaticVisualizationGenerator):
    def __init__(self,verbose=True):
        self.__verbose = verbose
    def generate(self,interpreter_state):
        # Get the actual state.
        state = interpreter_state.split('Goals:')[1]
        # Clean up the lines a bit.
        state = map(lambda l: l.strip(),state.split('\n'))
        state = filter(lambda l: len(l) > 0,state)
        l = len(state)
        i = 0
        graphlines = []
        while i < l:
            # Build the list of things that follow.
            toplevel = {'state':state[i],'follows':[],'depends':[]}
            i += 1
            while i < l and '-->' in state[i]:
                # order is important here, so maintain it
                toplevel['follows'].append(state[i])
                i += 1
            # Pull the dependencies from the actual state.
            substate = toplevel['state']
            if ' (  ):' in substate:
                substate = substate.replace(' (  ):','')
            else:
                deps = (substate.split('(')[1]).split(')')[0].strip().split(',')
                deps = map(lambda d: d.strip(),deps)
                toplevel['depends'] = deps
                substate = substate.split('(')[0].strip()
            toplevel['state'] = substate
            if self.__verbose:
                print toplevel
            # Put the final line together.
            newline = [toplevel['state']]
            newline.extend(toplevel['follows'])
            depends = toplevel['depends']
            depends.extend(newline)
            depends = map(lambda x: x.replace('-->','').replace(' ','_'),depends)
            # Don't include atoms. Only include paths.
            if len(depends) > 1:
                graphlines.append('\t%s;' % ' -> '.join(depends))
        g = ['digraph G {']
        g.extend(graphlines)
        g.append('}')
        return '\n'.join(g)
    def generate_to_file(self,interpreter_state,graph_file='graphfile.txt',pretty_file='graph.pdf',pretty_format='pdf'):
        open(graph_file,'w').write(self.generate(interpreter_state))
        dot_file = '%s.dot' % graph_file.split('.')[0]
        system('dot %s > %s' % (graph_file,dot_file))
        system('neato -T%s %s -o %s' % (pretty_format,dot_file,pretty_file))


if __name__ == '__main__':
    dg = DigraphGenerator(verbose=False)
    dg.generate_to_file(open('interpreter_state.txt','r').read())


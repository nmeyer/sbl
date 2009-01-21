class StaticVisualizationGenerator():
    def generate(self,*args,**kwargs):
        raise Exception('Uh oh!','This is not implemented!')

class DigraphGenerator(StaticVisualizationGenerator):
    def __init__(self,verbose=True):
        self.__verbose = verbose
    def generate(self,interpreter_state):
        state = interpreter_state.split('Goals:')[1]
        state = map(lambda l: l.strip(),state.split('\n'))
        state = filter(lambda l: len(l) > 0,state)
        l = len(state)
        i = 0
        graphlines = []
        while i < l:
            toplevel = {'state':state[i],'follows':[]}
            i += 1
            while i < l and '-->' in state[i]:
                # order is important here, so maintain it
                toplevel['follows'].append(state[i])
                i += 1
            if self.__verbose:
                print toplevel
            newline = [toplevel['state']]
            newline.extend([ '%s;' % f[3:] for f in toplevel['follows'] ])
            graphlines.append('\t%s' % ' -> '.join(newline))
        g = ['digraph G {']
        g.extend(graphlines)
        g.append('}')
        return '\n'.join(g)
    def generate_to_file(self,interpreter_state,out_file='graphfile.txt'):
        open(out_file,'w').write(self.generate(interpreter_state))

if __name__ == '__main__':
    dg = DigraphGenerator(verbose=False)
    dg.generate_to_file(open('interpreter_state.txt','r').read())

#digraph G {
#    size = "4,4";
#    main -> parse -> execute;
#    main -> init;
#    ...
#}
#main [shape=box] /* this is a comment */
#[weight=8]
#[style=dotted]
#[shape=box,style=filled,color=".7 .3 1.0"]

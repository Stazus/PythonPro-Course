from graphviz import Digraph

# Definicja klas
class A:
    pass

class B(A):
    pass

class C(A):
    pass

class D(B):
    pass

class E(C):
    pass

class F(D, E):
    pass

# Sprawdzenie MRO klasy F
mro = F.mro()
print("MRO klasy F: ", mro)

# Tworzenie diagramu za pomocą Graphviz
dot = Digraph(comment='Hierarchia klas')

# Dodawanie klas do diagramu
for cls in mro:
    dot.node(cls.__name__, cls.__name__)
    
# Dodawanie połączeń (tylko dla dziedziczenia w MRO)
for cls in mro:
    for base in cls.__bases__:
        dot.edge(base.__name__, cls.__name__)
        
# Zapis diagramu do pliku PDF i PNG
dot.render('mro_diagram', format='pdf', cleanup=True)
dot.render('mro_diagram', format='png', cleanup=True)

print("Diagram MRO zapisany jako 'mro_diagram.pdf i 'mro_diagram.png.'")
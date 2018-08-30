# Kayak - genetic encoding space description framework
Kayak is a library for creating and managing dynamic genetic encoding spaces with default operations such as mutation or cross-over.
Have a look into *tests/* for working examples.

```python
import kayak
import kayak.feature_types as ft

space = kayak.GeneticEncoding('NeuralGraphSpace', '0.1.0')
space.add_feature('number_neurons', ft.NaturalInteger)
space.add_feature('number_edges', ft.NaturalInteger)
space.add_feature('graph_generator', [
    ft.FeatureSet({'name': 'ErdosRenyi', 'rewiring_probability': ft.UnitFloat}),
    ft.FeatureSet({'name': 'WattsStrogatz', 'm': ft.IntegerType(1, 10), 'k': ft.IntegerType(1, 20)})
])
space.add_feature('layers', ft.NaturalInteger)

code = space.sample_random()
  # e.g. [500, 10000, 'ErdosRenyi', 0.7, None, None, None, 5] or [500, 10000, 0, 'ErdosRenyi', 0.7, 5]
  # e.g. [250, 8000, None, None, 'WattsStrogatz', 4, 7, 5] or [250, 8000, 1, 'WattsStrogatz', 4, 7, 5] 
code_map = space.map(code)  # e.g. {'number_neurons': 500, 'number_edges': 10000, 'graph_generator': 0, 'name': 'ErdosRenyi', 'rewiring_probability': 0.7', 'number_layers': 5 }
```


# Install from Padim Gitlab repository
```bash
pip install --upgrade git+ssh://git@gitlab.padim.fim.uni-passau.de:13003/paddle/kayak.git
```

# Development
General issue tag tracking: https://gitlab.padim.fim.uni-passau.de/paddle/management/issues?scope=all&utf8=%E2%9C%93&state=opened&label_name[]=project-kayak

During development, have a look into issues of the management repo, e.g. in https://gitlab.padim.fim.uni-passau.de/paddle/management/issues/15

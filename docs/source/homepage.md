# `dendrogram`: N-Dimensional Dendrogram

[![version](https://img.shields.io/badge/version-v0.3.dev-brightgreen.svg?style=flat)](https://github.com/EnthalpyBill/Dendrogram)
[![license](https://img.shields.io/badge/license-MIT-blue.svg?style=flat)](https://github.com/EnthalpyBill/Dendrogram/blob/main/LICENSE)
[![docs](https://readthedocs.org/projects/dendrogram/badge/?version=latest)](https://dendrogram.readthedocs.io/en/latest/)

`dendrogram` is a toolkit for creating N-dimensional (ND) dendrogram. See [documentation](https://dendrogram.readthedocs.io/en/latest/) for details.

## Table of Contents

- [Intro](#intro)
- [Install](#install)
- [Usage](#usage)
- [Contribute](#contribute)
	- [Authors](#authors)
	- [Maintainers](#maintainers)
- [License](#license)

## Intro

*Placeholder*

## Install

The prerequisites of `dendrogram` are 

```
python >= 3.8
numpy >= 1.18
```

Lower versions may also work (and higher versions may not work). Please [raise an issue](https://github.com/EnthalpyBill/Dendrogram/issues/new) if it doesn't work for you. Next, you can `git clone` the source package from [GitHub](https://github.com/EnthalpyBill/Dendrogram):
```shell
$ git clone https://github.com/EnthalpyBill/Dendrogram.git
```
To build and install `dendrogram`, `cd` the folder and `pip install` it:
```shell
$ cd Dendrogram/
$ pip install -e .
```
The `-e` command allows you to make changes to the code. Remove it if you don't want to do so. `dendrogram` has not been published to `PyPI` yet. 

## Usage

To use the package, import it as
```python
>>> import dendrogram as dg
```
Let's consider a simple two-dimensional bimodal data. 
```python
>>> data = np.array([[2,1], [1,2]])
>>> print(data)
[[2 1]
 [1 2]]
```
We can easily generate the dendrogram tree with the following command:
```python
>>> tree = makeTree(data, min_value=0, print_progress=False)
```
`min_value` specifies the minimum value to consider when making the tree, and `print_progress` determines whether to print the progress or not. Other arguments include
- `min_delta` (scalar, default to 0): Lag to be ignored. 
- `min_npix` (int, default to 1): Minimum number of pixels to form a cluster.
- `num_level` (int, default to 100): Number of levels.

The `makeTree()` method returns a `dendrogram.structureTree.clusterTree` object. To visualize it, use the following command to show the topology of the tree:
```python
>>> tp = tree.topology()
└──(-1)
    └──(2)
        ├──(0)
        └──(1)
```
As expected, two branches labeled 0 and 1 illustrates the bimodality. 

## Contribute

Feel free to dive in! [Raise an issue](https://github.com/EnthalpyBill/Dendrogram/issues/new) or submit pull requests.

### Authors

- [@mxmintaka (Xi Meng)](https://github.com/mxmintaka)
- [@EnthalpyBill (Bill Chen)](https://github.com/EnthalpyBill)

### Maintainers

- [@EnthalpyBill (Bill Chen)](https://github.com/EnthalpyBill)

## License

`dendrogram` is available at [GitHub](https://github.com/EnthalpyBill/Dendrogram) under the [MIT license](https://github.com/EnthalpyBill/Dendrogram/blob/main/LICENSE).